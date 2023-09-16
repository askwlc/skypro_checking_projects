from django.contrib import admin
from django.urls import path

from apps.accounts.views import registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', registration, name='reg')
]
