from django.contrib import admin
from django.urls import path

from skypro_checking_projects.apps.accounts.views import registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration', registration, name='registration')
]
