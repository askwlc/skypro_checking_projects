from rest_framework import serializers
from ..files.models import FileUpload, FileCheckLogs


class FileCheckLogsSerializer(serializers.ModelSerializer):
    """Сериализатор модели FileCheckLogs."""

    class Meta:
        model = FileCheckLogs
        fields = ['status', 'check_date', 'check_result']


class FileUploadSerializer(serializers.ModelSerializer):
    """Сериализатор модели FileUpload."""
    status = serializers.SerializerMethodField()
    last_check = serializers.SerializerMethodField()

    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'last_check', 'status']

    def get_status(self, obj):
        latest_log = obj.check_logs.order_by('-check_date').first()
        return latest_log.status if latest_log else "pending"

    def get_last_check(self, obj):
        latest_log = obj.check_logs.order_by('-check_date').first()
        return latest_log.check_date if latest_log else None


class FileUploadDetailSerializer(FileUploadSerializer):
    checks = serializers.SerializerMethodField()

    class Meta(FileUploadSerializer.Meta):
        fields = FileUploadSerializer.Meta.fields + ['checks']

    def get_checks(self, obj):
        return FileCheckLogsSerializer(obj.check_logs.all(), many=True).data
