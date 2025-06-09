from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BusinessLogic


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['home', 'cabinet-office', 'table', 'XXXXXXXXX', 'feedback', 'users:faq']

    def location(self, item):
        return reverse(item)


class DynamicModelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return BusinessLogic.objects.all()

    def location(self, obj):
        return reverse("some_view_XXXXXXXX", args=[obj.pk])
