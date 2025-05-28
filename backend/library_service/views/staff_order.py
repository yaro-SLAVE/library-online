from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from asgiref.sync import sync_to_async
from django.db.models import OuterRef, Subquery, Prefetch

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet

from aiohttp import ClientSession

from library_service.models.user import UserProfile
from library_service.opac.api.ticket import opac_reader_loans
from library_service.opac.book import book_retrieve_by_id

from library_service.mixins import (
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionUpdateModelMixin,
)

from library_service.models.order import Order, OrderHistory, OrderItem

from library_service.serializers.staff_order import (
    UserOrderSerializer,
    OrderSerializer,
    UpdateOrderSerializer,
    BorrowedBookSerializer,
    CheckOrderSerializer,
    OrderItemSerializer,
)

ACCEPTABLE_STATUSES = [
    OrderHistory.Status.NEW,
    OrderHistory.Status.PROCESSING,
    OrderHistory.Status.READY,
    OrderHistory.Status.DONE,
]


class StaffOrderViewset(
    SessionListModelMixin,
    AsyncGenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["get_orders"]:
            return UserOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related("library")

    @sync_to_async
    def get_data(self, target_status):
        queryset = self.get_queryset()

        last_status_subquery = OrderHistory.objects.filter(order=OuterRef("pk")).order_by("-date").values("status")[:1]

        queryset = queryset.annotate(last_status=Subquery(last_status_subquery)).filter(last_status=target_status)

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    @action(detail=False, methods=["get"], url_path="order")
    async def get_orders(self, request):
        status = self.request.query_params.get("status")
        target_status = OrderHistory.Status.NEW

        if status == "new":
            target_status = OrderHistory.Status.NEW
        elif status == "processing":
            target_status = OrderHistory.Status.PROCESSING
        elif status == "ready":
            target_status = OrderHistory.Status.READY
        else:
            target_status = OrderHistory.Status.DONE

        data = await self.get_data(target_status)
        return Response(data)


class StaffOrderGetUpdateViewset(
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionUpdateModelMixin,
    AsyncGenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["aupdate"]:
            return UpdateOrderSerializer
        elif self.action in ["check_order"]:
            return CheckOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "library",
                "user",
                "user__profile",
                Prefetch("statuses", queryset=OrderHistory.objects.select_related("order")),
                "statuses__staff",
                "statuses__staff__profile",
            )
        )

    @action(detail=False, methods=["GET"], url_path="check/(?P<order_id>\\w+)")
    async def check_order(self, request, order_id=None):
        order: Order = await self.get_queryset().prefetch_related("user").filter(id=order_id).afirst()
        profile: UserProfile = await UserProfile.objects.prefetch_related("user").aget(user=order.user)

        loans_id_list = []
        loans = []

        async with ClientSession() as client:
            self.client_session = client
            loans = await opac_reader_loans(client, profile.library_card)

            for loan in loans:
                book = await book_retrieve_by_id(client, loan.db, loan.book)
                loans_id_list.append(book.id)

            books = OrderItem.objects.prefetch_related("order").filter(order=order).all()
            found_books = []

            async for book in books:
                for loan in loans_id_list:
                    if book.book_id == loan:
                        found_books.append(book)
                        book.handed_date = loan.date
                        book.to_return_date = loan.deadline
                        await book.asave()

            notfound_books = []

            async for book in books:
                if book.book_id not in loans_id_list:
                    notfound_books.append(book)

            additional_books = []

            for loan in loans_id_list:
                if loan not in books:
                    additional_books.append(loan)

            response = {
                "found_books": await OrderItemSerializer(
                    found_books, many=True, context=self.get_serializer_context()
                ).adata,
                "notfound_books": await OrderItemSerializer(
                    notfound_books, many=True, context=self.get_serializer_context()
                ).adata,
                "additional_books": additional_books,
            }

        print(response)
        return Response(response)


class StaffBorrowedViewset(
    SessionRetrieveModelMixin,
    SessionListModelMixin,
    AsyncGenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = BorrowedBookSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related("library")

    # Получаем спсиок задолжностей, которые обещали принести с заказом
    async def aget_object(self):
        pk = self.kwargs["pk"]
        order: Order = await self.get_queryset().filter(id=pk).afirst()

        return await self.get_queryset().filter(order_to_return=order)
