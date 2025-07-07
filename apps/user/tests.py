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


# apps/user/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User


class UserAPITests(APITestCase):
    def test_register_valid(self):
        url = reverse('api_user_register')
        data = {'email': 'test@example.com', 'password': 'StrongPass123!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_register_invalid_email(self):
        User.objects.create_user(username='test@example.com', email='test@example.com', password='StrongPass123!')
        url = reverse('api_user_register')
        data = {'email': 'test@example.com', 'password': 'StrongPass123!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_login_valid(self):
        User.objects.create_user(username='test@example.com', email='test@example.com', password='StrongPass123!')
        url = reverse('api_user_login')
        data = {'email': 'test@example.com', 'password': 'StrongPass123!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class UserFormTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_form_register(self):
        url = reverse('user_register_form')
        data = {'email': 'formuser@example.com', 'password': 'StrongPass123!'}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, '/dashboard/')
        self.assertTrue(User.objects.filter(email='formuser@example.com').exists())
        session = self.client.session
        self.assertIn('jwt_access', session)

    def test_form_login(self):
        User.objects.create_user(username='formlogin@example.com', email='formlogin@example.com',
                                 password='StrongPass123!')
        url = reverse('user_login_form')
        data = {'email': 'formlogin@example.com', 'password': 'StrongPass123!'}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, '/dashboard/')
        session = self.client.session
        self.assertIn('jwt_access', session)
