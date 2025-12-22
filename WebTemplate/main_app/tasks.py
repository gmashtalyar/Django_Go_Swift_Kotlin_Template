from typing import Any

from celery import shared_task
from django.db.models import QuerySet
from users.models import NotificationTypes, WebNotifications
from users.utlis import match_status_n_preferences, notify_email
from .models import BusinessLogicModel


@shared_task
def celery_notification(item_id: int, notification_type: str, item_related_user_ids: list[int]) -> None:
    for user_id in item_related_user_ids:
        if notification_type == NotificationTypes.type_1:
            WebNotifications.objects.create(item_id=item_id, user_id=user_id, notification_type=notification_type)
        elif notification_type == NotificationTypes.type_2:
            WebNotifications.objects.create(item_id=item_id, user_id=user_id, notification_type=notification_type)
        elif notification_type == NotificationTypes.type_3:
            WebNotifications.objects.create(item_id=item_id, user_id=user_id, notification_type=notification_type)


@shared_task
def celery_email(pk: int, message_type: str, sender_id: int, status_label: str, item_related_user_ids: list[int]) -> None:
    # item = BusinessLogicModel.objects.get(id=pk)
    notification_preferences: QuerySet[Any] = match_status_n_preferences(status_label)
    notification_ids: list[int] = list(notification_preferences.values_list('user_id', flat=True))
    notifications: list[int] = list(set(x for x in item_related_user_ids if x in notification_ids))
    for user_id in notifications:
        try:
            notify_email(pk=pk, message_type=message_type, receiver_id=user_id, sender_id=sender_id)
            print(f"Email was sent to {user_id}!")
        except Exception as e:
            print(f"Notification failure for {user_id}: {e}")
            pass


@shared_task
def some_night_task() -> None:
    # XXXXXX
    notifications: QuerySet[WebNotifications] = WebNotifications.objects.all()
    for notification in notifications:
        notification.is_new = False
    notifications.save()

