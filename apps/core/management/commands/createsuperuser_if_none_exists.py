from typing import Any
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    help = "Create a superuser if one does not exist"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--username", type=str, help="Superuser username")
        parser.add_argument("--email", type=str, help="Superuser email")
        parser.add_argument("--password", type=str, help="Superuser password")

    def handle(self, *args: Any, **options: Any) -> None:
        User = get_user_model()

        # Check if a superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING("Superuser already exists. Skipping creation.")
            )
            return

        # Get or set default values
        username = options.get("username") or "admin"
        email = options.get("email") or "admin@example.com"
        password = options.get("password") or "admin123"

        # Create the superuser
        User.objects.create_superuser(username=username, email=email, password=password)

        self.stdout.write(
            self.style.SUCCESS(f'Superuser "{username}" created successfully!')
        )
