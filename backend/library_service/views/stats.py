from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Subquery, OuterRef
from library_service.models import Order, OrderHistory
from library_service.serializers.stats import LiveStatsSerializer

class StatsViewset(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def live(self, request):
        latest_status_subquery = OrderHistory.objects.filter(
            order=OuterRef('pk')
        ).order_by('-date').values('status')[:1]

        orders = Order.objects.annotate(
            last_status=Subquery(latest_status_subquery)
        )

        
        stats = orders.aggregate(
            total=Count('id'),
            new=Count('id', filter=Q(last_status=OrderHistory.Status.NEW)),
            processing=Count('id', filter=Q(last_status=OrderHistory.Status.PROCESSING)),
            ready=Count('id', filter=Q(last_status=OrderHistory.Status.READY)),
            done=Count('id', filter=Q(last_status=OrderHistory.Status.DONE)),
        )

        done_today = OrderHistory.objects.filter(
            status=OrderHistory.Status.DONE,
            date__date=timezone.now().date()
        ).values('order').distinct().count()

        data = {
            'timestamp': timezone.now(),
            'total_orders': stats['total'],
            'new_orders': stats['new'],
            'orders_in_work': stats['processing'],
            'orders_in_waiting': stats['ready'],
            'done_today': done_today,
        }

        serializer = LiveStatsSerializer(data)
        return Response(serializer.data)