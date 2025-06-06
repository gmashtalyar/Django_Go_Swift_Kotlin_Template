from django.contrib import admin
from .models import Demo, Organization, TariffModel, PaymentHistory, FeedbackComments, DashboardComments, DashboardItemComments


class TariffModelAdmin(admin.ModelAdmin):
    list_display = ('duration', 'user_count', 'price_per_user')


admin.site.register(Demo)
admin.site.register(Organization)
admin.site.register(TariffModel, TariffModelAdmin)
admin.site.register(PaymentHistory)
admin.site.register(FeedbackComments)
admin.site.register(DashboardComments)
admin.site.register(DashboardItemComments)
