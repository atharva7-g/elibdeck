from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from books_catalog.models import BookInstance

class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)
    psrn = models.CharField(
        max_length=255, default=uuid4, primary_key=True, editable=False, unique=True)
    room = models.CharField(max_length=10, default="No hostel.")

    def __str__(self):
        return self.username
