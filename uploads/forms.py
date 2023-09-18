from django import forms

from .models import FileUpload


class FileUploadForm(forms.ModelForm):
    """Форма для загрузки файла на проверку."""

    class Meta:
        model = FileUpload
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if not file.name.endswith('.py'):
            raise forms.ValidationError('Возможна загрузка только .py файлов')
        return file
