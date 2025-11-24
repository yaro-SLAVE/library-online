from django.contrib.auth import get_user_model

from rest_framework import serializers

from adrf import serializers as aserializers
from adrf import fields as afields

from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.models.user import UserProfile
from library_service.opac.api.ticket import opac_reader_loans
from library_service.opac.book import book_retrieve_by_id
from library_service.opac.book import book_retrieve

from library_service.serializers.catalog import BookSerializer, LibrarySerializer
from library_service.serializers.parallel_list import ParallelListSerializer

from aiohttp import ClientSession

from datetime import datetime

from asgiref.sync import sync_to_async

User = get_user_model()


class StaffOrderSerializer(aserializers.ModelSerializer):
    campus_id = serializers.CharField(source="profile.campus_id", read_only=True)
    mira_id = serializers.CharField(source="profile.mira_id", read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    fullname = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "campus_id", "mira_id", "fullname", "department"]


class OrderStatusSerializer(aserializers.ModelSerializer):
    staff = StaffOrderSerializer()

    class Meta:
        model = OrderHistory
        fields = ["description", "status", "date", "staff"]


class OrderUserSerializer(aserializers.ModelSerializer):
    library_card = serializers.CharField(source="profile.library_card", read_only=True)
    campus_id = serializers.CharField(source="profile.campus_id", read_only=True)
    mira_id = serializers.CharField(source="profile.mira_id", read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    fullname = serializers.CharField(read_only=True)
    department = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "library_card", "campus_id", "mira_id", "fullname", "department"]

class BorrowedBookSerializer(aserializers.ModelSerializer):
    book = afields.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "book", "order", "handed_date", "to_return_date"]
        list_serializer_class = ParallelListSerializer

    async def get_book(self, obj: OrderItem):
        return BookSerializer(await book_retrieve(self.context["client_session"], obj.book_id)).data


class OrderItemSerializer(aserializers.ModelSerializer):
    book = afields.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "status",
            "description",
            "handed_date",
            "to_return_date",
            "returned_date",
            "analogous_order_item",
        ]
        list_serializer_class = ParallelListSerializer

    async def get_book(self, obj: OrderItem):
        return BookSerializer(await book_retrieve(self.context["client_session"], obj.book_id)).data


class OrderSerializer(aserializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    books = OrderItemSerializer(many=True)
    user = OrderUserSerializer()
    books_to_return = afields.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "library", "statuses", "books", "user", "books_to_return"]
        list_serializer_class = ParallelListSerializer

    @sync_to_async
    def get_books_to_return(self, obj: Order):
        last_status = OrderHistory.objects.filter(order=obj).order_by("-date").values("status")[:1]
        if (last_status == OrderHistory.Status.DONE):
            return BorrowedBookSerializer(OrderItem.objects.filter(order_to_return = obj, status = OrderItem.Status.RETURNED).all(), many=True).data
        else:
            return BorrowedBookSerializer(OrderItem.objects.filter(order_to_return = obj).all(), many=True).data


