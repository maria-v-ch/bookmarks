"""Signal handlers for the account application."""

from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(
    sender, 
    instance: User, 
    created: bool, 
    **kwargs
) -> None:
    """Create a Profile instance when a new User is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(
    sender, 
    instance: User, 
    **kwargs
) -> None:
    """Ensure Profile exists and is saved when User is saved."""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
