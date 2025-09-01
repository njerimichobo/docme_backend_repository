from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Upload


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'

    def validate_file(self, value):
        # Check file size (limit to 5MB)
        if value.size > 5 * 1024 * 1024:
            raise ValidationError("File size exceeds the limit of 5MB.")
        return value
