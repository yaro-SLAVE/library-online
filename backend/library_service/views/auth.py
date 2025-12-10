from aiohttp import ClientSession, ClientResponseError
from django.http import Http404
from asgiref.sync import sync_to_async

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from adrf.views import APIView as AsyncAPIView

from rest_framework.response import Response

from library_service.opac.api.login import login_reader, login_librarian, login_admin, get_login_info, AuthResponse, UserInfo

User = get_user_model()

class AuthViewset(AsyncAPIView):
    class Serializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField()

    async def post(self, request, *args, **kwargs):
        serializer = self.Serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        async with ClientSession() as client:
            error = ""
            response: AuthResponse | None = None
            is_reader = False
            is_admin = False
            is_librarian = False
            try:
                response = await login_reader(client, serializer.validated_data["username"], serializer.validated_data["password"])
                is_reader = True
            except ClientResponseError as e:
                error = e
            
            if error != "":
                try:
                    response = await login_admin(client, serializer.validated_data["username"], serializer.validated_data["password"])
                    is_admin = True
                except ClientResponseError as e:
                    error = e

                if error != "":
                    try:
                        response = await login_librarian(client, serializer.validated_data["username"], serializer.validated_data["password"])
                        is_librarian = True
                    except ClientResponseError as e:
                        error = e

            if not is_reader and not is_admin and not is_librarian:
                raise Http404("user not found")
            
            elif is_reader:
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
            
            elif is_librarian:
                info: UserInfo = await get_login_info(client, response.accessToken)
                user, created = await User.objects.prefetch_related("profile").aget_or_create(
                    profile__library_card=info.ticket,
                    defaults={
                        "username": serializer.validated_data["username"],
                        "email": info.mail,
                    },
                )

                if created:
                    await user.groups.aadd(await Group.objects.aget(name="Librarian"))

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
            
            elif is_admin:
                info: UserInfo = await get_login_info(client, response.accessToken)
                user, created = await User.objects.prefetch_related("profile").aget_or_create(
                    profile__library_card=info.ticket,
                    defaults={
                        "username": serializer.validated_data["username"],
                        "email": info.mail,
                    },
                )

                if created:
                    await user.groups.aadd(await Group.objects.aget(name="Librarian"))
                    user.is_superuser = True
                    await user.asave()

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