from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from adrf.viewsets import GenericViewSet as AsyncGenericViewSet

from library_service.models.user import UserProfile
from library_service.serializers.profile import ProfileSerializer

from asgiref.sync import sync_to_async

from datetime import datetime, timedelta
from django.db.models import OuterRef, Exists

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
from django.db.models import Value, CharField
from django.db.models.functions import Concat
class ProfileBannedViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.filter(banned_status_our=True)
    
    # GET /api/profile/banned/ - список забаненных пользователей
    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        banned_profiles = self.get_queryset().filter(
            banned_status_our=True
        ).select_related('user')
        
        banned_users = [
            {
                'id': profile.id,
                'library_card': profile.library_card,
                'fullname': (
                    profile.fullname 
                    if profile.fullname and profile.fullname.strip() 
                    else f"{profile.user.first_name or ''} {profile.user.last_name or ''}".strip()
                ) or 'Не указано'
            }
            for profile in banned_profiles
        ]
        
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


    # GET /api/profile/candidates_for_ban/<YYYY-MM-DD>/<YYYY-MM-DD> - список пользователей - кандидатов попадания в список блокировки
    # Дата1 для фильтра / Дата2 для фильтра.
    @action(detail=False, methods=['get'], url_path='candidates_for_ban/(?P<start_date>[^/.]+)/(?P<end_date>[^/.]+)')
    def candidates_for_ban(self, request, start_date=None, end_date=None, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid start date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid end date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.db import connection
        from library_service.models.order import OrderHistory

        with connection.cursor() as cursor:
            sql = """
            SELECT 
                up.user_id,
                up.library_card,
                case when up.fullname is not null and length(trim(up.fullname)) > 0  then up.fullname  else u.first_name || ' ' || u.last_name end as fullname,
                COUNT(DISTINCT new_orders.order_id) as total_orders_count,
                COUNT(DISTINCT cancelled_orders.order_id) as cancelled_orders_count
            FROM 
                library_service_orderhistory new_orders
            LEFT JOIN 
                library_service_orderhistory cancelled_orders ON new_orders.order_id = cancelled_orders.order_id 
                AND cancelled_orders.status = %s 
                AND cancelled_orders.description = %s
            INNER JOIN 
                library_service_order ordr ON ordr.id = new_orders.order_id
            INNER JOIN 
                library_service_userprofile up ON up.user_id = ordr.user_id
            INNER JOIN 
                auth_user u ON up.user_id = u.id
            WHERE 
                new_orders.status = %s
                AND DATE(new_orders.date) BETWEEN %s AND %s
                AND up.banned_status_our = 0
            GROUP BY 
                up.user_id, up.library_card, u.username
            HAVING 
                COUNT(DISTINCT cancelled_orders.order_id) > 0;
            """
            
            cursor.execute(sql, [
                OrderHistory.Status.CANCELLED,  # для cancelled_orders
                OrderHistory.NOT_CAME_DESCRIPTION,
                OrderHistory.Status.NEW,        # для new_orders
                start_date_obj,
                end_date_obj
            ])
            
            columns = [col[0] for col in cursor.description]
            candidates_data = [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        
        return Response({
            'ban_candidates': candidates_data
        })

