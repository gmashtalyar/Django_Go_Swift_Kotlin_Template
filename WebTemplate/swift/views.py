import json
from typing import Any, Dict

from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DevicesDB, SwiftNotificationSettings


@csrf_exempt
def api_login_swift(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data: Dict[str, Any] = json.loads(request.body.decode('utf-8'))
        username: Any = data.get("username")
        password: Any = data.get("password")
        email: Any = data.get("email")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_data: Dict[str, Any] = {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "api_url": "https://www.XXXXXX.ru/"}
            # user_instance = User.objects.get(username=user.username)
            # TODO: org pass logic
            user_data.update({"organization": "no_org"})
        else:
            return JsonResponse({"message": "Login failed"}, status=401)
        return JsonResponse(user_data)
    else:
        return JsonResponse({"message": "Login failed"}, status=401)


@api_view(["POST"])
def api_logout_swift(request: HttpRequest) -> Response:
    # TODO: fix
    if request.method == "POST":
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@csrf_exempt
def register_device(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        data: Dict[str, Any] = json.loads(request.body)
        registration_id: Any = data.get("registration_id")
        device_type: Any = data.get("device_type")
        user_id: Any = data.get("user_id")
        email: Any = data.get("email")
        print(registration_id)
        print(device_type)
        print(user_id)
        print(email)

        company: str = email.split("@")[1]
        existing_device: DevicesDB | None = DevicesDB.objects.filter(email=email, user_id=user_id, device_type=device_type, company=email.split("@")[1]).first()
        if existing_device and existing_device.device_id == registration_id:
            return JsonResponse({"message": "Device already registered."}, status=400)
        elif existing_device and existing_device.device_id != registration_id:
            existing_device.delete()
            device: DevicesDB = DevicesDB.objects.create(email=email, device_id=registration_id, user_id=user_id, device_type=device_type, company=company)
        else:
            device = DevicesDB.objects.create(email=email, device_id=registration_id, user_id=user_id, device_type=device_type, company=company)

        SwiftNotificationSettings.objects.create(device_id=device.id)

        device = FCMDevice()
        device.registration_id = registration_id
        device.type = device_type
        device.save()
        return HttpResponse("Device registered successfully.")
    else:
        return HttpResponse("Invalid request method")


def send_notification(request: HttpRequest, company: str, user_id: int) -> HttpResponse:
    title: str = "XXXXXXXX"
    body: str = "Новое оповещение"
    device_db: DevicesDB = DevicesDB.objects.filter(company=company).get(user_id=user_id)
    device: FCMDevice = FCMDevice.objects.get(registration_id=device_db.device_id)
    if device:
        device.send_message(Message(notification=Notification(title=title, body=body)))
        return HttpResponse("Test notificaiton send successfully.")
    else:
        return HttpResponse("No device found for sending the notification.")


def share_preferences(request: HttpRequest, user_id: int, email: str, device_type: str) -> JsonResponse:
    device: DevicesDB = DevicesDB.objects.get(user_id=user_id, email=email, device_type=device_type)
    preference_instance: SwiftNotificationSettings = SwiftNotificationSettings.objects.get(device=device)
    fields_dict: Dict[str, Any] = model_to_dict(preference_instance)
    for key, value in fields_dict.items():
        if isinstance(value, bool):
            fields_dict[key] = 1 if value else 0
    fields_dict['user_id'] = user_id
    fields_dict['email'] = email
    return JsonResponse(fields_dict)


@api_view(["POST"])
def notification_settings(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data: Dict[str, Any] = json.loads(request.body)
        try:
            device_instance: DevicesDB = DevicesDB.objects.get(user_id=data.get("user_id"), email=data.get("email"), device_type=data.get("device_type"))
            notification_settings_instance: SwiftNotificationSettings = SwiftNotificationSettings.objects.get(device=device_instance)
            for key, value in data.items():
                if key != "user_id" and key != "email" and key != "device_type":
                    setattr(notification_settings_instance, key, bool(int(value)))
            notification_settings_instance.save()
            return JsonResponse({"message": "Settings updated successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"error": e}, status=405)
    return JsonResponse({"error": "Invalid request method."}, status=405)
