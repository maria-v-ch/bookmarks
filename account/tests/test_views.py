from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountViewsTest(TestCase):
    """Test cases for account views."""

    def setUp(self) -> None:
        """Set up test data."""
        self.client = Client()
        
        # Create regular user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='adminpass123',
            email='admin@example.com'
        )
        self.admin_user.profile.make_admin()

    def test_login_view(self) -> None:
        """Test login functionality."""
        response = self.client.post(reverse('account:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_dashboard_access(self) -> None:
        """Test dashboard access restrictions."""
        # Anonymous user should be redirected to login
        response = self.client.get(reverse('account:dashboard'))
        self.assertEqual(response.status_code, 302)

        # Logged in user should access dashboard
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('account:dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_access(self) -> None:
        """Test admin dashboard access restrictions."""
        admin_url = reverse('account:admin_dashboard')

        # Regular user shouldn't access admin dashboard
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 302)

        # Admin user should access admin dashboard
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(admin_url)
        self.assertEqual(response.status_code, 200)

    def test_admin_management(self) -> None:
        """Test admin promotion and demotion."""
        self.client.login(username='adminuser', password='adminpass123')
        
        # Test promotion
        response = self.client.get(
            reverse('account:make_admin', args=[self.user.id])
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertTrue(self.user.profile.is_admin)

        # Test demotion
        response = self.client.get(
            reverse('account:remove_admin', args=[self.user.id])
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertFalse(self.user.profile.is_admin)
