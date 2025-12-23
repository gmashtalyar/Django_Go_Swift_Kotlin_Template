"""
Celery tasks for asynchronous notification and email processing.

This module contains Celery shared tasks that handle background processing
of notifications and emails, allowing the main application to remain
responsive while these operations are performed asynchronously.
"""

from typing import Any

from celery import shared_task
from django.db.models import QuerySet
from users.models import NotificationTypes, WebNotifications
from users.utlis import match_status_n_preferences, notify_email
from .models import BusinessLogicModel


@shared_task
def celery_notification(item_id: int, notification_type: str, item_related_user_ids: list[int]) -> None:
    """
    Create web notifications for a list of users based on notification type.

    This task creates WebNotification records in the database for each user
    associated with a particular item. The notification type determines the
    category of notification created.

    Args:
        item_id: The ID of the item that triggered the notification.
        notification_type: The type of notification to create. Should be one of
            the values defined in NotificationTypes (type_1, type_2, type_3).
        item_related_user_ids: A list of user IDs who should receive the notification.

    Returns:
        None

    Side Effects:
        Creates WebNotifications records in the database for each user in
        item_related_user_ids.

    Note:
        All notification types currently create notifications with the same
        structure. The branching logic may be intended for future differentiation
        of notification handling per type.
    """
    for user_id in item_related_user_ids:
        if notification_type == NotificationTypes.type_1:
            WebNotifications.objects.create(item_id=item_id, user_id=user_id, notification_type=notification_type)
        elif notification_type == NotificationTypes.type_2:
            WebNotifications.objects.create(item_id=item_id, user_id=user_id, notification_type=notification_type)
        elif notification_type == NotificationTypes.type_3:
            WebNotifications.objects.create(item_id=item_id, user_id=user_id, notification_type=notification_type)


@shared_task
def celery_email(pk: int, message_type: str, sender_id: int, status_label: str, item_related_user_ids: list[int]) -> None:
    """
    Send email notifications to users based on their notification preferences.

    This task filters users by their notification preferences matching the given
    status label, then sends emails to those users who are both in the
    item_related_user_ids list and have matching notification preferences.

    Args:
        pk: The primary key of the item that triggered the email notification.
        message_type: The type of message/email template to use.
        sender_id: The user ID of the person who triggered/sent the notification.
        status_label: The status label used to filter notification preferences.
        item_related_user_ids: A list of user IDs potentially eligible to receive
            the email notification.

    Returns:
        None

    Side Effects:
        - Sends emails to qualifying users via the notify_email function.
        - Prints success or failure messages to stdout for each notification attempt.

    Raises:
        No exceptions are raised; all exceptions during email sending are caught
        and logged to stdout.
    """
    # TODO: Uncomment if item data is needed for email content
    # item = BusinessLogicModel.objects.get(id=pk)

    # Get users who have notification preferences matching the status label
    notification_preferences: QuerySet[Any] = match_status_n_preferences(status_label)
    notification_ids: list[int] = list(notification_preferences.values_list('user_id', flat=True))

    # Filter to only users who are both related to the item AND have matching preferences
    notifications: list[int] = list(set(x for x in item_related_user_ids if x in notification_ids))

    for user_id in notifications:
        try:
            notify_email(pk=pk, message_type=message_type, receiver_id=user_id, sender_id=sender_id)
            print(f"Email was sent to {user_id}!")
        except Exception as e:
            # Log the failure but continue processing other users
            print(f"Notification failure for {user_id}: {e}")
            pass


@shared_task
def some_night_task() -> None:
    """
    Mark all existing notifications as read/seen.

    This is intended to be run as a scheduled nightly task to reset the
    'is_new' flag on all notifications, marking them as no longer new.

    Returns:
        None

    Side Effects:
        Updates all WebNotifications records in the database, setting
        is_new to False.

    Note:
        TODO: The current implementation has a bug - calling save() on a
        QuerySet is not valid. This should be replaced with:
        WebNotifications.objects.all().update(is_new=False)
        or the loop should call notification.save() on each instance.
    """
    # XXXXXX
    notifications: QuerySet[WebNotifications] = WebNotifications.objects.all()
    for notification in notifications:
        notification.is_new = False
    # TODO: Fix - QuerySet.save() is not valid; use bulk_update or update()
    notifications.save()
