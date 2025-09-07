from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from apps.user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Fields:
        email (str): The user's email address.
        password (str): The user's password (write-only).

    Methods:
        validate_email: Ensures the email is unique.
        validate_password: Validates the password using Django's validators.
        create: Creates and returns a new User instance.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_email(self, value: str) -> str:
        """
        Validate that the email does not already exist.

        Args:
            value (str): The email to validate.

        Returns:
            str: The validated email.

        Raises:
            serializers.ValidationError: If the email already exists.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value: str) -> str:
        """
        Validate the password using Django's password validators.

        Args:
            value (str): The password to validate.

        Returns:
            str: The validated password.

        Raises:
            serializers.ValidationError: If the password is invalid.
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data: dict) -> User:
        """
        Create and return a new User instance.

        Args:
            validated_data (dict): The validated data.

        Returns:
            User: The created user instance.
        """
        user = User(
            username=validated_data['email'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Fields:
        email (str): The user's email address.
        password (str): The user's password (write-only).
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
