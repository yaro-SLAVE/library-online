from adrf import serializers as aserializers
from adrf import fields as afields
from rest_framework import serializers

from library_service.models.library_settings import LibrarySettings


class LibrarySettingsSerializer(aserializers.ModelSerializer):
    class Meta:
        model = LibrarySettings
        fields = "__all__"

class LibrarySettingsUpdateSerializer(aserializers.Serializer):
    max_books_per_order = serializers.IntegerField(required=False)
    max_books_per_reader = serializers.IntegerField(required=False)
    max_borrow_days = serializers.IntegerField(required=False)
    holidays = serializers.ListField(child=serializers.DateField, required=False)
    logo = serializers.ImageField()
    new_order_wait = serializers.FloatField(required=False)
    processing_order_wait = serializers.FloatField(required=False)

    async def aupdate(self, instance, validated_data):
        return instance
