import pytest
from django.urls import reverse
from apps.accounts.models import EmailConfirmation
from django.contrib.auth.models import User


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser',
                                    password='12345')


# Test registration view

@pytest.mark.django_db
def test_register_user(client):
    """Тест регистрации пользователя."""
    response = client.post(reverse('register'), {
        'email': 'test2@example.com',
        'password1': 'test_password',
        'password2': 'test_password',
    })
    assert response.status_code == 302
    assert reverse('files_list') in response.url


@pytest.mark.django_db
def test_confirm_email(client, user):
    """Тест верификации почты и дальнейшего редиректа."""
    email_confirm = EmailConfirmation.objects.create(
        user=user, confirmation_code="testcode12345"
    )
    response = client.get(reverse('confirm_email',
                                  args=[email_confirm.confirmation_code]))
    assert response.status_code == 302
    assert reverse('files_list') in response.url
    email_confirm.refresh_from_db()
    assert email_confirm.confirmed
