from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import FileUploadForm
from .models import FileUpload
from ..accounts.mixins import EmailVerifiedRequiredMixin
import logging

logger = logging.getLogger('apps')


class FileUploadView(LoginRequiredMixin, EmailVerifiedRequiredMixin, CreateView):
    """Обработка загрузки файла для проверки."""
    model = FileUpload
    form_class = FileUploadForm
    template_name = 'files/upload.html'
    success_url = reverse_lazy('files_list')

    def form_valid(self, form):
        """Переопределение метода для проверки файла после загрузки."""
        form.instance.user = self.request.user
        response = super().form_valid(form)
        logger.info(f"Файл {form.instance.file.name} загружен юзером {self.request.user.username}.")
        return response


class FilesListView(LoginRequiredMixin, ListView):
    """Отображение списка файлов и их данные."""
    model = FileUpload
    template_name = 'files/files_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        """Отображение файлов загруженных текущим пользователем."""
        return FileUpload.objects.filter(user=self.request.user).order_by('-upload_time')


class FileResultsView(DetailView):
    """Отображение результатов проверки отдельного файла."""
    model = FileUpload
    template_name = 'files/file_results.html'
    context_object_name = 'file'


class FileDeleteView(DeleteView):
    """Удаление файлов."""
    model = FileUpload
    success_url = reverse_lazy('files_list')

    def get(self, request, *args, **kwargs):
        logger.info(f"Файл с ID {self.kwargs['pk']} отправлен на удаление юзером {request.user.username}.")
        return self.post(request, *args, **kwargs)


class FileUpdateView(UpdateView):
    """Замена файлов."""
    model = FileUpload
    form_class = FileUploadForm
    template_name = 'files/upload.html'
    success_url = reverse_lazy('files_list')