# TODO: нам нужно это повторение?
# pylint: disable=duplicate-code
class UserOrderSerializer(aserializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    user = OrderUserSerializer()

    class Meta:
        model = Order
        fields = ["id", "user", "library", "statuses"]
        list_serializer_class = ParallelListSerializer


# pylint: enable=duplicate-code


class OrderBookSerializer(aserializers.Serializer):
    book_id = serializers.CharField()
    status = serializers.CharField()
    description = serializers.CharField()
    analogous = serializers.CharField(required=False, allow_blank=True)

class UpdateOrderStatusSerializer(aserializers.ModelSerializer):

    class Meta:
        model = OrderHistory
        fields = ["description", "status"]

class UpdateOrderSerializer(aserializers.Serializer):
    status = UpdateOrderStatusSerializer()
    books = OrderBookSerializer(many=True)

    async def aupdate(self, instance: Order, validated_data):
        user = self.context["request"].user
        new_status = validated_data["status"]

        if new_status["status"] == OrderHistory.Status.PROCESSING:
            await OrderHistory.objects.acreate(
                order=instance, status=OrderHistory.Status.PROCESSING, description=new_status["description"], staff=user
            )

        elif new_status["status"] == OrderHistory.Status.NEW:
            await OrderHistory.objects.acreate(
                order=instance, status=OrderHistory.Status.NEW, description=new_status["description"], staff=user
            )

        elif new_status["status"] == OrderHistory.Status.READY:
            books = validated_data["books"]

            if (len(books) > 0):
                for book in books:
                    order_item = await OrderItem.objects.filter(pk=book['book_id'], order=instance).afirst()

                    if book["status"] == "analogous":
                        analogous_order_item = await OrderItem.objects.acreate(order=instance, book_id=book["analogous"])
                        order_item.description = book["description"]
                        order_item.analogous_order_item = analogous_order_item
                        order_item.status = OrderItem.Status.ANALOGOUS

                    if book["status"] == "cancelled":
                        order_item.status = OrderItem.Status.CANCELLED
                        order_item.description = book["description"]

                    await order_item.asave()

            if (await OrderItem.objects.filter(order=instance).exclude(status=OrderItem.Status.CANCELLED).afirst() is None):
                await OrderHistory.objects.acreate(
                    order=instance, status=OrderHistory.Status.CANCELLED, description="Нет найденных или замененных книг", staff=user
                )
            else:    
                await OrderHistory.objects.acreate(
                    order=instance, status=OrderHistory.Status.READY, description=new_status["description"], staff=user
                )

        elif new_status["status"] == OrderHistory.Status.DONE:
            order: Order = await Order.objects.prefetch_related("user").filter(id=instance.id).afirst()
            profile: UserProfile = await UserProfile.objects.prefetch_related("user").aget(user=order.user)

            loans_id_list = []
            loans = []

            loans = await opac_reader_loans(self.context["client_session"], profile.library_card)

            for loan in loans:
                book = await book_retrieve_by_id(self.context["client_session"], loan.db, loan.book)
                loans_id_list.append(book.id)
                loan.book_id = book.id

            books = await self.get_order_items(order)
            found_books = []

            async for book in books:
                for loan in loans:
                    if book.book_id == loan.book_id:
                        found_books.append(book)

            notfound_books = []

            async for book in books:
                if book.book_id not in loans_id_list:
                    notfound_books.append(book)     

            for item in found_books:
                item.status = OrderItem.Status.HANDED
                item.handed_date = loan.date
                item.to_return_date = loan.deadline
                await item.asave()

            for item in notfound_books:
                if item.status == OrderItem.Status.ORDERED:
                    item.status = OrderItem.Status.CANCELLED
                    await item.asave()
            
            books_to_return = await self.get_borroweds(order)

            async for book in books_to_return:
                if book.book_id not in loans_id_list:
                    book.status = OrderItem.Status.RETURNED
                    book.returned_date = datetime.now()

            await OrderHistory.objects.acreate(
                order=instance, status=OrderHistory.Status.DONE, description=new_status["description"], staff=user
            )

        elif new_status["status"] == OrderHistory.Status.CANCELLED:
            order_items_list: list[OrderItem] = OrderItem.objects.filter(order=instance).all()

            async for order_item in order_items_list:
                order_item.status = OrderItem.Status.CANCELLED
                await order_item.asave()

                if order_item.analogous_order_item is not None:
                    await OrderItem.objects.filter(id=order_item.analogous_order_item.id).adelete()

            items_to_return: list[OrderItem] = OrderItem.objects.filter(order_to_return=instance).all()

            async for order_item in items_to_return:
                order_item.order_to_return = None
                await order_item.asave()

            await OrderHistory.objects.acreate(
                order=instance, status=OrderHistory.Status.CANCELLED, description=new_status["description"], staff=user
            )

        return validated_data
    
    @sync_to_async
    def get_order_items(self, order):
        return OrderItem.objects.prefetch_related("order").filter(order=order).all()
    
    @sync_to_async
    def get_borroweds(self, order):
        return OrderItem.objects.filter(order_to_return = order).all()


class CheckOrderSerializer(aserializers.Serializer):
    found_books = OrderItemSerializer(many=True)
    notfound_books = OrderItemSerializer(many=True)
    additional_books = BookSerializer(many=True)
