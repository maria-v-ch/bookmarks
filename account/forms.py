"""Forms for the account application."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """Form for user login."""
    
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """Form for user registration with password confirmation."""
    
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text=' at least 8 characters long.'
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput,
        help_text=' same password as before, just for verification.'
    )
    email = forms.EmailField(
        required=True,
        help_text=' enter a valid email address - it will be used for account verification.'
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']
        help_texts = {
            'username': ' 150 characters or fewer, containing letters, digits and @/./+/-/_ only.',
        }

    def clean_password2(self) -> str:
        """Validate that both passwords match."""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']
    
    def clean_email(self) -> str:
        """Validate email uniqueness."""
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


class UserEditForm(forms.ModelForm):
    """Form for editing user profile."""
    
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self) -> str:
        """Validate email uniqueness excluding current user."""
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data
