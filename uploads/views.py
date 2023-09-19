from rest_framework import generics, status
from rest_framework.response import Response

from apps.files.tasks import check_file_flake8_task

from ..files.models import FileUpload
from .serializers import FileUploadDetailSerializer, FileUploadSerializer


class FileListCreateView(generics.ListCreateAPIView):
    """Получение списка файлов."""
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer


class FileRetrieveRecheckView(generics.RetrieveAPIView):
    """Получение информации о файле и повторная отправка на проверку."""
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadDetailSerializer

    def post(self, request, *args, **kwargs):
        file = self.get_object()

        if not file:
            return Response({
                "result": "failed",
                "message": "have no access to this file"
            }, status=status.HTTP_403_FORBIDDEN)

        file.is_new = True
        file.save()
        check_file_flake8_task.delay()

        return Response({"result": "ok", "message": "file under testing"},
                        status=status.HTTP_200_OK)
