from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
    """Обработка входа пользователя в систему."""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('files_list')


class CustomLogoutView(LogoutView):
    """Обработка выхода пользователя из системы."""
    next_page = 'login'


def register(request: HttpRequest) -> HttpResponse:
    """Обработка регистрации пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('files_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
