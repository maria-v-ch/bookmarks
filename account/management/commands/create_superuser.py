from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Superuser already exists')
        else:
            username = settings.DJANGO_SUPERUSER_USERNAME
            email = settings.DJANGO_SUPERUSER_EMAIL
            password = settings.DJANGO_SUPERUSER_PASSWORD
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(f'Superuser {username} created successfully')
