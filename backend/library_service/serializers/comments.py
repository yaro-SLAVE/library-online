from adrf import serializers as aserializers

from library_service.models.comments import OrderComment, OrderItemComment


class OrderCommentSerrializer(aserializers.ModelSerializer):

    class Meta:
        model = OrderComment
        fields = ["comment"]


class OrderItemCommentSerializer(aserializers.ModelSerializer):

    class Meta:
        model = OrderItemComment
        fields = ["comment"]
