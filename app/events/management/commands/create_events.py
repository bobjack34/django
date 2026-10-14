"""
Ein Management Command zum Anlegen von Events

python manage.py create_events -n 200
"""

import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser

from events.factories import EventFactory


User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-n",
            "--number",
            type=int,
            required=True,
            help="Number of events that should be created",
        )

    def handle(self, *args, **options):
        user_list = User.objects.all()

        for _ in range(options.get("number", 5)):
            random_user = random.choice(user_list)
            event = EventFactory(author=random_user)
            print(f"Event wurde erstellt: {event} von {random_user}")
