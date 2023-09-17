from apps.accounts.views import CustomLoginView, CustomLogoutView, register
from apps.files.views import FileUploadView, FilesListView, FileDeleteView, FileUpdateView
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', FilesListView.as_view(), name='files_list'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('delete/<int:pk>/', FileDeleteView.as_view(), name='file_delete'),
    path('update/<int:pk>/', FileUpdateView.as_view(), name='file_update'),
    path('api/', include('apps.api.urls')),
]
