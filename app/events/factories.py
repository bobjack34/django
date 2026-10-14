from datetime import timedelta

import factory
from django.utils import timezone

from events import models

categories = [
    "Sports",
    "Talk",
    "Cooking",
    "Freetime",
    "Hiking",
    "Movies",
    "Travelling",
    "Science",
    "Arts",
    "Pets",
    "Music",
    "Wellness",
]


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Category
        django_get_or_create = ("name",)

    name = factory.Iterator(categories)
    sub_title = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=2)


class EventFactory(factory.django.DjangoModelFactory):
    """Erzeugt Events mit übergebenem User-Objekt als Author.

    event = EventFactory(author=user)
    """

    class Meta:
        model = models.Event

    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("sentence")
    sub_title = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=20)
    min_group = factory.Faker("random_element", elements=models.Event.Group)

    date = factory.Faker(
        "date_time_between",
        start_date=timezone.now() + timedelta(days=1),
        end_date=timezone.now() + timedelta(days=60),
        tzinfo=timezone.get_current_timezone(),
    )
