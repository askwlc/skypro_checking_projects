from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def registration(request: HttpRequest) -> HttpResponse:
    """Обработка регистрации пользователя."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('files_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})
