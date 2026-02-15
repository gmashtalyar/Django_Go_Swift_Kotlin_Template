"""
Helper functions for the users app.

This module contains utility functions for handling payments via Yookassa
and managing web notifications.
"""
from typing import Optional, Union, Tuple, Any
from yookassa import Payment, Configuration
import uuid
from .models import PaymentHistory, Organization, WebNotification
from yookassa import Payment, Configuration
from yookassa.domain.response import PaymentResponse

from django.conf import settings
from django.http import HttpRequest


def get_yookassa_config():
    """Configure YooKassa SDK with credentials from settings."""
    Configuration.account_id = settings.YOOKASSA_ACCOUNT_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def payment_helper(request: HttpRequest, total_price: Union[int, float, str]) -> Tuple[str, str]:
    """
    Initiates a payment transaction via YooKassa.

    Credentials are loaded from Django settings (environment variables).

    Args:
        request (HttpRequest): The Django request object containing user information.
        total_price (Union[int, float, str]): The amount to be charged for the payment.

    Returns:
        Tuple[str, str]: A tuple containing:
            - confirmation_url (str): The URL to redirect the user for payment confirmation.
            - payment.id (str): The unique identifier for the created payment.
    """
    get_yookassa_config()

    idempotence_key: str = str(uuid.uuid4())

    # Build return URL dynamically
    return_url = request.build_absolute_uri('/accounts/payment-return-page')

    payment: PaymentResponse = Payment.create({
        "amount": {
            "value": f"{total_price}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url,
        },
        "metadata": {
            "user_id": request.user.id,
            "amount": f"{total_price}"
        },
        "test": settings.YOOKASSA_TEST_MODE,
        "capture": True,
        "description": "Оплата XXXX"
    }, idempotence_key)

    return payment.confirmation.confirmation_url, payment.id


def check_payment(payment_history: PaymentHistory) -> str:
    """
    Check payment status with YooKassa and activate organization if successful.

    Args:
        payment_history: PaymentHistory instance to check

    Returns:
        Status string: 'succeeded', 'pending', or 'failed'
    """
    # Idempotency: Already processed successfully?
    if payment_history.status == 'succeeded':
        # Verify organization is actually activated
        org = Organization.objects.filter(user=payment_history.user).first()
        if org and org.payment:
            return 'succeeded'

    get_yookassa_config()

    payment: PaymentResponse = Payment.find_one(payment_history.payment_id)

    if payment.status == 'succeeded' or payment.paid:
        # Double-check we haven't already processed this
        if payment_history.status == 'succeeded':
            return 'succeeded'

        # Update payment record
        payment_history.status = 'succeeded'
        payment_history.save(update_fields=['status'])

        # Activate organization (SimpleBoard's business logic)
        org: Organization = Organization.objects.get(user=payment_history.user)
        org.payment = True
        org.save()

        return 'succeeded'

    elif payment.status == 'canceled':
        payment_history.status = 'canceled'
        payment_history.save(update_fields=['status'])
        return 'failed'

    elif payment.status in ('pending', 'waiting_for_capture'):
        # Payment still processing
        return 'pending'

    return 'failed'


def close_item_notifications(arg1: Union[int, Any], arg2: Optional[int] = None) -> None:
    """
    Marks web notifications as read (not new) based on provided criteria.

    This function is flexible and can filter notifications by item ID, user,
    or a combination of both.

    Args:
        arg1 (Union[int, Any]): Can be an item ID (int) if arg2 is None and
                                arg1 is an int, or a User instance/ID.
        arg2 (Optional[int]): Optional item ID. If provided, arg1 is treated
                              as the user.

    Returns:
        None

    Usage:
        close_item_notifications(item_id) -> Marks notifications for this item as read.
        close_item_notifications(user_instance) -> Marks notifications for this user as read.
        close_item_notifications(user_instance, item_id) -> Marks notifications for
                                                            this user and item as read.
    """
    # TODO: arg1 can be int (item_id) or User model instance (user), consider using overload or better naming
    filters: dict[str, Union[int, Any]]
    if arg2 is None:
        if isinstance(arg1, int):  # Only pk is provided
            filters = {'item_id': arg1}
        else:  # Only user is provided
            filters = {'user_id': arg1}
    else:
        filters = {'user_id': arg1, 'item_id': arg2}
    WebNotification.objects.filter(**filters).update(is_new=False)