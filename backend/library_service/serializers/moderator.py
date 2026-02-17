from rest_framework import serializers
from adrf import serializers as aserializers
from django.db.models import IntegerField
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
            "last_order_date",
        ]


class StaffStatsSerializer(aserializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    fullname = serializers.CharField(read_only=True)
    total_orders = serializers.IntegerField(read_only=True)
    cancelled_orders = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "username",
            "fullname",
            "total_orders",
            "cancelled_orders",
        ]

class ModeratorOrderSerializer(aserializers.ModelSerializer):
    fullname = serializers.CharField(source="user.profile.fullname", read_only=True)
    library_card = serializers.CharField(
        source="user.profile.library_card",
        read_only=True,
        allow_null=True,
    )
    library_name = serializers.CharField(source="library.description", read_only=True)
    current_status = serializers.CharField(
        source="latest_status",
        read_only=True,
        allow_null=True,
    )
    created_date = serializers.DateTimeField(read_only=True, allow_null=True)
    employee_collect = serializers.CharField(read_only=True)
    employee_issue = serializers.CharField(read_only=True)
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "fullname",
            "library_card",
            "library_name",
            "current_status",
            "created_date",
            "employee_collect",
            "employee_issue",
            "books_count",
        ]