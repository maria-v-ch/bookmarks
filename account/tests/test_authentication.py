"""Tests for authentication functionality."""

from django.test import TestCase
from django.contrib.auth.models import User
from account.authentication import EmailAuthBackend


class EmailAuthBackendTest(TestCase):
    """Test cases for email-based authentication backend."""

    def setUp(self) -> None:
        """Set up test data."""
        self.backend = EmailAuthBackend()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_authenticate_valid_credentials(self) -> None:
        """Test authentication with valid email and password."""
        authenticated_user = self.backend.authenticate(
            None,
            username='test@example.com',
            password='testpass123'
        )
        self.assertEqual(authenticated_user, self.user)

    def test_authenticate_invalid_password(self) -> None:
        """Test authentication with invalid password."""
        authenticated_user = self.backend.authenticate(
            None,
            username='test@example.com',
            password='wrongpass'
        )
        self.assertIsNone(authenticated_user)

    def test_authenticate_invalid_email(self) -> None:
        """Test authentication with non-existent email."""
        authenticated_user = self.backend.authenticate(
            None,
            username='nonexistent@example.com',
            password='testpass123'
        )
        self.assertIsNone(authenticated_user)

    def test_get_user_valid_id(self) -> None:
        """Test getting user by valid ID."""
        user = self.backend.get_user(self.user.id)
        self.assertEqual(user, self.user)

    def test_get_user_invalid_id(self) -> None:
        """Test getting user by invalid ID."""
        user = self.backend.get_user(999)
        self.assertIsNone(user)

    def test_multiple_users_same_email(self) -> None:
        """Test authentication when multiple users have the same email."""
        User.objects.create_user(
            username='testuser2',
            email='test@example.com',
            password='testpass123'
        )
        authenticated_user = self.backend.authenticate(
            None,
            username='test@example.com',
            password='testpass123'
        )
        self.assertIsNone(authenticated_user)
