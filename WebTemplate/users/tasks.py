from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_demo_request_email_task():
    subject = 'Simple Board: Demo Request'
    message = 'A new demo request has been submitted.'
    sender_email = settings.EMAIL_HOST_USER
    recipient_email = 'gmashtalyar@yandex.ru'
    send_mail(subject, message, sender_email, [recipient_email])


@shared_task
def send_payment_notification_email_task(organization_id):
    from .models import Organization
    organization = Organization.objects.get(id=organization_id)
    subject = 'Simple Board: Payment'
    message = f'A new payment recieved for {organization.org}.'
    sender_email = settings.EMAIL_HOST_USER
    recipient_email = 'gmashtalyar@yandex.ru'
    send_mail(subject, message, sender_email, [recipient_email])
