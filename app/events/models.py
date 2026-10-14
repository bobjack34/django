from functools import partial

from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

from .validators import validate_date

User = get_user_model()


class Category(models.Model):
    """Eine Kategorie für einen Event."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, unique=True)  # varchar100
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    """Der Event, der auf einen bestimmten Zeitpunkt terminiert ist."""

    class Group(models.IntegerChoices):
        BIG = 10, "große Gruppe"
        MEDIUM = 5, "kleine Gruppe"
        SMALL = 2, "sehr kleine Gruppe"
        UNLIMITED = 0, "kein Limit"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events",  # bob.events
    )
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
        ],
    )
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(
        validators=[
            partial(validate_date, hours=2),
        ],
    )
    sub_title = models.CharField(max_length=200, null=True, blank=True)
    min_group = models.PositiveIntegerField(
        choices=Group.choices,
        default=Group.UNLIMITED,
    )
    # sport.events
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events",  # Related Manager
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]  # generell absteigend sortierten
        verbose_name = "Ereignis"
        verbose_name_plural = "Ereignisse"

    @property
    def related_events(self):
        """All events in same Category with same min group size"""
        related_events = Event.objects.filter(
            min_group__exact=self.min_group, category=self.category
        )
        return related_events.exclude(pk=self.id)[:5]

    def __str__(self) -> str:
        return self.name
