from rest_framework import generics, status
from rest_framework.response import Response
from ..files.models import FileUpload
from .serializers import FileUploadSerializer, FileUploadDetailSerializer


class FileListCreateView(generics.ListCreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer


class FileRetrieveRecheckView(generics.RetrieveAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadDetailSerializer

    def post(self, request, *args, **kwargs):
        file = self.get_object()

        if not file:
            return Response({
                "result": "failed",
                "message": "have no access to this file"
            }, status=status.HTTP_403_FORBIDDEN)

        return Response({"result": "ok", "message": "file under testing"}, status=status.HTTP_200_OK)
