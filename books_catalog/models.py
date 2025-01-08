from django.db import models
from django.db.models import UniqueConstraint, Avg, Count
from django.db.models.functions import Lower
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import AbstractUser
import uuid

from elibdeck.settings import MEDIA_ROOT
import os


# Create your models here.

class LibrarySettings(models.Model):
    LATE_FEE = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    ISSUE_PERIOD = models.PositiveIntegerField(default=20, help_text="Number of days a book can be issued for")

    # def save(self, *args, **kwargs):
    #     if not self.pk and LibrarySettings.objects.exists():
    #         raise ValidationError('There can be only one LibrarySettings instance')
    #     return super(LibrarySettings, self).save(*args, **kwargs)
    #
    @classmethod
    def get_settings(cls):
        return cls.objects.first() or cls.objects.create(LATE_FEE=5.00, ISSUE_PERIOD=20)

    def __str__(self):
        return "Library Settings"


# def get_library_settings():
#     return LibrarySettings.get_settings()

class Genre(models.Model):
    """Model for genre of a book."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Fantasy, Sci-Fi, Adventure, etc.), case-insensitive"
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_case_insensitive_unique',
                violation_error_message="Genre already exists (case insensitive match)"
            ),
        ]


class Book(models.Model):
    """Model representing a book."""
    title = models.CharField(max_length=255, blank=True, null=True, help_text='Title of book')

    # Try to have a Many-to-Many-Field thing for authors. 
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)

    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book.", blank=True,
                               null=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 character ISBN', blank=True, null=True)

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book.')
    cover_image = models.ImageField(upload_to='covers', blank=True, null=True)
    publication_date = models.IntegerField(blank=True, null=True, help_text='Year of publication')

    borrowers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="borrowed_books")

    def average_rating(self):
        average_ratings = self.ratings.aggregate(Avg('value'))
        return average_ratings['value__avg'] or 0

    def num_ratings(self):
        # Calculate the number of ratings
        return self.ratings.aggregate(Count('value'))['value__count'] or 0

    class Meta:
        ordering = ['title', '-publication_date']

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('books_catalog:book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific physical copy of a book."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200, blank=True, null=True)
    due_date = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    total_late_fee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_date']
        permissions = (("can_mark_returned", "Set book as returned"),)

    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_date and date.today() > self.due_date)

    @property
    def overdue_by(self):
        if self.is_overdue and self.status == 'o':
            return (date.today() - self.due_date).days
        return 0

    @property
    def late_fee(self):
        """Calculate late fees."""
        settings = LibrarySettings.get_settings()
        return self.overdue_by * settings.LATE_FEE

    def save(self, *args, **kwargs):
        """Override save to update the total late fee automatically when saving."""
        self.total_late_fee = self.late_fee  # Automatically set total late fee
        super().save(*args, **kwargs)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('books_catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class Language(models.Model):
    """Model representing a language."""

    name = models.CharField(max_length=200, unique=True, help_text="Enter book's natural language.")

    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_case_insensitive_unique',
                violation_error_message="Language already exists (case insensitive match)"
            ),
        ]


class BorrowingHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bookinst = models.ForeignKey(BookInstance, on_delete=models.CASCADE, null=True, blank=True)
    borrowed_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.bookinst.book.title} on {self.return_date}"

    @property
    def is_returned(self):
        return self.return_date is not None


class PortalFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='feedback_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.subject} - {self.user}'

class BookRating(models.Model):
    book = models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.IntegerField()  # Value between 1 and 5

    # def clean(self):
    #     if not BorrowingHistory.objects.filter(user=self.user, book=self.book).exists():
    #         raise ValidationError('You can only rate a book you have borrowed.')
    #
    # def save(self, *args, **kwargs):
    #     self.clean()
    #     super().save(*args, **kwargs)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f'{self.user} rated {self.book.title} - {self.value}'