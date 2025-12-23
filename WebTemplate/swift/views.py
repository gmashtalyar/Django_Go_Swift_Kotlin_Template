"""
Views for Swift mobile application integration.

This module provides API endpoints for Swift (iOS) mobile applications,
including authentication, device registration for push notifications,
and notification settings management.
"""

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
    """
    Authenticate a user from a Swift mobile application.

    This endpoint handles user login requests from iOS applications.
    It accepts credentials via POST request and returns user data
    upon successful authentication.

    Args:
        request: The HTTP request object containing JSON body with:
            - username (str): The user's username.
            - password (str): The user's password.
            - email (str): The user's email (currently unused in authentication).

    Returns:
        JsonResponse: On success (200), returns user data including:
            - id (int): User's database ID.
            - email (str): User's email address.
            - first_name (str): User's first name.
            - last_name (str): User's last name.
            - username (str): User's username.
            - api_url (str): Base API URL for subsequent requests.
            - organization (str): User's organization (currently hardcoded as "no_org").
        On failure (401), returns {"message": "Login failed"}.

    Note:
        CSRF protection is disabled for this endpoint to allow mobile app access.
    """
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
            # TODO: org pass logic - implement organization lookup based on user
            user_data.update({"organization": "no_org"})
        else:
            return JsonResponse({"message": "Login failed"}, status=401)
        return JsonResponse(user_data)
    else:
        return JsonResponse({"message": "Login failed"}, status=401)


@api_view(["POST"])
def api_logout_swift(request: HttpRequest) -> Response:
    """
    Log out a user from a Swift mobile application session.

    This endpoint handles user logout requests from iOS applications.
    It terminates the user's session on the server side.

    Args:
        request: The HTTP POST request object.

    Returns:
        Response: A DRF Response with status 200 and message "Logout successful".

    Note:
        TODO: fix - This endpoint may need additional cleanup logic
        such as invalidating tokens or removing device registrations.
    """
    # TODO: fix
    if request.method == "POST":
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@csrf_exempt
def register_device(request: HttpRequest) -> HttpResponse:
    """
    Register a mobile device for push notifications.

    This endpoint registers a device's FCM (Firebase Cloud Messaging) token
    to enable push notifications. It handles both new registrations and
    updates to existing device registrations.

    Args:
        request: The HTTP request object containing JSON body with:
            - registration_id (str): The FCM device registration token.
            - device_type (str): The type of device (e.g., "ios", "android").
            - user_id (int): The ID of the user associated with the device.
            - email (str): The user's email address.

    Returns:
        HttpResponse: Success message with status 200 if device is registered.
        JsonResponse: Error with status 400 if device is already registered
            with the same registration_id.
        HttpResponse: Error message if request method is not POST.

    Side Effects:
        - Creates or updates a DevicesDB record for the device.
        - Creates a SwiftNotificationSettings record for new devices.
        - Creates an FCMDevice record for Firebase Cloud Messaging.

    Note:
        CSRF protection is disabled for this endpoint to allow mobile app access.
        The company is extracted from the email domain.
    """
    if request.method == "POST":
        data: Dict[str, Any] = json.loads(request.body)
        registration_id: Any = data.get("registration_id")
        device_type: Any = data.get("device_type")
        user_id: Any = data.get("user_id")
        email: Any = data.get("email")
        # Debug logging for device registration data
        print(registration_id)
        print(device_type)
        print(user_id)
        print(email)

        # Extract company domain from email address
        company: str = email.split("@")[1]
        # Check if device already exists for this user/email/device_type combination
        existing_device: DevicesDB | None = DevicesDB.objects.filter(email=email, user_id=user_id, device_type=device_type, company=email.split("@")[1]).first()
        if existing_device and existing_device.device_id == registration_id:
            # Device already registered with same token - no action needed
            return JsonResponse({"message": "Device already registered."}, status=400)
        elif existing_device and existing_device.device_id != registration_id:
            # Device exists but token changed - delete old record and create new one
            existing_device.delete()
            device: DevicesDB = DevicesDB.objects.create(email=email, device_id=registration_id, user_id=user_id, device_type=device_type, company=company)
        else:
            # New device registration
            device = DevicesDB.objects.create(email=email, device_id=registration_id, user_id=user_id, device_type=device_type, company=company)

        # Create default notification settings for the newly registered device
        SwiftNotificationSettings.objects.create(device_id=device.id)

        # Register device with FCM for push notification delivery
        device = FCMDevice()
        device.registration_id = registration_id
        device.type = device_type
        device.save()
        return HttpResponse("Device registered successfully.")
    else:
        return HttpResponse("Invalid request method")


