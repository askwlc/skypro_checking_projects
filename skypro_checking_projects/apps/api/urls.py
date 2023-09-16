from django.urls import path
from .views import FileListCreateView, FileRetrieveRecheckView

urlpatterns = [
    path('files/', FileListCreateView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileRetrieveRecheckView.as_view(), name='file-detail-recheck'),
]
