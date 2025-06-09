from django.db import models
from django.utils import timezone
from django.conf import settings
import os

User = settings.AUTH_USER_MODEL


class SomeChoices(models.TextChoices):
    LINE = 'line', 'Линия'
    AREA = 'area', 'Область'


class BusinessLogic(models.Model):
    pass


class Documents(models.Model):
    client_inn = models.ForeignKey(BusinessLogic, on_delete=models.CASCADE)
    document = models.FileField(upload_to='Documents/', null=True, blank=True)
    document_upload_date = models.DateField(default=timezone.now)

    def delete(self, *args, **kwargs):
        # Delete the file from the server when the instance is deleted
        if self.document:
            if os.path.isfile(self.document.path):
                os.remove(self.document.path)
        super(Documents, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class FeedbackComments(models.Model):
    email = models.TextField()
    company = models.TextField()
    comment = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
