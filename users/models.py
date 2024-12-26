from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4

class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)

    if is_librarian:
        psrn = models.CharField(
            max_length=255, default=uuid4, primary_key=True, editable=False, unique=True)

    def __str__(self):
        return self.username
