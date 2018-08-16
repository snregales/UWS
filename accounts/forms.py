from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from utils.validations import (
    validate_email,
    validate_email_absence,
    validate_password,
)

User = get_user_model()


class UserBaseForm(forms.ModelForm):
    initial = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        return validate_email(
            email=validate_email_absence(self.cleaned_data.get("email"))
        )

    def clean_password(self):
        return validate_password(
            initial=self.cleaned_data.get("initial"),
            confirm=self.cleaned_data.get("confirm")
        )


class UserAdminCreationForm(UserBaseForm):
    """A form for creating new admin users. Includes all the required
    fields, plus a repeated password."""
    admin_alias = forms.CharField(
        label='Admin Alias',
        max_length=10,
        help_text='your admin name, example "kalonji" -> "admin-kalonji"',
        widget=forms.TextInput(
            attrs={'placeholder': 'kalonji'}
        )
    )

    def save(self, commit=True):
        super(UserAdminCreationForm, self).save(commit=False)
        self.cleaned_data.update({
            'password': self.cleaned_data['initial']
        })
        del self.cleaned_data['initial']
        del self.cleaned_data['confirm']
        user = User.objects.create_superuser(**self.cleaned_data)
        if commit:
            user.save()
        return user


class UserStaffCreationForm(UserBaseForm):
    staff_alias = forms.CharField(
        label='Staff Alias',
        max_length=10,
        help_text='your staff name, example "kalonji" -> "staff-kalonji"',
        widget=forms.TextInput(
            attrs={'placeholder': 'kalonji'}
        )
    )

    def save(self, commit=True):
        super(UserStaffCreationForm, self).save(commit=False)
        self.cleaned_data.update({
            'password': self.cleaned_data['initial']
        })
        del self.cleaned_data['initial']
        del self.cleaned_data['confirm']
        user = User.objects.create_staff(**self.cleaned_data)
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the account, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the account provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']
