from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import FileUploadForm
from .models import FileUpload
from .tasks import check_files


class FileUploadView(LoginRequiredMixin, CreateView):
    """Обработка загрузки файла для проверки."""
    model = FileUpload
    form_class = FileUploadForm
    template_name = 'upload.html'
    success_url = reverse_lazy('files_list')

    def form_valid(self, form):
        """Переопределение метода для проверки файла после загрузки."""
        form.instance.user = self.request.user
        response = super().form_valid(form)
        check_files.delay(self.object.id)

        return response


class FilesListView(LoginRequiredMixin, ListView):
    """Отображение списка файлов и их результаты проверок."""
    model = FileUpload
    template_name = 'files_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        """Отображение файлов загруженных текущим пользователем."""
        return FileUpload.objects.filter(user=self.request.user).order_by('-upload_time')