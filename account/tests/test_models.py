from django.test import TestCase
from django.contrib.auth.models import User
from account.models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        # Profile is created automatically by signal

    def test_profile_creation(self):
        """Test profile is created correctly"""
        profile = self.user.profile
        self.assertTrue(isinstance(profile, Profile))
        self.assertEqual(profile.__str__(), f'Profile of {self.user.username}')
        self.assertFalse(profile.is_admin)

    def test_make_admin(self):
        """Test make_admin method"""
        self.user.profile.make_admin()
        self.assertTrue(self.user.profile.is_admin)
        self.assertTrue(self.user.is_staff)

    def test_remove_admin(self):
        """Test remove_admin method"""
        self.user.profile.is_admin = True
        self.user.is_staff = True
        self.user.save()
        
        self.user.profile.remove_admin()
        self.assertFalse(self.user.profile.is_admin)
        self.assertFalse(self.user.is_staff)

    def test_profile_auto_creation(self):
        """Test profile is automatically created for new users"""
        new_user = User.objects.create_user(
            username='newuser',
            password='newpass123',
            email='new@example.com'
        )
        self.assertTrue(Profile.objects.filter(user=new_user).exists())
