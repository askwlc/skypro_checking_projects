from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации пользователя."""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа в систему с использованием почты."""
    username = forms.EmailField(label="Email")

    def clean_username(self):
        """Проверка зарегистрирован ли email."""
        email = self.cleaned_data.get('username')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Вводимый email не зарегистрирован, "
                                        "пожалуйста зарегистрируйтесь.")

        return email