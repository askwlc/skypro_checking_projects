from apps.accounts.views import CustomLoginView, CustomLogoutView, register
from apps.files.views import FileUploadView
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('upload/', FileUploadView.as_view(), name='file_upload')
]
