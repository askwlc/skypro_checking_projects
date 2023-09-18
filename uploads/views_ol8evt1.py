from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.db import IntegrityError
import uuid
from decouple import config

from apps.accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import EmailConfirmation


class CustomLoginView(LoginView):
    """Обработка входа пользователя в систему."""
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('files_list')


class CustomLogoutView(LogoutView):
    """Обработка выхода пользователя из системы."""
    next_page = 'login'


def register(request: HttpRequest) -> HttpResponse:
    """Обработка регистрации пользователя."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = user.email
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('files_list')
            except IntegrityError:
                messages.error(request, 'Вы уже зарегистрированы.')
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def send_confirmation_mail(user):
    """Отправка сообщения для подтверждения эл.почты."""
    code = str(uuid.uuid4())
    EmailConfirmation.objects.create(user=user, confirmation_code=code)

    subject = 'Подтвердите адрес электронной почты.'
    message = f'Пожалуйста перейдите по ссылке для подтверждения адреса электронной почты:\n\nhttp://yourdomain.com{EmailConfirmation(user=user).get_absolute_url()}'
    from_email = config('DEFAULT_FROM_EMAIL')

    send_mail(subject, message, from_email, [user.email], fail_silently=False)


def confirm_email(request, confirmation_code):
    """Подтверждение эл.почты по ссылке в письме клиента."""
    try:
        email_confirm = EmailConfirmation.objects.get(confirmation_code=confirmation_code)
        if not email_confirm.confirmed:
            email_confirm.confirmed = True
            email_confirm.save()
            return render(request, 'email/confirmation_successful.html')
        else:
            return render(request,
                          'email/confirmation_already_done.html')
    except EmailConfirmation.DoesNotExist:
        return render(request, 'email/confirmation_error.html')
