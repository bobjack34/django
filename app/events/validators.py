from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_date(value: datetime, hours: int) -> None:
    """Prüfe, ob ein Datum in der Verhangenheit liegt.
    Diese Funktion muss mit functools.partial aufgerufen werden,
    da Validierungsfunktionen immer nur einen Parameter erlauben (
    der aktuelle Feldwert).
    """
    if value < timezone.now() + timedelta(hours=hours):
        msg = f"Zeitpunkt darf nicht in der Verganheit liegen (+{hours} hour)."
        raise ValidationError(msg)
