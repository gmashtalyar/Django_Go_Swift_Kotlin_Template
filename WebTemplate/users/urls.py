from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('faq/', views.faq, name='faq'),
    path('password-reset-request', views.password_reset_request, name='password-reset-request'),
    path('password-reset-confirm', views.password_reset_confirm, name='password-reset-confirm'),
    path('password-reset/reset/<uidb64>/<token>/', views.password_reset_confirm, name='password-reset-confirm'),

    path('change-user-data', views.change_user_data, name='change-user-data'),
    path('organization-create', views.organization_create, name='organization-create'),
    path('organization-add-users/<int:org_id>', views.organization_add_users, name='organization-add-users'),
    path('company-properties/', views.company_properties, name='company-properties'),
    path('org-settings/', views.org_settings, name='org-settings'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('tariff-plan', views.tariff_plan, name='tariff-plan'),
    path('demo-booking', views.demo_booking, name='demo-booking'),
    path('ask-signup', views.ask_signup, name='ask-signup'),
    path('choose-tariff-page', views.choose_tariff_page, name='choose-tariff-page'),
    path('org-registration-process-info', views.org_registration_process_info, name='org-registration-process-info'),
    path('payment-success-page', views.payment_success_page, name='payment-success-page'),
    path('payment-return-page', views.payment_return_page, name='payment-return-page'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('oferta', views.oferta, name='oferta'),
    path('feedback', views.feedback, name='feedback'),
    path('file-synchronization/', views.file_synchronization, name='file-synchronization'),
    path('buh-synchronization/', views.buh_synchronization, name='buh-synchronization'),
    path('sync-file/<str:file_name>', views.sync_file, name='sync-file'),
    path('user-management/', views.user_management, name='user-management'),
    path('assign-group/<int:user_id>/<str:group_name>/', views.assign_group, name='assign-group'),
    path('remove-group/<int:user_id>/<str:group_name>/', views.remove_group, name='remove-group'),

]