def send_notification(request: HttpRequest, company: str, user_id: int) -> HttpResponse:
    """
    Send a push notification to a specific user's device.

    This function sends a Firebase Cloud Messaging notification to a user's
    registered device, identified by company domain and user ID.

    Args:
        request: The HTTP request object (currently unused but required for view signature).
        company: The company domain (extracted from user's email) to filter devices.
        user_id: The ID of the user whose device should receive the notification.

    Returns:
        HttpResponse: Success message if notification was sent successfully.
        HttpResponse: Error message if no device was found for the user.

    Raises:
        DevicesDB.DoesNotExist: If no device is found for the given company and user_id.
        FCMDevice.DoesNotExist: If no FCM device is found for the registration_id.

    Note:
        The notification title and body are currently hardcoded.
        There is a typo in the success message ("notificaiton" instead of "notification").
    """
    title: str = "XXXXXXXX"
    body: str = "Новое оповещение"  # Russian: "New notification"
    # Look up the device in our database by company and user
    device_db: DevicesDB = DevicesDB.objects.filter(company=company).get(user_id=user_id)
    # Get the corresponding FCM device for sending the notification
    device: FCMDevice = FCMDevice.objects.get(registration_id=device_db.device_id)
    if device:
        device.send_message(Message(notification=Notification(title=title, body=body)))
        return HttpResponse("Test notificaiton send successfully.")
    else:
        return HttpResponse("No device found for sending the notification.")


def share_preferences(request: HttpRequest, user_id: int, email: str, device_type: str) -> JsonResponse:
    """
    Retrieve notification preferences for a specific device.

    This function returns the notification settings for a user's device,
    converting boolean values to integers (0/1) for Swift compatibility.

    Args:
        request: The HTTP request object (currently unused but required for view signature).
        user_id: The ID of the user whose preferences to retrieve.
        email: The user's email address.
        device_type: The type of device (e.g., "ios", "android").

    Returns:
        JsonResponse: A JSON object containing all notification preference fields
            with boolean values converted to integers (0 or 1), plus user_id and email.

    Raises:
        DevicesDB.DoesNotExist: If no device matches the given criteria.
        SwiftNotificationSettings.DoesNotExist: If no notification settings exist
            for the device.
    """
    device: DevicesDB = DevicesDB.objects.get(user_id=user_id, email=email, device_type=device_type)
    preference_instance: SwiftNotificationSettings = SwiftNotificationSettings.objects.get(device=device)
    fields_dict: Dict[str, Any] = model_to_dict(preference_instance)
    # Convert boolean values to integers for Swift compatibility
    for key, value in fields_dict.items():
        if isinstance(value, bool):
            fields_dict[key] = 1 if value else 0
    # Add user identification fields to the response
    fields_dict['user_id'] = user_id
    fields_dict['email'] = email
    return JsonResponse(fields_dict)


@api_view(["POST"])
def notification_settings(request: HttpRequest) -> JsonResponse:
    """
    Update notification settings for a user's device.

    This endpoint allows users to modify their notification preferences
    for a specific device. Settings are identified by user_id, email,
    and device_type combination.

    Args:
        request: The HTTP request object containing JSON body with:
            - user_id (int): The user's ID (required for device lookup).
            - email (str): The user's email address (required for device lookup).
            - device_type (str): The type of device (required for device lookup).
            - Additional key-value pairs representing notification settings
              where values are integers (0 or 1) that will be converted to booleans.

    Returns:
        JsonResponse: On success (200), returns {"message": "Settings updated successfully."}.
        JsonResponse: On error (405), returns {"error": <exception>} or
            {"error": "Invalid request method."}.

    Raises:
        Exception: Catches all exceptions and returns them in the error response.
            TODO: Consider more specific exception handling and appropriate status codes.

    Note:
        Setting values are expected as integers (0 or 1) and are converted
        to boolean values before saving.
    """
    if request.method == "POST":
        data: Dict[str, Any] = json.loads(request.body)
        try:
            # Look up the device using the identifying fields
            device_instance: DevicesDB = DevicesDB.objects.get(user_id=data.get("user_id"), email=data.get("email"), device_type=data.get("device_type"))
            notification_settings_instance: SwiftNotificationSettings = SwiftNotificationSettings.objects.get(device=device_instance)
            # Update each setting field, excluding the lookup fields
            for key, value in data.items():
                if key != "user_id" and key != "email" and key != "device_type":
                    # Convert integer values (0/1) to boolean
                    setattr(notification_settings_instance, key, bool(int(value)))
            notification_settings_instance.save()
            return JsonResponse({"message": "Settings updated successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"error": e}, status=405)
    return JsonResponse({"error": "Invalid request method."}, status=405)
