from django.urls import path

from . import views

app_name = 'swift'

urlpatterns = [
    path("api_login_swift", views.api_login_swift, name="api_login_swift"),
    path("api_logout_swift", views.api_logout_swift, name="api_logout_swift"),
    path("register_device", views.register_device, name="register_device"),
    path("send_notification/<str:company>/<int:user_id>", views.send_notification, name="send_notification"),
    path("share_preferences/<int:user_id>/<str:email>/<str:device_type>", views.share_preferences, name="share_preferences"),
    path('notification_settings', views.notification_settings, name='notification_settings'),

]
