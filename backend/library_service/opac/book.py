from dataclasses import dataclass
from typing import Iterable

import asyncio
from aiohttp import ClientSession
from django.conf import settings

from library_service.opac.api.announces import opac_announces_list
from library_service.models.catalog import Library, LibraryDatabase
from library_service.opac.api.book import OpacBook, opac_book_retrieve, opac_search, opac_book_retrieve_by_id


@dataclass
class BookLink:
    url: str
    description: str | None


@dataclass
class Book:
    id: str
    library: int
    description: str
    year: int
    copies: int
    can_be_ordered: bool
    links: list[BookLink]
    # pylint: disable=duplicate-code
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
    # pylint: enable=duplicate-code
    cover: str | None
    brief: str | None
    created: str | None

    def __init__(self, book: OpacBook, library: int):
        self.id = book.id.replace("/", "_")
        self.library = library
        self.description = book.description
        self.year = book.year
        self.copies = len(book.exemplars)
        self.can_be_ordered = book.order
        self.links = [BookLink(link.url, link.description) for link in (book.links or [])]
        self.author = book.info.author
        self.collective = book.info.collective
        self.title = book.info.title
        self.isbn = book.info.isbn
        self.language = book.info.language
        self.country = book.info.country
        self.city = book.info.city
        self.publisher = book.info.publisher
        self.subject = book.info.subject
        self.keyword = book.info.keyword
        self.cover = (
            settings.OPAC_HOSTNAME.removesuffix("/opac") + book.cover if book.cover else None
        )  # TODO: по идее, лучше проксировать
        self.brief = book.brief
        self.created = book.created


# Obtain database name and mfn id
def split_book_id(book_id: str) -> tuple[str, str]:
    return book_id.split("_")


async def books_list(client: ClientSession, libraries: Iterable[Library], expression: str) -> list[Book]:
    tasks = []
    async for library in libraries:
        databases: Iterable[LibraryDatabase] = library.databases.all()
        async for db in databases:

            async def task(library=library, db=db) -> list[Book]:
                search_result = await opac_search(client, db.database, expression)
                return [Book(book, library.id) for book in search_result]

            tasks.append(task())

    result: list[list[Book]] = await asyncio.gather(*tasks)
    return [book for book_list in result for book in book_list]


async def books_announces_list(client: ClientSession) -> list[Book]:
    announces = await opac_announces_list(client)
    
    # NOTE: тут вылетит исключение, если не зарегистрирована БД ISTU
    istu_library = (
        await LibraryDatabase.objects.filter(database="ISTU").prefetch_related("library").afirst()
    ).library  # По идее, все анонсы отсылают на ISTU

    tasks = []
    for announce in announces:

        async def task(announce=announce) -> Book:
            # TODO: привести это в порядок
            expresssion = announce.link.removeprefix("/opac/index.html?db=ISTU&expression=")  # Спс за такой удобный апи
            book = (await opac_search(client, "ISTU", expresssion))[0]
            return Book(book, istu_library.id)

        tasks.append(task())

    return await asyncio.gather(*tasks)


async def book_retrieve(client: ClientSession, book_id: str) -> Book:
    database, mfn = split_book_id(book_id)
    library = (await LibraryDatabase.objects.filter(database=database).prefetch_related("library").afirst()).library
    book = await opac_book_retrieve(client, database, mfn)

    return Book(book, library.id)


async def book_retrieve_safe(client: ClientSession, book_id: str, library: Library | None = None) -> Book | None:
    try:
        database, _ = split_book_id(book_id)
        if library is not None and not await library.databases.filter(database=database).aexists():
            return None

        return await book_retrieve(client, book_id)
    except Exception:  # pylint: disable=broad-exception-caught # TODO: на самом деле, pylint здесь прав
        return None


async def book_retrieve_by_id(client: ClientSession, database: str, book_id: str) -> Book:
    library = (await LibraryDatabase.objects.filter(database=database).prefetch_related("library").afirst()).library
    book = await opac_book_retrieve_by_id(client, database, book_id)

    return Book(book, library.id)
