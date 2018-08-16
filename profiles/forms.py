from django import forms
from django.contrib.auth import get_user_model

from .models import Profile
from utils.validations import (
    validate_email,
    validate_email_absence,
    validate_email_exists,
    validate_password,
)

User = get_user_model()


class ProfileRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    initial = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')

    def clean_email(self):
        return validate_email(
            validate_email_absence(self.cleaned_data.get("email")),
        )

    def clean_password(self):
        return validate_password(
            initial=self.cleaned_data.get("initial"),
            confirm=self.cleaned_data.get("confirm"),
        )


class PasswordChangeForm(forms.Form):
    initial = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password(self):
        return validate_password(
            initial=self.cleaned_data.get("initial"),
            confirm=self.cleaned_data.get("confirm")
        )


class PasswordChangeRequestForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'example@me.com'})
    )

    def clean_email(self):
        return validate_email(
            validate_email_exists(self.cleaned_data.get("email"))
        )
