from django import forms

class DataUploadForm(forms.Form):
    file = forms.FileField(
        label="Select a file",
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls',
        }),
        error_messages={
            'required': 'Please upload a file.',
            'invalid': 'The uploaded file is not valid.',
        }
    )
