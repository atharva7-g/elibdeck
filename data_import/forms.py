from django import forms

class DataUploadForm(forms.Form):
    file = forms.FileField()