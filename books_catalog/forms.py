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
        fields = ['subject', 'body']
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

class BookRatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ['value']
        widgets = {
            'value': forms.RadioSelect(choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)])
        }

    # def __init__(self, *args, **kwargs):
        # self.book = kwargs.pop('book')
        # super().__init__(*args, **kwargs)

        # self.fields['value'].label = None


    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     if not BorrowingHistory.objects.filter(user=self.instance.user, book=self.book).exists():
    #         raise forms.ValidationError('You can only rate a book you have borrowed.')
    #
    #     return cleaned_data