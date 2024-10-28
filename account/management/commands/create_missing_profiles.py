"""Management command to create missing user profiles."""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.models import Profile

User = get_user_model()


class Command(BaseCommand):
    """Command to create profiles for users that don't have one."""
    
    help = 'Creates missing user profiles'

    def handle(self, *args, **options) -> None:
        """Execute the command."""
        users_without_profile = User.objects.filter(profile__isnull=True)
        
        for user in users_without_profile:
            Profile.objects.create(user=user)
            self.stdout.write(
                self.style.SUCCESS(f'Created profile for user: {user.username}')
            )
