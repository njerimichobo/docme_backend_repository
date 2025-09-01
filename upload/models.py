from django.db import models


class Upload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    patient_name = models.CharField(max_length=255, null=True, blank=True)
    patient_id = models.CharField(max_length=100, null=True, blank=True)
    report_date = models.DateField(null=True, blank=True)
    llm_result = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Report {self.id}"

    class Meta:
        verbose_name = 'Upload'
        verbose_name_plural = 'Uploads'
        ordering = ['-uploaded_at']
