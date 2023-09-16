from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import FileUploadForm
from .models import FileUpload
from .tasks import check_files


class FileUploadView(CreateView):
    """Обработка загрузки файла для проверки."""
    model = FileUpload
    form_class = FileUploadForm
    template_name = 'upload.html'
    success_url = reverse_lazy('files_list')

    def form_valid(self, form):
        """Переопределение метода для проверки файла после загрузки."""
        response = super().form_valid(form)
        check_files.delay(self.object.id)

        return response
