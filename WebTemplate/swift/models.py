from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class DevicesDB(models.Model):
    email = models.CharField(max_length=30)
    device_id = models.CharField(max_length=250)
    user_id = models.PositiveIntegerField()
    device_type = models.CharField(max_length=30)
    company = models.CharField(max_length=30)


class SwiftNotificationSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device = models.ForeignKey(DevicesDB, on_delete=models.CASCADE)
    notification_types = models.JSONField(default=list)
