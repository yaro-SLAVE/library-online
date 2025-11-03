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
    
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class ProfileBannedViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.filter(banned_status_our=True)
    
    # GET /api/profile/banned/ - список забаненных пользователей
    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        banned_users = list(
            self.get_queryset().values('id', 'user__username')
        )
        
        return Response({"banned_users": banned_users})
    
    # PUT /api/profile/banned/ban/<id>/ - забанить пользователя
    @action(detail=False, methods=['put'], url_path='ban/(?P<user_id>[^/.]+)')
    def ban_user(self, request, user_id=None, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        if not user_id:
            return Response({"error": "user_id is required in URL"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_profile = get_object_or_404(UserProfile, id=user_id)
            
            if user_profile.banned_status_our:
                return Response({
                    "error": f"User {user_profile.user.username} is already banned"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user_profile.banned_status_our = True
            user_profile.save()
            
            return Response({
                "message": f"User {user_profile.user.username} has been banned",
                "user_id": user_id,
                "username": user_profile.user.username,
                "banned": True
            }, status=status.HTTP_200_OK)
            
        except UserProfile.DoesNotExist:
            return Response({"error": f"User with id {user_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid user_id format"}, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE /api/profile/banned/unban/<id>/ - разбанить пользователя
    @action(detail=False, methods=['delete'], url_path='unban/(?P<user_id>[^/.]+)')
    def unban_user(self, request, user_id=None, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        if not user_id:
            return Response({"error": "user_id is required in URL"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_profile = get_object_or_404(UserProfile, id=user_id)
            
            if not user_profile.banned_status_our:
                return Response({
                    "error": f"User {user_profile.user.username} is not banned"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user_profile.banned_status_our = False
            user_profile.save()
            
            return Response({
                "message": f"User {user_profile.user.username} has been unbanned",
                "user_id": user_id,
                "username": user_profile.user.username,
                "banned": False
            }, status=status.HTTP_200_OK)
            
        except UserProfile.DoesNotExist:
            return Response({"error": f"User with id {user_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid user_id format"}, status=status.HTTP_400_BAD_REQUEST)

