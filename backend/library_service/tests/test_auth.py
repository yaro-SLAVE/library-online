from django.http import HttpHeaders
from django.test import Client
import pytest


def authorize(client: Client, username: str = "user", password: str = "1235") -> tuple[str, str]:
    response = client.post("/api/auth/login/", {"username": username, "password": password})
    json = response.json()
    client.defaults.update(HttpHeaders.to_wsgi_names({"Authorization": f'Bearer {json["access"]}'}))
    return json["access"], json["refresh"]


@pytest.mark.django_db
def test_normal_auth(client: Client):
    authorize(client)
    response = client.get("/api/profile/self-info/")
    json = response.json()
    assert json == {"username": "user", "first_name": "Alan", "last_name": "Turing", "groups": ["Reader"]}


@pytest.mark.django_db
def test_normal_auth_wrong(client: Client):
    response = client.post("/api/auth/login/", {"username": "user", "password": "12345"})
    assert response.status_code == 401

    response = client.post("/api/auth/login/", {"username": "alan", "password": "1234"})
    assert response.status_code == 401


# TODO: test_bitrix_auth


@pytest.mark.django_db
def test_refresh(client: Client):
    _, refresh = authorize(client)

    # Refresh the token
    response = client.post("/api/auth/refresh/", {"refresh": refresh})
    json = response.json()
    access: str = json["access"]
    old_refresh = refresh
    refresh: str = json["refresh"]

    # Check that the old refresh token doesn't work
    response = client.post("/api/auth/refresh/", {"refresh": old_refresh})
    assert response.status_code == 401

    # Get profile info with the new token
    response = client.get("/api/profile/self-info/", headers={"Authorization": f"Bearer {access}"})
    json = response.json()
    assert json == {"username": "user", "first_name": "Alan", "last_name": "Turing", "groups": ["Reader"]}


@pytest.mark.django_db
def test_logout(client: Client):
    _, refresh = authorize(client)

    # Logout
    response = client.post("/api/auth/logout/", {"refresh": refresh})
    assert response.status_code == 200

    # Check that the refresh token doesn't work anymore
    response = client.post("/api/auth/logout/", {"refresh": refresh})
    assert response.status_code == 401
