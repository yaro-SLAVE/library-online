from django.contrib import admin

from library_service.models.catalog import Library, LibraryDatabase
from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.models.user import Basket, BasketItem, UserProfile
from library_service.models.comments import OrderComment, OrderItemComment


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "library_card",
        "campus_id",
        "mira_id",
        "fullname",
        "department",
    ]


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_filter = [
        "created_at",
    ]


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ["id", "basket", "book_id"]
    list_filter = [
        "basket",
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    list_filter = [
        "user",
    ]


@admin.register(OrderHistory)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "status", "date", "staff"]
    list_filter = ["status", "date"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "book_id", "status"]
    list_filter = ["order", "status"]


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ["id", "description", "address"]
    search_fields = [
        "location",
    ]


@admin.register(LibraryDatabase)
class LibraryDatabaseAdmin(admin.ModelAdmin):
    list_display = ["id", "database", "library"]


@admin.register(OrderComment)
class OrderCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "comment"]


@admin.register(OrderItemComment)
class OrderItemCommentAdmin(admin.ModelAdmin):
    list_display = ["id", "comment"]
