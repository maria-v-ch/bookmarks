"""Models for the account application."""

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    """User profile model extending the base User model.
    
    Attributes:
        user (User): One-to-one relationship with Django User model
        is_admin (bool): Flag indicating if user has admin privileges
    """
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    is_admin = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return string representation of Profile."""
        return f'Profile of {self.user.username}'

    def make_admin(self) -> None:
        """Grant admin privileges to user."""
        if not self.is_admin:
            self.is_admin = True
            self.user.is_staff = True
            self.user.save()
            self.save()

    def remove_admin(self) -> None:
        """Remove admin privileges from user."""
        if self.is_admin:
            self.is_admin = False
            self.user.is_staff = False
            self.user.save()
            self.save()
