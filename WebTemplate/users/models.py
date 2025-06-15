from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .tasks import send_demo_request_email_task, send_payment_notification_email_task
from django.utils import timezone

from main_app.models import BusinessLogicModel

User = settings.AUTH_USER_MODEL


class Organization(models.Model):
    org = models.CharField(max_length=30, blank=False, null=False)
    corporate_email = models.CharField(max_length=30, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.BooleanField(default=False)


@receiver(post_save, sender=Organization)
def send_payment_confirmation_email(sender, instance, **kwargs):
    if instance.payment:
        send_payment_notification_email_task(instance.id)


class Demo(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)
    message = models.TextField(blank=True, null=True)
    channel = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.email}: {self.first_name}"


@receiver(post_save, sender=Demo)
def send_demo_request_email(sender, instance, created, **kwargs):
    if created:
        send_demo_request_email_task()


class TariffModel(models.Model):
    duration_choices = [('monthly', 'Monthly'), ('annually', 'Annually'), ('two_years', 'Two Years')]
    user_count_choices = [(50, "50 users"), (100, "100 users"), (250, "250 users"), (500, "500 users"), (1000, "1000 users")]

    duration = models.CharField(max_length=25, choices=duration_choices)
    user_count = models.SmallIntegerField(choices=user_count_choices)
    price_per_user = models.PositiveIntegerField()


class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)


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


class BusinessModelComments(models.Model):
    item = models.ForeignKey(BusinessLogicModel, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Обсуждение XXXXXXXX'
        verbose_name_plural = 'Обсуждение XXXXXXXX'


class NotificationTypes(models.TextChoices):
    type_1 = 'Тип 1', 'Тип 1'
    type_2 = 'Тип 2', 'Тип 2'
    type_3 = 'Тип 3', 'Тип 3'


class WebNotifications(models.Model):
    item = models.ForeignKey(BusinessLogicModel, on_delete=models.CASCADE)
    is_new = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(choices=NotificationTypes.choices, max_length=50, blank=False, null=False, default=NotificationTypes.type_1)


class EmailNotificationSettings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_types = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user.email}"
