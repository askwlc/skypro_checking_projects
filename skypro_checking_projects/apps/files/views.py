from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import FileUpload
from .forms import FileUploadForm
from .utils import check_file_flake8


class FileUploadView(CreateView):
    """Обработка загрузки файла для проверки."""
    model = FileUpload
    form_class = FileUploadForm
    template_name = 'upload.html'
    success_url = reverse_lazy('files_list')

    def form_valid(self, form):
        """Переопределение метода для проверки файла после загрузки."""
        response = super().form_valid(form)
        file_path = self.object.file.path
        check_result = check_file_flake8(file_path)

        return response
