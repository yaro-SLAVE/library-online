from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin, config, Undefined
from aiohttp import ClientSession
from django.conf import settings


@dataclass
class OpacBookLink(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    url: str
    description: str | None = None


@dataclass
class OpacBookExemplar(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    number: str
    amount: int
    status: str
    onhand: str | None = None
    sigla: str | None = None


@dataclass
class OpacBookInfo(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    author: list[str]
    collective: list[str]
    title: list[str]
    isbn: list[str]
    language: list[str]
    country: list[str]
    city: list[str]
    publisher: list[str]
    subject: list[str]
    keyword: list[str]


@dataclass
class OpacBook(DataClassJsonMixin):
    dataclass_json_config = config(undefined=Undefined.EXCLUDE)["dataclasses_json"]
    id: str
    description: str
    info: OpacBookInfo
    order: bool
    year: int
    exemplars: list[OpacBookExemplar]
    brief: str | None = None
    cover: str | None = None
    links: list[OpacBookLink] | None = None
    created: str | None = None


async def opac_search(client: ClientSession, database: str, expression: str) -> list[OpacBook]:
    payload = {"database": database, "expression": expression, "format": "@opac_plain"}

    params = {"extended": "true"}

    r = await client.post(f"{settings.OPAC_HOSTNAME}/api/search", json=payload, params=params)
    r.raise_for_status()
    return OpacBook.schema().load(await r.json(), many=True)


async def opac_book_retrieve(client: ClientSession, database: str, mfn: int) -> OpacBook:
    params = {"format": "@opac_plain", "extended": "true"}

    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/books/by/mfn/{database}/{mfn}", params=params)
    r.raise_for_status()
    return OpacBook.schema().load(await r.json())


async def opac_book_retrieve_by_id(client: ClientSession, database: str, book_id: str) -> OpacBook:
    params = {"format": "@opac_plain", "extended": "true", "db": database, "id": book_id}

    r = await client.get(f"{settings.OPAC_HOSTNAME}/api/books/", params=params)
    r.raise_for_status()
    return OpacBook.schema().load(await r.json())
