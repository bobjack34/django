"""
Hier liegen Service Funktionen zur Verwaltung von Events (Beispiel)
"""

import logging

from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from events.models import Event

logger = logging.getLogger(__name__)


class CancelException(Exception):
    pass


def cancel_event(event: Event, user: AbstractBaseUser) -> Event:
    """einen Event canceln der nicht in Vergangenheit liegt."""
    if event.author != user:
        logger.warning(
            "User %s versucht den Event %s zu canceln, der ihm nicht gehört.",
            user,
            event,
        )
        raise CancelException("Dieser Vorgang ist nicht erlaubt.")

    if event.date <= timezone.now():
        raise CancelException(
            "Ein Event in der Vergangenheit darf nicht gecancelt werden."
        )
    event.is_active = False
    event.save(update_fields=["is_active"])

    logger.info("User %s hat den Event %s abgesagt.", user, event)

    return event
