from aiohttp import ClientSession, ClientResponseError
from django.http import Http404
from asgiref.sync import sync_to_async

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from adrf.views import APIView as AsyncAPIView

from rest_framework.response import Response

from library_service.opac.api.login import login_reader, login_librarian, login_admin, get_login_info, AuthResponse, UserInfo, login_universal, AuthUniversalResponse

from library_service.models.user import UserProfile

User = get_user_model()

class LogoutViewset(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data.get("refresh"))

            user_id = token.payload["user_id"]
            
            user = User.objects.filter(pk = user_id).first()

            profile = UserProfile.objects.filter(user = user).first()
            profile.current_role = None
            profile.save()

            token.blacklist()

            return Response({"detail": "Successfully logged out."}, status=200)
        except TokenError:
            return Response({"detail": "Invalid token or missing token."}, status=400)

class AuthViewset(AsyncAPIView):
    class Serializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    async def post(self, request, *args, **kwargs):
        serializer = self.Serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        async with ClientSession() as client:
            error = ""
            response: AuthUniversalResponse | None = None

            try:
                response = await login_universal(client, serializer.validated_data["username"], serializer.validated_data["password"])
            except ClientResponseError as e:
                error = e
            
            if error == "":
                info: UserInfo = await get_login_info(client, response.accessToken)
                user, created = await User.objects.prefetch_related("profile").aget_or_create(
                    profile__library_card=info.ticket,
                    defaults={
                        "username": serializer.validated_data["username"],
                        "email": info.mail,
                    },
                )

                if created:
                    await user.groups.aadd(await Group.objects.aget(name="Reader"))
                    if "Librarian" in response.roles:
                        await user.groups.aadd(await Group.objects.aget(name="Librarian"))
                        if "Admin" in response.roles:
                            await user.groups.aadd(await Group.objects.aget(name="Librarian"))
                            user.is_superuser = True
                    await user.asave()

                user.profile.library_card = info.ticket
                user.profile.fullname = info.name
                user.profile.department = info.department
                user.profile.mira_id = info.mira

                user_groups = [x.name async for x in user.groups.all()]

                if ("Librarian" not in user_groups):
                    print(user_groups)
                    print(user.profile.current_role)
                    user.profile.current_role = "Reader"
                else:
                    user.profile.current_role = None

                await user.profile.asave()

                user.last_login = timezone.now()
                await user.asave(update_fields=['last_login'])

                tokens = await sync_to_async(TokenObtainPairSerializer.get_token)(user)
                return Response(
                    status=200,
                    data={"refresh": str(tokens), "access": str(tokens.access_token)},
                )
            
class AuthThirdPartyViewset(AsyncAPIView):
    class Serializer(serializers.Serializer):
        token = serializers.CharField()

    async def post(self, request, *args, **kwargs):
        serializer = self.Serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        async with ClientSession() as client:

            try:
                info: UserInfo = await get_login_info(client, serializer.validated_data["token"])
                user, created = await User.objects.prefetch_related("profile").aget_or_create(
                    username = serializer.validated_data["username"],
                    defaults={
                        "username": serializer.validated_data["username"],
                        "email": info.mail,
                    },
                )

                if created:
                    await user.groups.aadd(await Group.objects.aget(name="Reader"))

                user.profile.library_card = info.ticket
                user.profile.fullname = info.name
                user.profile.department = info.department
                user.profile.mira_id = info.mira
                await user.profile.asave()

                user.last_login = timezone.now()
                await user.asave(update_fields=['last_login'])
                
                tokens = await sync_to_async(TokenObtainPairSerializer.get_token)(user)
                return Response(
                    status=200,
                    data={"refresh": str(tokens), "access": str(tokens.access_token)},
                )                

            except ClientResponseError as e:
                return Response(status=400, data="Bad request")