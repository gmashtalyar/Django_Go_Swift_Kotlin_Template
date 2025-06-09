from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from . import views

sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('', views.index, name='index'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
