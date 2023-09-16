from django import forms
from .models import FileUpload


class FileUploadForm(forms.ModelForm):
    """Форма для загрузки файла на проверку."""

    class Meta:
        model = FileUpload
        fields = ['file', 'user']
