from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from users.views import error


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),

]


handler404 = error
handler500 = error
