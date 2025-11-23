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
from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.serializers.order import UserOrderSerializer
from library_service.serializers.order import OrderSerializer
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
        
        completed_orders = Count(
            "user__order",
            filter=Q(user__order__statuses__status="done"),
            distinct=True
        )
        
        cancelled_orders = Count(
            "user__order", 
            filter=Q(user__order__statuses__status="cancelled"),
            distinct=True
        )
        
        active_orders = Count(
            "user__order",
            filter=Q(
                user__order__statuses__status__in=[
                    "new", "processing", "ready"
                ]
            ),
            distinct=True
        )
        
        total_books_ordered = Count(
            "user__order__books",
            filter=~Q(user__order__books__status="cancelled")
        )

        queryset = queryset.annotate(
            total_orders=total_orders,
            completed_orders=completed_orders,
            cancelled_orders=cancelled_orders,
            active_orders=active_orders,
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
        registration_date_from = filters.get('registration_date_from')
        registration_date_to = filters.get('registration_date_to')
        last_order_date_from = filters.get('last_order_date_from')
        last_order_date_to = filters.get('last_order_date_to')
        
        if registration_date_from:
            queryset = queryset.filter(user__date_joined__gte=registration_date_from)
        if registration_date_to:
            queryset = queryset.filter(user__date_joined__lte=registration_date_to)
        if last_order_date_from:
            queryset = queryset.filter(last_order_date__gte=last_order_date_from)
        if last_order_date_to:
            queryset = queryset.filter(last_order_date__lte=last_order_date_to)
            
        return queryset

    def _apply_boolean_filters(self, queryset, filters):
        has_active_orders = filters.get('has_active_orders')
        has_overdue_books = filters.get('has_overdue_books')
        current_order_statuses = filters.get('current_order_statuses')
        
        if has_active_orders:
            if has_active_orders.lower() == 'true':
                queryset = queryset.filter(active_orders__gt=0)
            elif has_active_orders.lower() == 'false':
                queryset = queryset.filter(active_orders=0)
            
        if has_overdue_books:
            if has_overdue_books.lower() == 'true':
                overdue_users = User.objects.filter(
                    order__books__status="handed",
                    order__books__to_return_date__lt=timezone.now().date()
                ).distinct().values_list('id', flat=True)
                queryset = queryset.filter(user_id__in=overdue_users)
            elif has_overdue_books.lower() == 'false':
                overdue_users = User.objects.filter(
                    order__books__status="handed",
                    order__books__to_return_date__lt=timezone.now().date()
                ).distinct().values_list('id', flat=True)
                queryset = queryset.exclude(user_id__in=overdue_users)
            
        if current_order_statuses:
            valid_statuses = [
                status for status in current_order_statuses 
                if status in ['new', 'processing', 'ready', 'done', 'cancelled', 'error', 'archived']
            ]
            if valid_statuses:
                status_users = User.objects.filter(
                    order__statuses__status__in=valid_statuses
                ).distinct().values_list('id', flat=True)
                queryset = queryset.filter(user_id__in=status_users)
            
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
            'registration_date_from': request.query_params.get('registration_date_from'),
            'registration_date_to': request.query_params.get('registration_date_to'),
            'last_order_date_from': request.query_params.get('last_order_date_from'),
            'last_order_date_to': request.query_params.get('last_order_date_to'),
            'has_active_orders': request.query_params.get('has_active_orders'),
            'has_overdue_books': request.query_params.get('has_overdue_books'),
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
            queryset = self._apply_boolean_filters(queryset, filters)

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
                except Exception as e:
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
    async def reader_orders(self):
        reader = await self.aget_object()
        orders = Order.objects.filter(user=reader.user).prefetch_related(
            'library', 'statuses', 'books'
        )
        
        from library_service.serializers.order import UserOrderSerializer
        
        serializer = UserOrderSerializer(orders, many=True, context=self.get_serializer_context())
        data = await serializer.adata
        return Response(data)
    
class ModeratorOrderViewset(AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ModeratorOrderSerializer
    queryset = Order.objects.all()