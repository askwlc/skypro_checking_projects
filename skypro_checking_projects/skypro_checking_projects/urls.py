from django.contrib import admin
from django.urls import path

from apps.accounts.views import register, CustomLoginView, CustomLogoutView
from apps.files.views import FileUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('upload/', FileUploadView.as_view(), name='file_upload')
]
