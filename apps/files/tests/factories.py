from factory import Factory, SubFactory, Faker
from apps.files.models import FileUpload, FileCheckLogs
from django.contrib.auth.models import User


class UserFactory(Factory):
    """
    Factory class to generate user instances for testing purposes.
    """

    class Meta:
        model = User

    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password')
