from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from library_service.models import Order, OrderHistory
from library_service.serializers.stats import LiveStatsSerializer
class StatsViewset(
    viewsets.ViewSet
):
    @action(detail=False, methods=['get'])
    def live(self, request):
        new_order_ids = OrderHistory.objects.filter(
            status='new'
        ).values_list('order_id', flat=True).distinct()

        processing_order_ids = OrderHistory.objects.filter(
            status='processing'
        ).values_list('order_id', flat=True).distinct()

        ready_order_ids = OrderHistory.objects.filter(
            status='ready'  
        ).values_list('order_id', flat=True).distinct()

        data = {
            'timestamp': timezone.now(),
            'total_orders': Order.objects.count(),
            'new_orders': len(new_order_ids),
            'orders_in_work': len(processing_order_ids),
            'orders_in_waiting': len(ready_order_ids),
        }

        serializer = LiveStatsSerializer(data)
        return Response(serializer.data)

