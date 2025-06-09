from django.contrib import admin
from .models import BusinessLogic
from import_export.admin import ImportExportModelAdmin
from import_export import resources


class BusinessModelResource(resources.ModelResource):
    class Meta:
        model = BusinessLogic


class BusinessAdmin(ImportExportModelAdmin):
    resource_class = BusinessModelResource

admin.site.register(BusinessLogic, BusinessAdmin)
admin.site.register(BusinessLogic)
