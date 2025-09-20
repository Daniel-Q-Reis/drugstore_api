from typing import Any
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = "Create a superuser"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--username", type=str, help="Username", default="admin")
        parser.add_argument(
            "--email", type=str, help="Email address", default="admin@example.com"
        )
        parser.add_argument("--password", type=str, help="Password", default="admin")

    def handle(self, *args: Any, **options: Any) -> None:
        User = get_user_model()
        if not User.objects.filter(username=options["username"]).exists():
            User.objects.create_superuser(
                username=options["username"],
                email=options["email"],
                password=options["password"],
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser {options["username"]} created successfully!'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Superuser {options["username"]} already exists.')
            )
