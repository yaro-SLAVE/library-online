from rest_framework import serializers
from adrf import serializers as aserializers
from library_service.models.user import UserProfile
from library_service.models.order import Order, OrderHistory

class ReaderStatsSerializer(aserializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    fullname = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)
    library_card = serializers.CharField(read_only=True)
    campus_id = serializers.CharField(read_only=True)
    mira_id = serializers.CharField(read_only=True)
    
    total_books_ordered = serializers.IntegerField(read_only=True)
    total_orders = serializers.IntegerField(read_only=True)
    cancelled_orders = serializers.IntegerField(read_only=True)
    last_order_date = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username", 
            "fullname",
            "department",
            "library_card",
            "campus_id", 
            "mira_id",
            "total_books_ordered",
            "total_orders", 
            "cancelled_orders",
            "last_order_date"
        ]
        
class StaffStatsSerializer(aserializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    fullname = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)
    
    # Статистика по заказам, где сотрудник был исполнителем
    total_orders = serializers.IntegerField(read_only=True)
    cancelled_orders = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "fullname",
            "department",
            "total_orders",
            "cancelled_orders"
        ]
        
    async def get_total_orders(self, obj):
        # Количество заказов, где сотрудник был исполнителем
        return await OrderHistory.objects.filter(staff=obj.user).values('order').distinct().acount()
    
    async def get_cancelled_orders(self, obj):
        # Количество отмененных заказов, где сотрудник был исполнителем
        return await OrderHistory.objects.filter(
            staff=obj.user,
            status="cancelled"
        ).values('order').distinct().acount()

class ModeratorOrderSerializer(aserializers.ModelSerializer):

    class Meta:
        model = Order
        fields = []