from io import StringIO
from django.core.management import call_command
from django.test import TestCase
from django.contrib.auth import get_user_model
from account.models import Profile

User = get_user_model()


class CommandsTestCase(TestCase):
    """Test cases for custom management commands."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_create_missing_profiles(self) -> None:
        """Test create_missing_profiles command."""
        # Delete profile if exists
        Profile.objects.filter(user=self.user).delete()
        
        out = StringIO()
        call_command('create_missing_profiles', stdout=out)
        
        # Check if profile was created
        self.assertTrue(
            Profile.objects.filter(user=self.user).exists()
        )
        self.assertIn('Created profile for user: testuser', out.getvalue())

    def test_create_missing_profiles_no_missing(self) -> None:
        """Test command when all users have profiles."""
        out = StringIO()
        call_command('create_missing_profiles', stdout=out)
        
        # Output should be empty as no profiles were created
        self.assertEqual('', out.getvalue().strip())
