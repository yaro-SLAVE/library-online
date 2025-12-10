from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined, LetterCase
from aiohttp import ClientSession
from django.conf import settings


@dataclass
class AuthResponse(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    accessToken: str
    refreshToken: str


@dataclass
class UserInfo(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    ticket: str
    name: str
    allowed: bool
    debtor: bool
    gone: bool
    academ: bool
    everlasting: bool
    mira: str | None = None
    category: str | None = None
    department: str | None = None
    mail: str | None = None


async def login_reader(client: ClientSession, username: str, password: str) -> AuthResponse:
    payload = {"username": username, "password": password}

    r = await client.post(f"{settings.OPAC_HOSTNAME}/api/login/reader", json=payload)
    r.raise_for_status()
    return AuthResponse.schema().load(await r.json())


async def login_librarian(client: ClientSession, username: str, password: str) -> AuthResponse:
    payload = {"username": username, "password": password}

    r = await client.post(f"{settings.OPAC_HOSTNAME}/api/login/librarian", json=payload)
    r.raise_for_status()
    return AuthResponse.schema().load(await r.json())


async def login_admin(client: ClientSession, username: str, password: str) -> AuthResponse:
    payload = {"username": username, "password": password}

    r = await client.post(f"{settings.OPAC_HOSTNAME}/api/login/admin", json=payload)
    r.raise_for_status()
    return AuthResponse.schema().load(await r.json())


async def get_login_info(client: ClientSession, access_token: str) -> UserInfo:
    headers = {"Authorization": f"Bearer {access_token}"}

    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/readers/info", headers=headers)
    r.raise_for_status()
    return UserInfo.schema().load(await r.json())
