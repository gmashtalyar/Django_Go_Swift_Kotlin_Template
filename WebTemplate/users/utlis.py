import os, smtplib, ssl

from django.contrib.auth.models import User

from .models import EmailNotificationSettings, NotificationTypes


def match_status_n_preferences(status: str):

    if status == NotificationTypes.type_1:
        notification_preferences = EmailNotificationSettings.objects.filter(notification_types=NotificationTypes.type_1)
    elif status == NotificationTypes.type_2:
        notification_preferences = EmailNotificationSettings.objects.filter(notification_types=NotificationTypes.type_2)
    elif status == NotificationTypes.type_3:
        notification_preferences = EmailNotificationSettings.objects.filter(notification_types=NotificationTypes.type_3)
    else:
        return None
    return notification_preferences


def notify_email(pk, message_type, receiver_id, sender_id):
    receiver = User.objects.get(id=receiver_id)
    email_to = receiver.email

    server = smtplib.SMTP('mail.hosting.reg.ru:587')
    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()

    login = os.environ.get('EMAIL_HOST_USER')
    password = os.environ.get('EMAIL_HOST_PASSWORD')
    email_from = os.environ.get('DEFAULT_FROM_EMAIL')
    subject = "Оповещение ХХХХХ"

    if receiver_id == sender_id:
        pass
    else:
        status_message = f"""\
        Новое оповещение - {message_type}.
        Some text here XXXXX
        Ссылка на объект: https://XXXXXX/XXXXXXX/{pk} .
        """
        status_text = f"Subject:{subject}\n\n{status_message}".encode('utf-8')

        server.login(login, password)
        server.sendmail(email_from, email_to, status_text)
        server.quit()

