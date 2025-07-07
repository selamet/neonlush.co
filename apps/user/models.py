from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with additional phone number field."""
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="User's phone number"
    )

    def __str__(self):
        return self.username
