from apps.accounts.views import CustomLoginView, CustomLogoutView, register, confirm_email
from apps.files.views import FileUploadView, FilesListView, FileDeleteView, FileUpdateView, file_results
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('files/', FilesListView.as_view(), name='files_list'),
    path('register/', register, name='register'),
    path('confirm-email/<str:confirmation_code>/', confirm_email, name='confirm_email'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('file_results/<int:file_id>/', file_results, name='file_results'),
    path('delete/<int:pk>/', FileDeleteView.as_view(), name='file_delete'),
    path('update/<int:pk>/', FileUpdateView.as_view(), name='file_update'),
    path('api/', include('apps.api.urls')),
]
