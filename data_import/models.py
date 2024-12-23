from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    isbn = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
