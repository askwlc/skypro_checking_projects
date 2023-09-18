import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.files.models import FileUpload


@pytest.mark.django_db
class TestFileViews:

    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_file_list_view(self):
        """Тест отображения списка файлов."""
        FileUpload.objects.create(file="file1.txt", user=self.user)
        FileUpload.objects.create(file="file2.txt", user=self.user)
        url = reverse('file-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_file_retrieve(self):
        """Тест обновления файла."""
        test_user = User.objects.get(username='testuser')
        file = FileUpload.objects.create(file="file4.txt", user=test_user)
        url = reverse('file-detail-recheck', args=[file.id])
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['filename'] == 'file4.txt'

    def test_file_recheck(self):
        """Тест повторной проверки файла."""
        test_user = User.objects.get(username='testuser')
        file = FileUpload.objects.create(user=test_user, file="file5.txt")
        url = reverse('file-detail-recheck', args=[file.id])
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'file under testing'
