# apps/core/apps.py

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"

    def ready(self) -> None:
        """
        Overrides the default admin index template with our custom dashboard.
        This method is called once the app registry is fully populated.
        """
        # This import is placed here to avoid circular import issues during startup.
        from django.contrib import admin

        admin.site.index_template = "admin/index.html"
