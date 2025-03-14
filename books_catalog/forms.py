import datetime

from django import forms
from .models import LibrarySettings, Book, Author, PortalFeedback, BookRating, BorrowingHistory
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data_date = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data_date < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data_date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data_date


class PortalFeedbackForm(forms.ModelForm):
    class Meta:
        model = PortalFeedback
        fields = ['subject', 'body', 'image']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your feedback here...'}),
        }


class LibrarySettingsForm(forms.ModelForm):
    class Meta:
        model = LibrarySettings
        fields = ['LATE_FEE', 'ISSUE_PERIOD']  # Fields to edit
        widgets = {
            'LATE_FEE': forms.NumberInput(attrs={'step': '0.5'}),  # Add step for decimal input
            'ISSUE_PERIOD': forms.NumberInput(attrs={'min': '1'}),  # Minimum value for issuing period
        }
        labels = {
            'LATE_FEE': 'Late Fee',
            'ISSUE_PERIOD': 'Issue Period',
        }


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']


class AddBookForm(forms.ModelForm):
    available_copies = forms.IntegerField(min_value=1, initial=1, label="Number of Copies")

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'genre', 'isbn', 'cover_image', 'available_copies']
        widgets = {
            'publication_date': forms.NumberInput(attrs={'min': '1000', 'max': '9999'})
        }
        labels = {
            'publication_date': 'Publication Year',  # Update the label here
        }


class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'genre', 'isbn', 'cover_image']
        widgets = {
            'publication_date': forms.NumberInput(attrs={'min': '1000', 'max': '9999'})
        }
        labels = {
            'publication_date': 'Publication Year',  # Update the label here
        }


class BookRatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ['value']
        widgets = {
            'value': forms.RadioSelect(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)])
        }
