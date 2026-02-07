from django import forms
from django.core.validators import RegexValidator

from .models import User


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        min_length=8
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'user_type']

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        validator = RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*\d).+$',
            message=(
                'Password must contain at least one uppercase letter '
                'and one digit.'
            )
        )
        validator(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned_data
