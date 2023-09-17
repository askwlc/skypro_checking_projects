from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа в систему с использованием почты."""
    username = forms.EmailField(label="Email")
