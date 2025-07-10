from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with additional phone number and tag fields."""
    
    # Tag choices for user categorization
    TAG_CHOICES = [
        (1, 'Regular'),
        (2, 'Premium'),
        (3, 'VIP'),
        (4, 'Admin'),
    ]
    
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="User's phone number"
    )
    
    tag = models.PositiveSmallIntegerField(
        choices=TAG_CHOICES,
        default=1,
        help_text="User category tag"
    )

    def __str__(self):
        return self.username
