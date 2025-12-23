"""
Helper functions for the users app.

This module contains utility functions for handling payments via Yookassa
and managing web notifications.
"""
from typing import Optional, Union, Tuple, Any
from yookassa import Payment, Configuration
import uuid
from .models import PaymentHistory, Organization, WebNotification


def payment_helper(request: Any, total_price: Union[int, float, str]) -> Tuple[str, str]:
    """
    Initiates a payment process using the Yookassa API.

    Sets up the configuration with account ID and secret key, creates a unique
    idempotence key, and sends a payment creation request to Yookassa.

    Args:
        request (Any): The Django HttpRequest object containing user information.
                       (Type is Any to avoid circular imports or strict coupling).
        total_price (Union[int, float, str]): The amount to be charged.

    Returns:
        Tuple[str, str]: A tuple containing the confirmation URL (where the user
                         should be redirected) and the unique payment ID.
    """
    # TODO: request type should be HttpRequest from django.http, but using Any to avoid import
    Configuration.account_id = "some int here (acc number)"
    Configuration.secret_key = ""
    idempotence_key: str = str(uuid.uuid4())
    payment: Payment = Payment.create({
        "amount": {
            "value": f"{total_price}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"",
        },
        "metadata": {
            "user_id": request.user.id,
            "payment": f"{total_price}"
        },
        "test": True,
        "capture": True,
        "description": "Оплата XXXXXXXX"
    }, idempotence_key)
    confirmation_url: str = payment.confirmation.confirmation_url
    return confirmation_url, payment.id


def check_payment(payment_history: PaymentHistory) -> bool:
    """
    Verifies the status of a specific payment with Yookassa.

    Retrieves payment details using the payment ID from the provided history record.
    If the payment is confirmed as paid, it updates the associated Organization's
    payment status.

    Args:
        payment_history (PaymentHistory): The payment history record containing
                                          the payment ID to check.

    Returns:
        bool: True if the payment was successfully paid and the organization
              updated, False otherwise.
    """
    payment: Payment = Payment.find_one(payment_history.payment_id)
    if payment.paid:
        org: Organization = Organization.objects.get(user=payment_history.user)
        org.payment = True
        org.save()
        return True
    else:
        return False


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