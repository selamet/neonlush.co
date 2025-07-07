from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for the custom User model."""

    def test_create_user_with_phone_number(self):
        """Test creating a user with a phone number."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            phone_number='+1234567890'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertTrue(user.check_password('testpassword'))

    def test_create_user_without_phone_number(self):
        """Test creating a user without a phone number."""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword'
        )
        
        self.assertEqual(user.username, 'testuser2')
        self.assertEqual(user.email, 'test2@example.com')
        self.assertIsNone(user.phone_number)

    def test_user_str_representation(self):
        """Test the string representation of the user."""
        user = User.objects.create_user(
            username='testuser3',
            phone_number='123-456-7890'
        )
        
        self.assertEqual(str(user), 'testuser3')
