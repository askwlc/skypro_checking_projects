import uuid

from decouple import config
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy

from apps.accounts.forms import (CustomAuthenticationForm,
                                 CustomUserCreationForm)

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
                login(request, user,
                      backend='django.contrib.auth.backends.ModelBackend')
                send_confirmation_mail(user, request)
                return redirect('files_list')
            except IntegrityError:
                messages.error(request, 'Вы уже зарегистрированы.')
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def send_confirmation_mail(user, request):
    """Отправка сообщения для подтверждения эл.почты."""
    code = str(uuid.uuid4())
    EmailConfirmation.objects.create(user=user, confirmation_code=code)

    subject = 'Подтвердите адрес электронной почты.'
    confirmation_url = reverse('confirm_email', args=[code])
    domain = request.get_host()
    message = f'Пожалуйста перейдите по ссылке для подтверждения адреса ' \
              f'электронной почты:\n\nhttp://{domain}{confirmation_url}'
    from_email = config('DEFAULT_FROM_EMAIL')

    send_mail(subject, message, from_email, [user.email], fail_silently=False)


def resend_verification_email(request):
    """Возможность повторной отправки ссылки верификации."""
    send_confirmation_mail(request.user, request)
    return HttpResponseRedirect(reverse('files_list'))


def confirm_email(request, confirmation_code):
    """Подтверждение эл.почты по ссылке в письме клиента."""
    try:
        email_confirm = EmailConfirmation.objects.get(
            confirmation_code=confirmation_code
        )
        if not email_confirm.confirmed:
            email_confirm.confirmed = True
            email_confirm.save()
            return redirect('files_list')
        else:
            return redirect('files_list')
    except EmailConfirmation.DoesNotExist:
        return render(request, 'confirmation_error.html')
