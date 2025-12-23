"""
Background tasks for the users app.

This module contains Celery tasks related to user actions and notifications,
such as sending emails for demo requests and payment notifications.
"""

from typing import Any

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_demo_request_email_task() -> None:
    """
    Sends an email notification for a new demo request.

    This task is executed asynchronously using Celery. It sends a predefined
    email to the administrator notifying them that a user has requested a demo.

    Returns:
        None
    """
    subject: str = 'Simple Board: Demo Request'
    message: str = 'A new demo request has been submitted.'
    sender_email: str = settings.EMAIL_HOST_USER
    recipient_email: str = 'gmashtalyar@yandex.ru'
    send_mail(subject, message, sender_email, [recipient_email])


@shared_task
def send_payment_notification_email_task(organization_id: int) -> None:
    """
    Sends an email notification upon receiving a payment.

    This task retrieves the organization associated with the payment and sends
    an email to the administrator with the organization's name.

    Args:
        organization_id (int): The unique identifier of the Organization
            that made the payment.

    Returns:
        None

    Raises:
        Organization.DoesNotExist: If the organization with the provided ID
            does not exist.
    """
    from .models import Organization
    organization: Organization = Organization.objects.get(id=organization_id)
    subject: str = 'Simple Board: Payment'
    message: str = f'A new payment recieved for {organization.org}.'
    sender_email: str = settings.EMAIL_HOST_USER
    recipient_email: str = 'gmashtalyar@yandex.ru'
    send_mail(subject, message, sender_email, [recipient_email])