from datetime import timedelta

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.forms.models import model_to_dict

from events.models import Event, Category


@pytest.mark.django_db
def test_event_list(client: Client, event: Event):
    """Die Event-Liste ist erreichbar und verwendet das
    richtige Template. der client ist ein django-pytest fixture.
    event erzeugt implizit ein Event-Objekt für diesen Test.
    """
    url = reverse("events:event_list")
    response = client.get(url)

    assert response.status_code == 200
    assert event in response.context["object_list"]
    assert response.template_name == ["events/event_list.html"]


@pytest.mark.django_db
def test_event_create(
    authenticated_client: Client,
    user: AbstractBaseUser,
    category: Category,
):
    """Ein neuer, valider Event kann mit einem eingeloggten Userclient
    angelegt werden.
    authenticated_client ist ein eingeloggter User, category ist eine Katorie
    (beides aus conftest.py)
    """
    url = reverse("events:event_create")
    date = timezone.now() + timedelta(days=1)
    payload = {
        "name": "Python Workshop",
        "sub_title": "Alles rund um Python",
        "min_group": 5,
        "category": category.pk,
        "date": date,
    }
    response = authenticated_client.post(url, payload)
    created_event = Event.objects.get(name="Python Workshop")
    assert response.status_code == 302
    assert created_event.author == user
    assert created_event.category == category


@pytest.mark.django_db
def test_invalid_event_create(
    authenticated_client: Client,
    user: AbstractBaseUser,
    category: Category,
):
    """Ein neuer, invalider Event kann mit einem eingeloggten Userclient
    NICHT angelegt werden.
    """
    url = reverse("events:event_create")
    invalid_date = timezone.now() + timedelta(hours=1)
    payload = {
        "name": "Python Kurs",
        "sub_title": "Alles rund um Python",
        "min_group": 5,
        "category": category.pk,
        "date": invalid_date,
    }
    response = authenticated_client.post(url, payload)
    assert not Event.objects.filter(name="Python Kurs").exists()
    assert response.status_code == 200
    assert "date" in response.context["form"].errors


def test_event_update_forbidden_user(
    client: Client,
    other_user: AbstractBaseUser,
    event: Event,
):
    """Ein Event darf nicht von einem anderen User geändert werden."""
    url = reverse("events:event_update", args=(event.pk,))
    payload = model_to_dict(event, exclude=["id"])
    payload["name"] = "xyz"
    client.force_login(other_user)
    response = client.post(url, payload)

    assert response.status_code == 403
    assert not Event.objects.filter(name="xyz").exists()
    assert event.name == "Django Workshop"
