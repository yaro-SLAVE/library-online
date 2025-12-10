from aiohttp import ClientSession, ClientResponseError
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from adrf.views import APIView as AsyncAPIView

from library_service.opac.api.ticket import opac_reader_info_by_mira, OpacReader

User = get_user_model()


class BitrixAuthView(AsyncAPIView):
    class Serializer(serializers.Serializer):
        code = serializers.CharField()

    # TODO: отрефакторить, чтобы pylint не ругался
    # pylint: disable-next=too-many-locals
    async def post(self, request, *args, **kwargs):
        serializer = self.Serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        async with ClientSession() as client:
            token_response = await client.get(
                "https://int.istu.edu/oauth/token/?grant_type=authorization_code",
                params={
                    "code": serializer.validated_data["code"],
                    "client_id": settings.OAUTH_CLIENT_ID,
                    "client_secret": settings.OAUTH_CLIENT_SECRET,
                },
            )

            token_response_data = await token_response.json()
            if token_response.status != 200:
                raise AuthenticationFailed(token_response_data["error_description"], code="token_response")

            userinfo_response = await client.get(
                token_response_data["client_endpoint"] + "user.info.json",
                params={
                    "auth": token_response_data["access_token"],
                },
            )

            userinfo_response_data = await userinfo_response.json()
            if userinfo_response.status != 200:
                raise AuthenticationFailed(
                    userinfo_response_data["error_description"],
                    code="userinfo_response",
                )

            result = userinfo_response_data["result"]

            campus_id = result["id"]
            email = result["email"]
            user, created = await User.objects.prefetch_related("profile").aget_or_create(
                username=email,
                defaults={
                    "username": email,
                    "email": email,
                    "first_name": result["name"] or "",
                    "last_name": result["last_name"] or "",
                },
            )

            user.profile.campus_id = campus_id

            if created:
                await user.groups.aadd(await Group.objects.aget(name="Reader"))
                await user.asave()

            # user.profile.is_teacher = bool(result["is_teacher"])
            # user.profile.is_student = bool(result["is_student"])
            # user.profile.full_name = " ".join(
            #     i for i in [result["last_name"], result["name"], result["second_name"]] if i
            # )

            mira_id = int(result["mira_id"][0] if result["mira_id"] else 0)
            if mira_id > 2:
                user.profile.mira_id = mira_id

            try:
                user_info: OpacReader = await opac_reader_info_by_mira(client, user.profile.mira_id)
                user.profile.library_card = user_info.ticket
                user.profile.fullname = user_info.name
                user.profile.department = user_info.department
            except ClientResponseError as error:
                pass #Если не нашли аккаунт с данным mira_id, есть смысл авторизовать читателя?

            await user.profile.asave()

            user.last_login = timezone.now()
            await user.asave(update_fields=['last_login'])

            # TODO: это можно в асинке переписать
            tokens = await sync_to_async(TokenObtainPairSerializer.get_token)(user)
            return Response(
                status=200,
                data={"refresh": str(tokens), "access": str(tokens.access_token)},
            )
