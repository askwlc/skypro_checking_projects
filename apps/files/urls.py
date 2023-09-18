from django.urls import path

from .views import (FileDeleteView, FileResultsView, FilesListView,
                    FileUpdateView, FileUploadView)

urlpatterns = [
    path('files/', FilesListView.as_view(), name='files_list'),
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('file_results/<int:pk>/',
         FileResultsView.as_view(), name='file_results'),
    path('delete/<int:pk>/', FileDeleteView.as_view(), name='file_delete'),
    path('update/<int:pk>/', FileUpdateView.as_view(), name='file_update'),
]
