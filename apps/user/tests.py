from __future__ import annotations

from typing import Dict, Any
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for the custom User model."""

    def test_create_user_with_phone_number(self) -> None:
        """
        Test creating a user with a phone number.
        
        Ensures that the User model can be created with all fields
        and that the phone number is properly stored.
        """
        user: User = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            phone_number='+1234567890'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertTrue(user.check_password('testpassword'))

    def test_create_user_without_phone_number(self) -> None:
        """
        Test creating a user without a phone number.
        
        Ensures that the phone number field is optional and
        defaults to None when not provided.
        """
        user: User = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpassword'
        )

        self.assertEqual(user.username, 'testuser2')
        self.assertEqual(user.email, 'test2@example.com')
        self.assertIsNone(user.phone_number)

    def test_user_str_representation(self) -> None:
        """
        Test the string representation of the user.
        
        Verifies that the __str__ method returns the username.
        """
        user: User = User.objects.create_user(
            username='testuser3',
            phone_number='123-456-7890'
        )

        self.assertEqual(str(user), 'testuser3')


class RegisterAPIViewTest(APITestCase):
    """Test cases for the RegisterAPIView."""

    def setUp(self) -> None:
        """Set up test data before each test method."""
        self.register_url: str = reverse('api_user_register')
        self.valid_data: Dict[str, str] = {
            'email': 'test@example.com',
            'password': 'StrongPass123!'
        }

    def test_register_success(self) -> None:
        """
        Test successful user registration.
        
        Ensures that a valid registration request returns JWT tokens
        and creates a new user in the database.
        """
        response: Response = self.client.post(
            self.register_url, 
            self.valid_data, 
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_register_duplicate_email(self) -> None:
        """
        Test registration with duplicate email.
        
        Ensures that attempting to register with an already existing
        email returns a validation error.
        """
        User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='StrongPass123!'
        )

        response: Response = self.client.post(
            self.register_url,
            self.valid_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_weak_password(self) -> None:
        """
        Test registration with weak password.
        
        Ensures that weak passwords are rejected with appropriate
        validation errors.
        """
        weak_password_data: Dict[str, str] = {
            'email': 'test@example.com',
            'password': '123'
        }

        response: Response = self.client.post(
            self.register_url,
            weak_password_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_missing_email(self) -> None:
        """
        Test registration with missing email field.
        
        Ensures that requests without email field are rejected.
        """
        incomplete_data: Dict[str, str] = {
            'password': 'StrongPass123!'
        }

        response: Response = self.client.post(
            self.register_url,
            incomplete_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_missing_password(self) -> None:
        """
        Test registration with missing password field.
        
        Ensures that requests without password field are rejected.
        """
        incomplete_data: Dict[str, str] = {
            'email': 'test@example.com'
        }

        response: Response = self.client.post(
            self.register_url,
            incomplete_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_register_invalid_email_format(self) -> None:
        """
        Test registration with invalid email format.
        
        Ensures that malformed email addresses are rejected.
        """
        invalid_email_data: Dict[str, str] = {
            'email': 'invalid-email',
            'password': 'StrongPass123!'
        }

        response: Response = self.client.post(
            self.register_url,
            invalid_email_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class LoginAPIViewTest(APITestCase):
    """Test cases for the LoginAPIView."""

    def setUp(self) -> None:
        """Set up test data before each test method."""
        self.login_url: str = reverse('api_user_login')
        self.test_email: str = 'test@example.com'
        self.test_password: str = 'StrongPass123!'
        
        # Create a test user for login tests
        self.test_user: User = User.objects.create_user(
            username=self.test_email,
            email=self.test_email,
            password=self.test_password
        )

    def test_login_success(self) -> None:
        """
        Test successful user login.
        
        Ensures that valid credentials return JWT tokens.
        """
        login_data: Dict[str, str] = {
            'email': self.test_email,
            'password': self.test_password
        }

        response: Response = self.client.post(
            self.login_url,
            login_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_email(self) -> None:
        """
        Test login with non-existent email.
        
        Ensures that login attempts with non-existent email
        return unauthorized status.
        """
        invalid_login_data: Dict[str, str] = {
            'email': 'nonexistent@example.com',
            'password': self.test_password
        }

        response: Response = self.client.post(
            self.login_url,
            invalid_login_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_login_wrong_password(self) -> None:
        """
        Test login with incorrect password.
        
        Ensures that login attempts with wrong password
        return unauthorized status.
        """
        wrong_password_data: Dict[str, str] = {
            'email': self.test_email,
            'password': 'WrongPassword123!'
        }

        response: Response = self.client.post(
            self.login_url,
            wrong_password_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)

    def test_login_missing_email(self) -> None:
        """
        Test login with missing email field.
        
        Ensures that requests without email field are rejected.
        """
        incomplete_data: Dict[str, str] = {
            'password': self.test_password
        }

        response: Response = self.client.post(
            self.login_url,
            incomplete_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_login_missing_password(self) -> None:
        """
        Test login with missing password field.
        
        Ensures that requests without password field are rejected.
        """
        incomplete_data: Dict[str, str] = {
            'email': self.test_email
        }

        response: Response = self.client.post(
            self.login_url,
            incomplete_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_invalid_email_format(self) -> None:
        """
        Test login with invalid email format.
        
        Ensures that malformed email addresses are rejected.
        """
        invalid_email_data: Dict[str, str] = {
            'email': 'invalid-email',
            'password': self.test_password
        }

        response: Response = self.client.post(
            self.login_url,
            invalid_email_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)