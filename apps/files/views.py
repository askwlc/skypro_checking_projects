from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

from .forms import FileUploadForm
from .models import FileUpload
from ..accounts.mixins import EmailVerifiedRequiredMixin


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

        return response


class FilesListView(LoginRequiredMixin, EmailVerifiedRequiredMixin, ListView):
    """Отображение списка файлов и их данные."""
    model = FileUpload
    template_name = 'files/files_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        """Отображение файлов загруженных текущим пользователем."""
        return FileUpload.objects.filter(user=self.request.user).order_by('-upload_time')


def file_results(request, file_id):
    """Отображение результатов проверки отдельного файла."""
    file = get_object_or_404(FileUpload, id=file_id)
    return render(request, 'files/file_results.html', {'file': file})


class FileDeleteView(DeleteView):
    """Удаление файлов."""
    model = FileUpload
    success_url = reverse_lazy('files_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class FileUpdateView(UpdateView):
    """Замена файлов."""
    model = FileUpload
    form_class = FileUploadForm
    template_name = 'files/upload.html'
    success_url = reverse_lazy('files_list')
