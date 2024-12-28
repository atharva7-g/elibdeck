import datetime

from django import forms
from .models import Feedback, LibrarySettings, Book, Author
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

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'body', 'rating']
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': 'Enter the subject of your feedback',
                'class': 'form-control',
            }),
            'body': forms.Textarea(attrs={
                'placeholder': 'Write your detailed feedback here',
                'rows': 5,
                'class': 'form-control',
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

class LibrarySettingsForm(forms.ModelForm):
    class Meta:
        model = LibrarySettings
        fields = ['LATE_FEE', 'ISSUE_PERIOD']  # Fields to edit
        widgets = {
            'LATE_FEE': forms.NumberInput(attrs={'step': '0.01'}),  # Add step for decimal input
            'ISSUE_PERIOD': forms.NumberInput(attrs={'min': '1'}),  # Minimum value for issuing period
        }

class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'genre', 'isbn', 'cover_image']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UpdateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'genre', 'isbn']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }
