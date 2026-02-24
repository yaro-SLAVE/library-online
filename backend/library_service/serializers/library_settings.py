from adrf import serializers as aserializers
from adrf import fields as afields
from rest_framework import serializers

from library_service.models.library_settings import LibrarySettings


class LibrarySettingsSerializer(aserializers.ModelSerializer):
    class Meta:
        model = LibrarySettings
        fields = "__all__"
