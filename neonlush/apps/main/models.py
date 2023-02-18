from django.db import models

from neonlush.core.models import BaseModel


# Create your models here.

class NotifyMe(BaseModel):
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.email
