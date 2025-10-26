from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q, Subquery, OuterRef
from django.utils import timezone

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from asgiref.sync import sync_to_async

from library_service.models.user import UserProfile
from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.serializers.readers import ReaderStatsSerializer

class ReadersViewset(AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReaderStatsSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset().select_related("user")
        
        last_order_subquery = OrderHistory.objects.filter(
            order__user=OuterRef("user")
        ).order_by("-date").values("date")[:1]
        
        total_orders = Count("user__order", distinct=True)
        
        completed_orders = Count(
            "user__order",
            filter=Q(user__order__statuses__status=OrderHistory.Status.DONE),
            distinct=True
        )
        
        cancelled_orders = Count(
            "user__order", 
            filter=Q(user__order__statuses__status=OrderHistory.Status.CANCELLED),
            distinct=True
        )
        
        active_orders = Count(
            "user__order",
            filter=Q(
                user__order__statuses__status__in=[
                    OrderHistory.Status.NEW,
                    OrderHistory.Status.PROCESSING, 
                    OrderHistory.Status.READY
                ]
            ),
            distinct=True
        )
        
        total_books_ordered = Count(
            "user__order__books",
            filter=~Q(user__order__books__status=OrderItem.Status.CANCELLED)
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

    async def alist(self, request):
        fullname = request.query_params.get('fullname', '').strip()
        min_books = request.query_params.get('min_books')
        max_books = request.query_params.get('max_books')
        min_orders = request.query_params.get('min_orders')
        max_orders = request.query_params.get('max_orders')
        min_cancelled = request.query_params.get('min_cancelled')
        max_cancelled = request.query_params.get('max_cancelled')
        
        registration_date_from = request.query_params.get('registration_date_from')
        registration_date_to = request.query_params.get('registration_date_to')
        last_order_date_from = request.query_params.get('last_order_date_from')
        last_order_date_to = request.query_params.get('last_order_date_to')
        
        has_active_orders = request.query_params.get('has_active_orders')
        has_overdue_books = request.query_params.get('has_overdue_books')
        current_order_statuses = request.query_params.getlist('current_order_statuses[]')
        
        sort_by = request.query_params.get('sort_by', 'id')
        sort_order = request.query_params.get('sort_order', 'asc')
        
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        queryset = self.get_queryset()

        if fullname:
            queryset = queryset.filter(
                Q(fullname__icontains=fullname) |
                Q(user__first_name__icontains=fullname) |
                Q(user__last_name__icontains=fullname)
            )

        if min_books:
            queryset = queryset.filter(total_books_ordered__gte=int(min_books))
        if max_books:
            queryset = queryset.filter(total_books_ordered__lte=int(max_books))
            
        if min_orders:
            queryset = queryset.filter(total_orders__gte=int(min_orders))
        if max_orders:
            queryset = queryset.filter(total_orders__lte=int(max_orders))
            
        if min_cancelled:
            queryset = queryset.filter(cancelled_orders__gte=int(min_cancelled))
        if max_cancelled:
            queryset = queryset.filter(cancelled_orders__lte=int(max_cancelled))

        if registration_date_from:
            queryset = queryset.filter(user__date_joined__gte=registration_date_from)
        if registration_date_to:
            queryset = queryset.filter(user__date_joined__lte=registration_date_to)
            
        if last_order_date_from:
            queryset = queryset.filter(last_order_date__gte=last_order_date_from)
        if last_order_date_to:
            queryset = queryset.filter(last_order_date__lte=last_order_date_to)

        if has_active_orders and has_active_orders.lower() == 'true':
            queryset = queryset.filter(active_orders__gt=0)
            
        if has_overdue_books and has_overdue_books.lower() == 'true':
            overdue_users = User.objects.filter(
                order__books__status=OrderItem.Status.HANDED,
                order__books__to_return_date__lt=timezone.now().date()
            ).values_list('id', flat=True)
            queryset = queryset.filter(user_id__in=overdue_users)
            
        if current_order_statuses:
            status_users = User.objects.filter(
                order__statuses__status__in=current_order_statuses
            ).values_list('id', flat=True)
            queryset = queryset.filter(user_id__in=status_users)

        if sort_by in ['fullname', 'total_orders', 'total_books_ordered', 'cancelled_orders']:
            order_field = sort_by
            if sort_order == 'desc':
                order_field = f'-{order_field}'
            queryset = queryset.order_by(order_field)
        else:
            queryset = queryset.order_by('id')

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        total_count = await sync_to_async(queryset.count)()
        readers = await sync_to_async(list)(queryset[start_index:end_index])
        
        serializer = self.get_serializer(readers, many=True)
        data = await serializer.adata
        
        return Response({
            "count": total_count,
            "next": f"{request.build_absolute_uri()}?page={page + 1}" if end_index < total_count else None,
            "previous": f"{request.build_absolute_uri()}?page={page - 1}" if page > 1 else None,
            "results": data
        })

    # Детальная информация о читателе
    @action(detail=True, methods=['get'], url_path='details')
    async def reader_details(self):
        reader = await self.aget_object()
        serializer = self.get_serializer(reader)
        return Response(await serializer.adata)

    # Заказы конкретного читателя
    @action(detail=True, methods=['get'], url_path='orders')
    async def reader_orders(self):
        reader = await self.aget_object()
        orders = Order.objects.filter(user=reader.user).prefetch_related(
            'library', 'statuses', 'books'
        )
        
        from library_service.serializers.order import UserOrderSerializer
        
        serializer = UserOrderSerializer(orders, many=True, context=self.get_serializer_context())
        data = await serializer.adata
        return Response(data)