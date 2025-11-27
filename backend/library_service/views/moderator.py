from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q, Subquery, OuterRef, Min
from django.utils import timezone

from django.contrib.auth.models import User

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from asgiref.sync import sync_to_async

from library_service.models.user import UserProfile
from library_service.models.order import Order, OrderHistory
from library_service.serializers.order import UserOrderSerializer, OrderSerializer
from library_service.serializers.moderator import ReaderStatsSerializer, ModeratorOrderSerializer


class ReadersViewset(AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReaderStatsSerializer
    queryset = UserProfile.objects.all()

    def get_annotated_queryset(self):
        queryset = super().get_queryset().select_related("user")
        
        last_order_subquery = OrderHistory.objects.filter(
            order__user=OuterRef("user")
        ).order_by("-date").values("date")[:1]
        
        total_orders = Count("user__order", distinct=True)
        
        cancelled_orders = Count(
            "user__order", 
            filter=Q(user__order__statuses__status="cancelled"),
            distinct=True
        )
        
        total_books_ordered = Count(
            "user__order__books"
        )

        queryset = queryset.annotate(
            total_orders=total_orders,
            cancelled_orders=cancelled_orders,
            total_books_ordered=total_books_ordered,
            last_order_date=Subquery(last_order_subquery)
        )
        
        return queryset

    def _apply_text_filters(self, queryset, fullname, department):
        if fullname:
            queryset = queryset.filter(fullname__icontains=fullname)
                    
        if department:
            queryset = queryset.filter(department__icontains=department)
                    
        return queryset

    def _apply_date_filters(self, queryset, filters):
        last_order_date_from = filters.get('last_order_date_from')
        last_order_date_to = filters.get('last_order_date_to')
        
        if last_order_date_from:
            queryset = queryset.filter(last_order_date__gte=last_order_date_from)
        if last_order_date_to:
            queryset = queryset.filter(last_order_date__lte=last_order_date_to)
            
        return queryset
    
    def _apply_status_filters(self, queryset, current_order_statuses):
        if not current_order_statuses:
            return queryset
            
        valid_statuses = [
            status for status in current_order_statuses 
            if status in ['new', 'processing', 'ready', 'done', 'cancelled', 'error', 'archived']
        ]
        
        if not valid_statuses:
            return queryset
        
        # Находим пользователей, у которых есть заказы с указанными статусами
        from django.db.models import Exists, OuterRef
        
        orders_with_status = Order.objects.filter(
            user=OuterRef('user'),
            statuses__status__in=valid_statuses
        )
        
        queryset = queryset.filter(Exists(orders_with_status))
            
        return queryset

    def _apply_ordering(self, queryset, sort_by, sort_order):
        valid_sort_fields = ['id', 'fullname', 'department', 'total_books_ordered', 'total_orders', 'cancelled_orders']
        
        if sort_by in valid_sort_fields:
            order_field = sort_by
            if sort_order == 'desc':
                order_field = f'-{order_field}'
            queryset = queryset.order_by(order_field)
        else:
            queryset = queryset.order_by('id')
            
        return queryset

    async def alist(self, request):
        filters = {
            'fullname': request.query_params.get('fullname', '').strip(),
            'department': request.query_params.get('department', '').strip(),
            'last_order_date_from': request.query_params.get('last_order_date_from'),
            'last_order_date_to': request.query_params.get('last_order_date_to'),
            'current_order_statuses': request.query_params.getlist('current_order_statuses[]'),
        }
        
        sort_by = request.query_params.get('sort_by', 'id')
        sort_order = request.query_params.get('sort_order', 'asc')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        try:
            queryset = self.get_annotated_queryset()

            queryset = self._apply_text_filters(queryset, filters['fullname'], filters['department'])
            queryset = self._apply_date_filters(queryset, filters)
            queryset = self._apply_status_filters(queryset, filters['current_order_statuses'])

            queryset = self._apply_ordering(queryset, sort_by, sort_order)

            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            
            total_count = await sync_to_async(queryset.count)()
            readers = await sync_to_async(list)(queryset[start_index:end_index])
            
            serializer = self.get_serializer(readers, many=True)
            data = await serializer.adata
            
            base_url = request.build_absolute_uri().split('?')[0]
            query_params = request.GET.copy()
            
            next_page = None
            previous_page = None
            
            if end_index < total_count:
                query_params['page'] = page + 1
                next_page = f"{base_url}?{query_params.urlencode()}"
                
            if page > 1:
                query_params['page'] = page - 1
                previous_page = f"{base_url}?{query_params.urlencode()}"

            return Response({
                "count": total_count,
                "next": next_page,
                "previous": previous_page,
                "results": data
            })

        except Exception as e:
            return Response({"error": "Внутренняя ошибка сервера"}, status=500)

    @action(detail=True, methods=['get'], url_path='orders')
    async def reader_orders(self, request, pk=None):
        try:
            reader = await self.aget_object()

            @sync_to_async
            def get_orders_for_user(user_id):
                orders = Order.objects.filter(user_id=user_id).annotate(
                    first_status_date=Min('statuses__date')
                ).prefetch_related(
                    'library', 'statuses', 'books'
                ).order_by('-first_status_date')
                
                return list(orders)
            
            orders = await get_orders_for_user(reader.user_id)
            
            @sync_to_async
            def serialize_orders(orders_data, context):
                serializer = UserOrderSerializer(
                    orders_data, 
                    many=True, 
                    context=context
                )
                return serializer.data
            
            data = await serialize_orders(orders, self.get_serializer_context())
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {"error": "Ошибка при получении заказов читателя"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='orders/(?P<order_id>[^/.]+)')
    async def reader_order_detail(self, request, pk=None, order_id=None):
        try:
            reader = await self.aget_object()

            @sync_to_async
            def get_order_detail(user_id, order_id):
                try:
                    order = Order.objects.select_related(
                        'library'
                    ).prefetch_related(
                        'statuses', 'books'
                    ).get(
                        id=order_id, 
                        user_id=user_id
                    )
                    return order
                except Order.DoesNotExist:
                    return None
            
            order = await get_order_detail(reader.user_id, order_id)
            
            if not order:
                return Response(
                    {"error": "Заказ не найден или не принадлежит данному читателю"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            from aiohttp import ClientSession
            
            async with ClientSession() as client_session:
                context = self.get_serializer_context()
                context['client_session'] = client_session
                
                serializer = OrderSerializer(
                    order, 
                    context=context
                )
                data = await serializer.adata
                
                return Response(data)
            
        except Exception as e:
            return Response(
                {"error": "Ошибка при получении деталей заказа"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class ModeratorOrderViewset(AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ModeratorOrderSerializer
    queryset = Order.objects.all()