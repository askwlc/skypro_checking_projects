from django.contrib import admin
from django.urls import path, include

from apps.accounts.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('files/', include('apps.files.urls')),
    path('api/', include('apps.api.urls')),
]
