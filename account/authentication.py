"""Custom authentication backends for the account application."""

from account.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from typing import Optional, Union

User = get_user_model()


class EmailAuthBackend(BaseBackend):
    """Authentication backend that allows users to log in with email."""

    def authenticate(
        self, 
        request, 
        username: str = None, 
        password: str = None
    ) -> Optional[User]:
        """Authenticate a user based on email address."""
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by their ID."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    """
    Create user profile for social authentication
    """
    Profile.objects.get_or_create(user=user)
