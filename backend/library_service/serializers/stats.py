from rest_framework import serializers

class LiveStatsSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    total_orders = serializers.IntegerField()
    new_orders = serializers.IntegerField()
    orders_in_work = serializers.IntegerField()
    orders_in_waiting = serializers.IntegerField()
