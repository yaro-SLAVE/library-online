import asyncio
from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from adrf import serializers as aserializers
from adrf import fields as afields

from library_service.models.order import Order, OrderHistory, OrderItem
from library_service.opac.book import book_retrieve, book_retrieve_safe
from library_service.models.catalog import Library

from library_service.serializers.catalog import BookSerializer, LibrarySerializer
from library_service.serializers.parallel_list import ParallelListSerializer

User = get_user_model()


class OrderStatusSerializer(aserializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ["description", "status", "date"]


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


class OrderItemSerializer(aserializers.ModelSerializer):
    book = afields.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "book",
            "status",
            "handed_date",
            "to_return_date",
            "returned_date",
        ]
        list_serializer_class = ParallelListSerializer

    async def get_book(self, obj: OrderItem):
        return BookSerializer(await book_retrieve(self.context["client_session"], obj.book_id)).data


class OrderSerializer(aserializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    books = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "library", "statuses", "books"]
        list_serializer_class = ParallelListSerializer


class UserOrderSerializer(aserializers.ModelSerializer):
    library = LibrarySerializer()
    statuses = OrderStatusSerializer(many=True)
    user = OrderUserSerializer()

    class Meta:
        model = Order
        fields = ["id", "user", "library", "statuses"]
        list_serializer_class = ParallelListSerializer


class CreateUpdateOrderSerializer(aserializers.Serializer):
    library = serializers.IntegerField()
    books = serializers.ListField(child=serializers.CharField())
    borrowed = serializers.ListField(child=serializers.IntegerField())

    async def validate_order(self, validated_data, order: Order | None = None):
        library = await Library.objects.aget(pk=validated_data["library"])
        books: list[str] = validated_data["books"]
        borrowed_books: list[str] = validated_data["borrowed"]

        if len(books) == 0:
            raise ValidationError("Can't make an empty order", code="empty_order")

        queryset = (
            OrderItem.objects.all()
            .filter(order__user=self.context["request"].user)
            .filter(Q(status=OrderItem.Status.ORDERED) | Q(status=OrderItem.Status.HANDED))
        )
        if order is not None:
            queryset = queryset.filter(~Q(order=order))
        current_books = [order_book.book_id async for order_book in queryset]

        tasks = []
        for book_id in set(books):

            async def task(book_id=book_id):
                if book_id in current_books:
                    raise ValidationError(
                        f"Can't order the same book {book_id} twice",
                        code="same_book_twice",
                    )

                book = await book_retrieve_safe(self.context["client_session"], book_id, library)

                if book is None:
                    raise ValidationError(f"Invalid book id {book_id}", code="invalid_book_id")

                if not book.can_be_ordered:
                    raise ValidationError(f"Can't order book {book_id}", code="cant_order_book")

            tasks.append(task())

        await asyncio.gather(*tasks)

        for book in borrowed_books:
            order_item = await OrderItem.objects.filter(pk=book).prefetch_related("order__user").afirst()
            if (
                order_item is None
                or order_item.order.user != self.context["request"].user
                or order_item.status != OrderItem.Status.HANDED
            ):
                raise ValidationError(f"Invalid borrowed book id {book}", code="invalid_borrowed_book_id")

    async def configure_order(self, order: Order, validated_data):
        books: list[str] = validated_data["books"]
        for book_id in set(books):
            # TODO: exemplar_id
            await OrderItem.objects.acreate(order=order, book_id=book_id)

        borrowed_books: list[str] = validated_data["borrowed"]
        for book in borrowed_books:
            order_item = await OrderItem.objects.aget(pk=book)
            order_item.order_to_return = order
            await order_item.asave()

    async def acreate(self, validated_data):
        user = self.context["request"].user

        await self.validate_order(validated_data)  # Проводим валидацию перед тем, как что-то добавлять в БД
        order = await Order.objects.acreate(user=user, library=await Library.objects.aget(pk=validated_data["library"]))
        await self.configure_order(order, validated_data)

        await OrderHistory.objects.acreate(order=order, status=OrderHistory.Status.NEW)
        return validated_data

    async def aupdate(self, instance: Order, validated_data):
        order_statuses = OrderHistory.objects.filter(order=instance).all()

        # Когда статус new, то в истории статусов заказа будет только одна запись
        if await order_statuses.acount() > 1:
            raise ValidationError("Order status is not new", code="cant_update_order")

        await self.validate_order(
            validated_data, instance
        )  # Проводим валидацию перед тем, как что-то редактировать в БД
        await OrderItem.objects.filter(order=instance).all().adelete()

        old_borrowed_books = OrderItem.objects.filter(order_to_return=instance).all()
        async for order_item in old_borrowed_books:
            order_item.order_to_return = None
            await order_item.asave()

        instance.library = await Library.objects.aget(pk=validated_data["library"])
        await instance.asave()

        await self.configure_order(instance, validated_data)
        # TODO: как-то помечать, что заказ был изменен?
        return validated_data


class BorrowedBookSerializer(aserializers.ModelSerializer):
    book = afields.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "book", "order", "handed_date", "to_return_date"]
        list_serializer_class = ParallelListSerializer

    async def get_book(self, obj: OrderItem):
        return BookSerializer(await book_retrieve(self.context["client_session"], obj.book_id)).data
