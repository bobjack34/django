"""
conftest.py
Test-Fixtures für das gesamte Projekt
"""

import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from events.factories import EventFactory, CategoryFactory

User = get_user_model()


@pytest.fixture
def user(db):
    """Erzeuge einen normalen Testnutzer."""
    return User.objects.create_user(
        username="alice",
        password="abc123",
    )


@pytest.fixture
def other_user(db):
    """Erzeuge einen weiteren Testnutzer."""
    return User.objects.create_user(
        username="mallory",
        password="abc123",
    )


@pytest.fixture
def event(user):
    return EventFactory(
        author=user,
        name="Django Workshop",
    )


@pytest.fixture
def category(db):
    return CategoryFactory()


@pytest.fixture
def authenticated_client(client: Client, user: AbstractBaseUser) -> Client:
    """Erzeuge einen eingeloggten User-Client."""
    client.force_login(user)
    return client
