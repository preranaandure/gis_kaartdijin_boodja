"""Kaartdijin Boodja Accounts Django Application Configuration."""


# Third-Party
from django import apps


class AccountsConfig(apps.AppConfig):
    """Accounts Application Configuration."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "govapp.apps.accounts"

    def ready(self) -> None:
        import govapp.apps.accounts.signals
        # Import the checks module to register the system checks.
        # The checks are automatically registered with Django's check framework
        # when this module is imported, thanks to the @register decorator.
        from . import checks

        return super().ready()