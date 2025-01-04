from django import forms
from .models import User

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['room']  # Include other fields if necessary, e.g., email
