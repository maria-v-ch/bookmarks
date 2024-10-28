"""Application configuration for the account app."""

from django.apps import AppConfig


class AccountConfig(AppConfig):
    """Configuration class for the account application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = 'User Accounts'

    def ready(self) -> None:
        """Import signal handlers when Django is ready."""
        import account.signals  # noqa
