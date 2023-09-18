import pytest
from django.contrib.auth.models import User

from apps.files.models import FileCheckLogs, FileUpload
from apps.files.tests.factories import (FileCheckLogsFactory,
                                        FileUploadFactory, UserFactory)


@pytest.mark.django_db
def test_user_creation():
    """Тест успешного создания экземпляра User."""
    user = UserFactory()
    assert isinstance(user, User)


@pytest.mark.django_db
def test_file_upload_creation():
    """Тест успешного создания экземпляра Fileupload."""
    file_upload = FileUploadFactory()
    assert isinstance(file_upload, FileUpload)


@pytest.mark.django_db
def test_file_check_logs_creation():
    """Тест успешного создания экземпляра FileCheckLogs."""
    file_check_log = FileCheckLogsFactory()
    assert isinstance(file_check_log, FileCheckLogs)
