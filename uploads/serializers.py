from rest_framework import serializers
from ..files.models import FileUpload, FileCheckLogs


class FileCheckLogsSerializer(serializers.ModelSerializer):
    """Сериализатор модели FileCheckLogs."""
    status = serializers.CharField()
    date = serializers.DateTimeField(source='check_date')
    result = serializers.CharField()

    class Meta:
        model = FileCheckLogs
        fields = ['status', 'date', 'result']


class FileUploadSerializer(serializers.ModelSerializer):
    """Сериализатор модели FileUpload."""
    filename = serializers.CharField(source='file.name')
    status = serializers.SerializerMethodField()
    last_check = serializers.SerializerMethodField()

    class Meta:
        model = FileUpload
        fields = ['id', 'filename', 'last_check', 'status']

    def get_status(self, obj):
        last_log = obj.logs.last()
        return last_log.status if last_log else 'pending'

    def get_last_check(self, obj):
        latest_log = obj.logs.order_by('-check_date').first()
        return latest_log.check_date if latest_log else None


class FileUploadDetailSerializer(FileUploadSerializer):
    checks = FileCheckLogsSerializer(source='logs', many=True)

    class Meta:
        model = FileUpload
        fields = ['id', 'filename', 'last_check', 'status', 'checks']
