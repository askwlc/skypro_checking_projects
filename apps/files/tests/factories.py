from django.contrib.auth.models import User
from factory import Factory, Faker, SubFactory

from apps.files.models import FileCheckLogs, FileUpload


class UserFactory(Factory):
    """Генерация экземпляров пользователей."""
    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password')


class FileUploadFactory(Factory):
    """Генерация экземпляров загрузки файлов."""
    class Meta:
        model = FileUpload
        strategy = "create"

    user = SubFactory(UserFactory)
    file = Faker('file_name')
    is_new = True


class FileCheckLogsFactory(Factory):
    """Генерация экземпляров логов."""
    class Meta:
        model = FileCheckLogs

    file = SubFactory(FileUploadFactory)
    status = 'waiting'
