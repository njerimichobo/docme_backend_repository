from django.contrib import admin
from .models import Upload


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at',
                    'patient_name', 'patient_id', 'report_date')
    search_fields = ('file',)
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)
