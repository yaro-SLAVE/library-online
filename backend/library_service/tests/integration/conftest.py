"""Fixtures for integration tests"""
import pytest
from aiohttp import ClientSession
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from library_service.models.catalog import Library, LibraryDatabase


@pytest.fixture(scope="session", autouse=True)
def setup_database(django_db_setup, django_db_blocker):  # pylint: disable=unused-argument
    """Setup test database with minimal required data"""
    with django_db_blocker.unblock():
        # Create libraries if they don't exist
        library_inrtu, _ = Library.objects.get_or_create(
            id=1,
            defaults={"description": "ИРНИТУ", "address": "664074, Россия, г. Иркутск, ул. Лермонтова, 83."}
        )
        LibraryDatabase.objects.get_or_create(library=library_inrtu, database="ISTU")
        LibraryDatabase.objects.get_or_create(library=library_inrtu, database="NTD")

        library_zima, _ = Library.objects.get_or_create(
            id=3,
            defaults={"description": "ZIMA_LIB"}
        )
        LibraryDatabase.objects.get_or_create(library=library_zima, database="ZIMA")

        # Create test user
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username="test_integration_user",
            defaults={"first_name": "Integration", "last_name": "Test"}
        )
        if not user.has_usable_password():
            user.set_password("integration_test_pass")
            user.save()

        reader_group = Group.objects.get(name="Reader")
        user.groups.add(reader_group)


@pytest.fixture
async def client_session():
    """Provide aiohttp ClientSession for async tests"""
    async with ClientSession() as client:
        yield client
