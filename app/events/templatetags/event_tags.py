"""
Eigene Template-Tags und Filter für die Event App

Der has_group Filter prüft im Template, ob ein User Mitglied
einer Gruppe ist. Dieser Gruppenname wird dem Filter übergeben:

{% if request.user|has_group:"Moderatoren" %}
"""

from django import template
from django.contrib.auth.models import AbstractBaseUser

register = template.Library()


@register.filter("has_group")
def has_group(user: AbstractBaseUser, group_name: str):
    """True, wenn der User Mitglied der Gruppe ist."""
    return user.groups.filter(name=group_name).exists()
