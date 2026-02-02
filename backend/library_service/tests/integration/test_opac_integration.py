"""Integration tests for OPAC service.

These tests verify that the application can connect to and interact with
the real OPAC service at https://library.istu.edu/opac

Run with: pytest -m integration
"""
import pytest
from aiohttp import ClientSession
from django.test import Client

from library_service.opac.api.databases import opac_databases
from library_service.opac.api.scenarios import opac_scenarios
from library_service.opac.api.announces import opac_announces_list
from library_service.opac.api.book import opac_search


@pytest.mark.integration
@pytest.mark.asyncio
async def test_opac_databases_accessible(client_session: ClientSession):
    """Test that we can fetch databases list from real OPAC"""
    databases = await opac_databases(client_session)

    # Should have at least ISTU, NTD, ZIMA databases
    assert len(databases) >= 3

    db_names = [db.name for db in databases]
    assert "ISTU" in db_names
    assert "NTD" in db_names

    # Check structure
    for db in databases:
        assert hasattr(db, 'name')
        assert hasattr(db, 'order')
        assert isinstance(db.name, str)
        assert len(db.name) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_opac_scenarios_accessible(client_session: ClientSession):
    """Test that we can fetch search scenarios from real OPAC"""
    scenarios = await opac_scenarios(client_session, "ISTU")

    # Should have multiple search scenarios
    assert len(scenarios) > 0

    # Common scenarios should exist
    prefixes = [s.prefix for s in scenarios]
    assert "A=" in prefixes  # Author
    assert "T=" in prefixes  # Title

    # Check structure
    for scenario in scenarios:
        assert hasattr(scenario, 'prefix')
        assert hasattr(scenario, 'description')
        assert isinstance(scenario.prefix, str)
        assert len(scenario.prefix) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_opac_announces_accessible(client_session: ClientSession):
    """Test that we can fetch announcements from real OPAC"""
    announces = await opac_announces_list(client_session)

    # Should have at least some announcements
    assert len(announces) > 0

    # Check structure
    for announce in announces:
        assert hasattr(announce, 'link')
        assert isinstance(announce.link, str)
        assert 'opac' in announce.link.lower()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_opac_search_books(client_session: ClientSession):
    """Test that we can search for books in real OPAC"""
    # Search for all books (limited by OPAC)
    books = await opac_search(client_session, "ISTU", "T=$")

    # Should return some books
    assert len(books) > 0

    # Check structure of first book
    first_book = books[0]
    assert hasattr(first_book, 'id')
    assert hasattr(first_book, 'info')
    assert hasattr(first_book, 'exemplars')

    # ID should follow ISTU/number format
    assert '/' in first_book.id or '_' in first_book.id

    # Info should have basic fields
    assert hasattr(first_book.info, 'title')
    assert hasattr(first_book.info, 'author')


@pytest.mark.integration
@pytest.mark.django_db
def test_library_api_returns_data(client: Client):
    """Test that /api/library/ returns real data from database"""
    response = client.get("/api/library/")

    assert response.status_code == 200
    libraries = response.json()

    # Should have at least one library
    assert len(libraries) > 0

    # Check structure
    for library in libraries:
        assert "id" in library
        assert "description" in library
        assert "address" in library


@pytest.mark.integration
@pytest.mark.django_db
def test_scenario_api_returns_real_opac_data(client: Client):
    """Test that /api/scenario/ fetches data from real OPAC"""
    response = client.get("/api/scenario/")

    assert response.status_code == 200
    scenarios = response.json()

    # Should have many scenarios from real OPAC
    assert len(scenarios) > 10

    # Should include common search prefixes
    prefixes = [s["prefix"] for s in scenarios]
    assert "A=" in prefixes
    assert "T=" in prefixes
    assert "IN=" in prefixes


@pytest.mark.integration
@pytest.mark.django_db
def test_book_announcement_api_accessible(client: Client):
    """Test that /api/book/announcement/ works with real OPAC"""
    response = client.get("/api/book/announcement/")

    assert response.status_code == 200
    announcements = response.json()

    # Should have at least one announcement
    assert len(announcements) > 0

    # Check structure
    for announcement in announcements:
        assert "id" in announcement
        assert isinstance(announcement["id"], str)


@pytest.mark.integration
@pytest.mark.django_db
def test_book_search_api_accessible(client: Client):
    """Test that /api/book/ search works with real OPAC"""
    response = client.get("/api/book/", {"expression": "T=$"})

    assert response.status_code == 200
    books = response.json()

    # Should return books from real OPAC
    assert len(books) > 0

    # Check structure
    first_book = books[0]
    assert "id" in first_book
    assert "info" in first_book
    assert "exemplars" in first_book
