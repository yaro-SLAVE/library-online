from adrf import mixins as amixins
from adrf.viewsets import GenericViewSet as AsyncGenericViewSet

from library_service.serializers.comments import (
    OrderCommentSerrializer,
    OrderItemCommentSerializer,
)

from library_service.models.comments import OrderComment, OrderItemComment


class OrderCommentViewset(AsyncGenericViewSet, amixins.ListModelMixin):
    serializer_class = OrderCommentSerrializer
    queryset = OrderComment.objects.all()


class OrderItemCommentViewset(AsyncGenericViewSet, amixins.ListModelMixin):
    serializer_class = OrderItemCommentSerializer
    queryset = OrderItemComment.objects.all()
