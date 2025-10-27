from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet
from asgiref.sync import sync_to_async

from aiohttp import ClientSession, ClientResponseError

from rest_framework.decorators import action

from library_service.opac.api.login import get_login_info, AuthResponse, UserInfo

from library_service.mixins import (
    LockUserMixin,
    SessionCreateModelMixin,
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionUpdateModelMixin,
)
from library_service.models.order import Order, OrderHistory, OrderItem

from library_service.serializers.order import BorrowedBookSerializer, CreateUpdateOrderSerializer, OrderSerializer, EternalOrderSerializer

from library_service.emails import send_new_order_notification

ACCEPTABLE_STATUSES = [
    OrderHistory.Status.NEW,
    OrderHistory.Status.PROCESSING,
    OrderHistory.Status.READY,
    OrderHistory.Status.DONE,
]

from django.contrib.auth import get_user_model

from library_service.models.user import UserProfile

User = get_user_model()


class OrderViewset(
    LockUserMixin,
    SessionListModelMixin,
    SessionRetrieveModelMixin,
    SessionCreateModelMixin,
    SessionUpdateModelMixin,
    AsyncGenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action in ["acreate", "aupdate"]:
            return CreateUpdateOrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).prefetch_related("library")

    @LockUserMixin.lock_request
    async def acreate(self, *args, **kwargs):
        response = await super().acreate(*args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            await send_new_order_notification()

        return response

    @LockUserMixin.lock_request
    async def aupdate(self, *args, **kwargs):
        return await super().aupdate(*args, **kwargs)

    @LockUserMixin.lock_request
    async def adestroy(self, request, *args, **kwargs):
        order = await self.aget_object()

        order_last_status = (
            await OrderHistory.objects.filter(order=order).order_by("date").alast()
        )  # Нам интересен только последний статус заказа

        if order_last_status.status not in ACCEPTABLE_STATUSES:
            raise ValidationError(
                f"Can't cancel an order with status {order_last_status.status}",
                code="cant_cancel_order",
            )

        await OrderHistory.objects.acreate(order=order, status=OrderHistory.Status.CANCELLED)

        async for book in order.books.all():
            book.status = OrderItem.Status.CANCELLED
            await book.asave()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BorrowedViewset(SessionListModelMixin, AsyncGenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(order__user=self.request.user, status=OrderItem.Status.HANDED)
    
class EternalOrderViewset(SessionListModelMixin, AsyncGenericViewSet):
    queryset = Order.objects.all()
    serializer_class = EternalOrderSerializer
            
    @action(detail=False, methods=["GET"], url_path="order")
    async def get_orders(self, request):
        authorization = self.request.headers.get('Authorization-eternal')

        async with ClientSession() as client:
            info: UserInfo = await get_login_info(client, authorization.split(' ')[1])
            userprofile = await UserProfile.objects.filter(library_card = info.ticket).aget()

            if userprofile:
                orders = await self.get_data(userprofile)
                return Response(orders)
            else:
                return Response([])

    @sync_to_async    
    def get_data(self, userprofile):
        orders =  Order.objects.filter(user = userprofile.user).all()
        serializer = self.get_serializer(orders, many=True)
        return serializer.data