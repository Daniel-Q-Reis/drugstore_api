from typing import Any

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    """
    Runs the initial setup for the project, including migrations,
    superuser creation, and optional data seeding.

    This command is idempotent and safe to run multiple times.
    """

    help = "Sets up the project with a single command."

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Add arguments to the command.
        """
        parser.add_argument(
            "--no-seed",
            action="store_false",
            dest="seed",
            help="Do not seed the database with sample data.",
        )
        parser.add_argument(
            "--no-superuser",
            action="store_false",
            dest="superuser",
            help="Do not create a superuser.",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        """
        Execute the setup commands.
        """
        self.stdout.write(self.style.SUCCESS("Starting project setup..."))

        # --- 1. Run Migrations ---
        self.stdout.write(self.style.HTTP_INFO("Running database migrations..."))
        try:
            call_command("migrate")
            self.stdout.write(self.style.SUCCESS("Migrations applied successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Migration failed: {e}"))
            return

        # --- 2. Create Superuser (if needed) ---
        if options["superuser"]:
            self.stdout.write(
                self.style.HTTP_INFO("Creating superuser if none exists...")
            )
            try:
                # Using your idempotent command
                call_command(
                    "createsuperuser_if_none_exists",
                    "--username",
                    "admin",
                    "--email",
                    "admin@example.com",
                    "--password",
                    "admin123",
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Superuser creation failed: {e}"))
                return

        # --- 3. Seed Database (if requested) ---
        # You were right, making this optional is the best approach.
        if options["seed"]:
            self.stdout.write(
                self.style.HTTP_INFO("Seeding database with sample data...")
            )
            try:
                call_command(
                    "seed_db",
                    "--brands",
                    50,
                    "--categories",
                    50,
                    "--products",
                    200,
                    "--stock-items",
                    400,
                    "--sales",
                    450,
                )
                self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Data seeding failed: {e}"))
                return

        self.stdout.write(self.style.SUCCESS("Project setup complete!"))
