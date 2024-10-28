"""Tests for form functionality."""

from django.test import TestCase
from django.contrib.auth.models import User
from account.forms import UserRegistrationForm, UserEditForm


class FormsTest(TestCase):
    """Test cases for user-related forms."""

    def setUp(self) -> None:
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

    def test_registration_form(self) -> None:
        """Test user registration form with valid data."""
        form_data = {
            'username': 'newuser',
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'new@example.com',
            'first_name': 'Test'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_password_mismatch(self) -> None:
        """Test password validation in registration form."""
        form_data = {
            'username': 'newuser',
            'password': 'pass123',
            'password2': 'pass456',
            'email': 'new@example.com'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_edit_form(self) -> None:
        """Test user edit form with valid data."""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        }
        form = UserEditForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_form_duplicate_email(self) -> None:
        """Test email uniqueness validation in edit form."""
        User.objects.create_user(
            username='another',
            password='pass123',
            email='another@example.com'
        )
        
        form_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'another@example.com'  # Try to use existing email
        }
        form = UserEditForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
