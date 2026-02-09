from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q, Subquery, OuterRef, Min

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from asgiref.sync import sync_to_async

from library_service.models.user import UserProfile
from library_service.models.order import Order, OrderHistory
from library_service.serializers.order import OrderSerializer
from library_service.serializers.moderator import (
    ReaderStatsSerializer, 
    StaffStatsSerializer, 
    ModeratorOrderSerializer
)


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
            "user__order__books",
            distinct=True
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
            
            from aiohttp import ClientSession
            
            async with ClientSession() as client_session:
                context = {
                    'request': request,
                    'format': self.format_kwarg,
                    'view': self,
                    'client_session': client_session
                }
                
                # Создаем список задач для асинхронной сериализации каждого заказа
                serialized_data = []
                for order in orders:
                    serializer = OrderSerializer(order, context=context)
                    order_data = await serializer.adata
                    serialized_data.append(order_data)
                
                return Response(serialized_data)
            
        except Exception as e:
            print(f"Error in reader_orders: {str(e)}")  # Для отладки
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
                context = {
                    'request': request,
                    'format': self.format_kwarg,
                    'view': self,
                    'client_session': client_session
                }
                
                serializer = OrderSerializer(order, context=context)
                data = await serializer.adata
                
                return Response(data)
            
        except Exception as e:
            print(f"Error in reader_order_detail: {str(e)}")  # Для отладки
            return Response(
                {"error": "Ошибка при получении деталей заказа"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StaffViewset(AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StaffStatsSerializer
    queryset = UserProfile.objects.all()
    
    def get_staff_queryset(self):
        return self.get_queryset().select_related("user").filter(
            user__groups__name__in=['Librarian', 'Admin']
        ).distinct()
    
    def get_annotated_queryset(self):
        queryset = self.get_staff_queryset()
        
        from django.db.models import IntegerField
        
        # Подзапрос для подсчета уникальных заказов по сотруднику
        total_orders_subquery = OrderHistory.objects.filter(
            staff=OuterRef('user')
        ).values('staff').annotate(
            count=Count('order', distinct=True)
        ).values('count')[:1]
        
        # Подзапрос для подсчета отмененных заказов по сотруднику
        cancelled_orders_subquery = OrderHistory.objects.filter(
            staff=OuterRef('user'),
            status="cancelled"
        ).values('staff').annotate(
            count=Count('order', distinct=True)
        ).values('count')[:1]
        
        queryset = queryset.annotate(
            total_orders=Subquery(total_orders_subquery, output_field=IntegerField()),
            cancelled_orders=Subquery(cancelled_orders_subquery, output_field=IntegerField())
        )
        
        return queryset
    
    def _apply_search_filter(self, queryset, search_query):
        if search_query:
            # Ищем по ФИО и отделу
            queryset = queryset.filter(
                Q(fullname__icontains=search_query) |
                Q(department__icontains=search_query)
            )
        return queryset
    
    def _apply_ordering(self, queryset, sort_by, sort_order):
        valid_sort_fields = ['fullname', 'department', 'total_orders', 'cancelled_orders']
        
        if sort_by in valid_sort_fields:
            order_field = sort_by
            if sort_order == 'desc':
                order_field = f'-{order_field}'
            queryset = queryset.order_by(order_field)
        else:
            queryset = queryset.order_by('fullname')
            
        return queryset

    async def alist(self, request):
        # Для основного list используем stats endpoint
        return await self.staff_stats(request)
    
    @action(detail=True, methods=['get'], url_path='orders')
    async def staff_orders(self, request, pk=None):
        try:
            staff_profile = await self.aget_object()
            
            @sync_to_async
            def get_staff_orders(user_id):
                # Находим заказы, где сотрудник был исполнителем
                order_ids = OrderHistory.objects.filter(
                    staff_id=user_id
                ).values_list('order_id', flat=True).distinct()
                
                orders = Order.objects.filter(
                    id__in=order_ids
                ).annotate(
                    first_status_date=Min('statuses__date')
                ).prefetch_related(
                    'library', 'statuses', 'books', 'user__profile'
                ).order_by('-first_status_date')
                
                return list(orders)
            
            orders = await get_staff_orders(staff_profile.user_id)
            
            # Добавляем ClientSession как в ReadersViewset
            from aiohttp import ClientSession
            
            async with ClientSession() as client_session:
                context = {
                    'request': request,
                    'format': self.format_kwarg,
                    'view': self,
                    'client_session': client_session
                }
                
                # Создаем список задач для асинхронной сериализации каждого заказа
                serialized_data = []
                for order in orders:
                    serializer = OrderSerializer(order, context=context)
                    order_data = await serializer.adata
                    serialized_data.append(order_data)
                
                return Response(serialized_data)
            
        except Exception as e:
            print(f"Error in staff_orders: {str(e)}")
            return Response(
                {"error": "Ошибка при получении заказов сотрудника"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'], url_path='orders/(?P<order_id>[^/.]+)')
    async def staff_order_detail(self, request, pk=None, order_id=None):
        try:
            staff_profile = await self.aget_object()
            
            @sync_to_async
            def get_staff_order_detail(user_id, order_id):
                try:
                    # Проверяем, что сотрудник действительно обрабатывал этот заказ
                    order_handled = OrderHistory.objects.filter(
                        staff_id=user_id,
                        order_id=order_id
                    ).exists()
                    
                    if not order_handled:
                        return None
                    
                    order = Order.objects.select_related(
                        'library'
                    ).prefetch_related(
                        'statuses', 'books', 'user__profile'
                    ).get(id=order_id)
                    
                    return order
                except Order.DoesNotExist:
                    return None
            
            order = await get_staff_order_detail(staff_profile.user_id, order_id)
            
            if not order:
                return Response(
                    {"error": "Заказ не найден или сотрудник не обрабатывал этот заказ"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Добавляем ClientSession как в ReadersViewset
            from aiohttp import ClientSession
            
            async with ClientSession() as client_session:
                context = {
                    'request': request,
                    'format': self.format_kwarg,
                    'view': self,
                    'client_session': client_session
                }
                
                serializer = OrderSerializer(order, context=context)
                data = await serializer.adata
                
                return Response(data)
            
        except Exception as e:
            print(f"Error in staff_order_detail: {str(e)}")
            return Response(
                {"error": "Ошибка при получении деталей заказа"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='stats')
    async def staff_stats(self, request):
        try:
            queryset = self.get_annotated_queryset()
            
            # Применяем фильтры поиска
            search_query = request.query_params.get('search', '').strip()
            queryset = self._apply_search_filter(queryset, search_query)
            
            # Применяем сортировку
            sort_by = request.query_params.get('sort_by', 'fullname')
            sort_order = request.query_params.get('sort_order', 'asc')
            queryset = self._apply_ordering(queryset, sort_by, sort_order)
            
            # Пагинация
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 10))
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            
            total_count = await sync_to_async(queryset.count)()
            staff_members = await sync_to_async(list)(queryset[start_index:end_index])
            
            # Сериализация
            serializer = self.get_serializer(staff_members, many=True)
            data = await serializer.adata
            
            # Формирование пагинации
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
            print(f"Error in staff_stats: {str(e)}")
            return Response(
                {"error": "Ошибка при получении статистики сотрудников"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ModeratorOrderViewset(AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ModeratorOrderSerializer
    queryset = Order.objects.all()