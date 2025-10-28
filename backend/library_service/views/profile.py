from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet

from library_service.models.user import UserProfile
from library_service.serializers.profile import ProfileSerializer

from asgiref.sync import sync_to_async

class ProfileViewset(AsyncGenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).prefetch_related("user")

    @action(detail=False, url_path="self-info", methods=["get"])
    async def get_self(self, request, *args, **kwargs):
        profile = await self.get_queryset().afirst()
        serializer = self.get_serializer(profile)
        return Response(await serializer.adata)

    @action(detail=False, url_path="banned", methods=["get"])
    async def get_banned_all(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=403)
        
        banned_usernames = await sync_to_async(list)(
            UserProfile.objects
            .filter(banned_status_our=True)
            .values_list('user__username', flat=True)
        )
        
        return Response({"banned_usernames": banned_usernames})
