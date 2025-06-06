import os
from django.test import TestCase, Client, override_settings
from .models import Organization, Demo, PaymentHistory, TariffModel
from .forms import AddUserForm
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.mail import outbox
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from unittest.mock import patch


class DemoBookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.demo_booking_url = reverse('users:demo-booking')

    def test_demo_booking(self):
        response = self.client.get(self.demo_booking_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/demo_booking.html')
        self.assertIn('form', response.context)

    def test_demo_booking_valid_post(self):
        data = {"first_name": "Евгений", "last_name": "Дубский", "email": "someemail@mail.ru", "company_name": "Абра-кадабра",}
        response = self.client.post(self.demo_booking_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Demo.objects.count(), 1)

    def test_demo_booking_invalid_post(self):
        data = {'first_name': '', 'last_name': 'Doe', 'email': 'sdfsdf', 'company_name': 'Acme Corp', 'phone_number': '1234567890',
            'message': 'Looking forward to the demo.', 'channel': 'Google Search'}
        response = self.client.post(self.demo_booking_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/demo_booking.html')
        form = response.context['form']
        self.assertFormError(form, 'first_name', 'Обязательное поле.')
        self.assertFormError(form, 'email', 'Введите правильный адрес электронной почты.')
        self.assertEqual(Demo.objects.count(), 0)


class OrganizationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.org_admin = User.objects.create_user(username='org_admin', password='password', email="test@test_3.ru")
        self.user = User.objects.create_user(username='test', password='test', email="test@test.ru")
        self.user_2 = User.objects.create_user(username='test_2', password='test_2', email="test_2@test.ru")
        self.user_3 = User.objects.create_user(username='test_3', password='test_3', email="test_3@test_3.ru")
        self.test_org_user = User.objects.create_user(username='test_org_user', password='test_org_user', email="test_org_user@test_org_user.ru")

        self.org_admin_group = Group.objects.create(name='org_admin')
        self.dashboard_creator_group = Group.objects.create(name='dashboard_creator')
        self.data_contributor_group = Group.objects.create(name='data_contributor')
        self.viewer_group = Group.objects.create(name='viewer')

        self.user.groups.add(self.org_admin_group)
        self.org_admin.groups.add(self.org_admin_group)

        self.test_org_user.groups.add(self.org_admin_group)
        self.client.login(username='test', password='test')

        self.test_organization = Organization.objects.create(org="TestOrg", corporate_email="test_org_user.ru", user=self.test_org_user)
        self.org = Organization.objects.create(org='TestOrg', corporate_email='test_3.ru', user=self.org_admin)

        # urls
        self.company_properties_url = reverse('users:company-properties')
        self.organization_create_url = reverse('users:organization-create')
        self.organization_add_users_url = reverse('users:organization-add-users', args=[1])
        self.company_properties_url = reverse('users:company-properties')
        self.org_settings_url = reverse('users:org-settings')
        self.user_management_url = reverse('users:user-management')

    def test_organization_create_get(self):
        response = self.client.get(self.organization_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create_organization.html')
        self.assertIn('form', response.context)

    def test_organization_create_valid_post(self):
        data = {'org': 'Test Organization', 'corporate_email': 'user@test.ru'}
        response = self.client.post(self.organization_create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Organization.objects.filter(org='Test Organization', corporate_email='test.ru').exists())

    def test_organization_create_invalid_post(self):
        data = {'org': 'Test Organization', 'corporate_email': 'user'}
        response = self.client.post(self.organization_create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create_organization.html')
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('Введите действительный адрес корпоративной электронной почты.', form.errors['corporate_email'])
        self.assertFalse(Organization.objects.filter(corporate_email='user').exists())

    def test_organization_add_users_get(self):
        # Organization.objects.create(org='TestOrg', corporate_email='test.ru', user=self.user)
        # response = self.client.get(self.organization_add_users_url)
        org = Organization.objects.create(org='TestOrg', corporate_email='test.ru', user=self.user)
        self.organization_add_users_url = reverse('users:organization-add-users', args=[org.pk])
        response = self.client.get(self.organization_add_users_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/organization_add_users.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertNotIn('test@test.ru', form.fields)
        self.assertIn('test_2@test.ru', form.fields)
        self.assertNotIn('test_3@test_3.ru', form.fields)

    def test_organization_add_users_valid_post(self):
        org = Organization.objects.create(org='TestOrg', corporate_email='test.ru', user=self.user)
        self.organization_add_users_url = reverse('users:organization-add-users', args=[org.pk])
        data = {'test_2@test.ru': True}
        response = self.client.post(self.organization_add_users_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Organization.objects.filter(org='TestOrg', corporate_email='test.ru').exists())
        self.assertTrue(Organization.objects.filter(org='TestOrg', corporate_email='test_2@test.ru').exists())

    def test_organization_create_already_exists(self):
        Organization.objects.create(org='Existing Org', corporate_email='existing@test.ru', user=self.user)
        data = {'org': 'New Org', 'corporate_email': 'new@test.ru'}
        response = self.client.post(self.organization_create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create_organization.html')
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('Вы уже создали организацию. Чтобы создать новую - зарегистрируйтесь с другой корпоративной почтой.',form.errors['org'])
        self.assertEqual(Organization.objects.filter(user=self.user).count(), 1)

    def test_organization_add_users_invalid_post(self):
        data = {"invalid@test_orkjnbg_user.com": True,}
        form = AddUserForm(data, user_emails=["user1@test_org_user.com", "user2@test_org_user.com"], organization=self.test_organization)
        self.assertFalse(form.is_valid())

    def test_removing_user(self):
        Organization.objects.create(org=self.test_organization, corporate_email=self.user_2.email, user=self.user_2)
        self.user_2.groups.add(self.viewer_group)
        self.assertTrue(Organization.objects.filter(user=self.user_2, org=self.test_organization).exists())
        self.assertTrue(self.user_2.groups.filter(name='viewer').exists())
        data = {self.user_2.email: False}
        form = AddUserForm(data, user_emails=[self.user_2.email], organization=self.test_organization)
        self.assertTrue(form.is_valid())
        form.save(organization=self.test_organization)
        self.assertFalse(Organization.objects.filter(user=self.user_2, org=self.test_organization).exists())
        self.assertFalse(self.user_2.groups.filter(name='viewer').exists())

    def test_company_properties_get(self):
        Organization.objects.create(org='TestOrg', corporate_email='test.ru', user=self.user)
        Organization.objects.create(org='TestOrg', corporate_email='test.ru', user=self.user_2)
        response = self.client.get(self.company_properties_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/company_properties.html')
        self.assertEqual(Organization.objects.count(), 4)
        # see if users are rendered

    def test_org_settings_with_org_admin(self):
        self.client.login(username='test_org_user', password='test_org_user')
        response = self.client.get(self.org_settings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/org_settings.html')
        self.assertContains(response, "Управление правами пользователей")

    def test_org_settings_without_org_admin(self):
        self.user.groups.remove(self.org_admin_group)
        response = self.client.get(self.org_settings_url)
        self.assertEqual(response.status_code, 403)

    def test_user_management_access_by_org_admin(self):
        self.client.login(username='org_admin', password='password')
        response = self.client.get(self.user_management_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_management.html')
        self.assertContains(response, "TestOrg")

    def test_user_management_lists_correct_users(self):
        Organization.objects.create(org='TestOrg', corporate_email='test_3.ru', user=self.user_3)
        org_users = Organization.objects.filter(user=self.org_admin).values_list('user__email', flat=True)
        self.client.login(username='org_admin', password='password')
        response = self.client.get(self.user_management_url)
        users_in_context = response.context['users']

        self.assertEqual(len(users_in_context), 2)
        user_emails = [user_data['user'].email for user_data in users_in_context]
        self.assertNotIn('user_2@test.ru', user_emails)
        self.assertIn('test_3@test_3.ru', user_emails)
        self.assertNotIn('test_org_user@test_org_user.ru', user_emails)

    def test_user_management_role_assignment(self):
        self.client.login(username='org_admin', password='password')
        response = self.client.get(self.user_management_url)
        users_in_context = response.context['users']

        for user_data in users_in_context:
            if user_data['user'].username == 'user_2':
                self.assertTrue(user_data['is_viewer'])
                self.assertFalse(user_data['is_dashboard_creator'])
                self.assertFalse(user_data['is_data_contributor'])
                self.assertFalse(user_data['is_external_user'])
            elif user_data['user'].username == 'user_3':
                self.assertFalse(user_data['is_viewer'])
                self.assertTrue(user_data['is_dashboard_creator'])
                self.assertFalse(user_data['is_data_contributor'])
                self.assertFalse(user_data['is_external_user'])

    def test_user_management_access_denied_to_non_admin(self):
        self.client.login(username='test_3', password='test_3')
        response = self.client.get(self.user_management_url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='non_org_user', password='password')
        response = self.client.get(self.user_management_url)
        self.assertEqual(response.status_code, 403)


class MinorUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.org = Organization.objects.create(org="TestOrg", corporate_email="test.com", user=self.user)

        self.org_admin_group = Group.objects.create(name='org_admin')
        self.dashboard_creator_group = Group.objects.create(name='dashboard_creator')
        self.data_contributor_group = Group.objects.create(name='data_contributor')
        self.viewer_group = Group.objects.create(name='viewer')

        self.tariff_plan_url = reverse('users:tariff-plan')
        self.cabinet_url = reverse('users:cabinet')
        self.ask_signup_url = reverse('users:ask-signup')
        self.oferta_url = reverse('users:oferta')
        self.privacy_policy_url = reverse('users:privacy-policy')
        self.feedback_url = reverse('users:feedback')
        self.file_synchronization_url = reverse('users:file-synchronization')
        self.buh_synchronization_url = reverse('users:buh-synchronization')
        self.payment_url = reverse('users:payment-success-page')
        self.registration_url = reverse('users:org-registration-process-info')

    def test_cabinet_with_organization(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.cabinet_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/cabinet.html')

    def test_cabinet_without_organization(self):
        self.client.login(username='testuser', password='testpass')
        self.org.delete()
        response = self.client.get(self.cabinet_url)
        self.assertEqual(response.status_code, 200)

    def test_tariff_plan(self):
        response = self.client.get(self.tariff_plan_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/tariff_plan.html')

    # def test_cabinet_not_logged_in(self):
    #     response = self.client.get(self.cabinet_url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTemplateUsed(response, 'users/ask_signup.html')

    def test_ask_signup(self):
        response = self.client.get(self.ask_signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/ask_signup.html')

    def test_oferta_view(self):
        response = self.client.get(self.oferta_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('Content-Disposition', response)
        self.assertTrue(response['Content-Disposition'].startswith('inline; filename="oferta.pdf"'))

    def test_oferta_view_file_not_found(self):
        os.rename("Documents/oferta.pdf", "Documents/oferta_temp.pdf")
        response = self.client.get(self.oferta_url)
        self.assertEqual(response.status_code, 404)
        os.rename("Documents/oferta_temp.pdf", "Documents/oferta.pdf")

    def test_privacy_policy_view(self):
        response = self.client.get(self.privacy_policy_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('Content-Disposition', response)
        self.assertTrue(response['Content-Disposition'].startswith('inline; filename="privacy_policy.pdf"'))

    def test_privacy_policy_view_file_not_found(self):
        # Temporarily rename the file to simulate file not found
        os.rename("Documents/privacy_policy.pdf", "Documents/privacy_policy_temp.pdf")
        response = self.client.get(self.privacy_policy_url)
        self.assertEqual(response.status_code, 404)
        # Restore the file
        os.rename("Documents/privacy_policy_temp.pdf", "Documents/privacy_policy.pdf")

    def test_feedback_view_get(self):
        response = self.client.get(self.feedback_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/feedback.html')
        self.assertIn('form', response.context)

    def test_feedback_view_post_valid(self):
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'comment': 'This is a test feedback comment.'
        }
        response = self.client.post(self.feedback_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_feedback_view_post_invalid(self):
        data = {
            'name': '',
            'email': 'invalidemail',
            'comment': ''
        }
        response = self.client.post(self.feedback_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/feedback.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)

    def test_file_synchronization_view(self):
        response = self.client.get(self.file_synchronization_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/file_synchronization.html')

    # def test_buh_synchronization_view(self):
    #     response = self.client.get(self.buh_synchronization_url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'users/buh_synchronization.html')

    def test_payment_success_page(self):
        response = self.client.get(self.payment_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/payment_success_page.html')

    def test_org_registration_process_info_page(self):
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/org_registration_process_info.html')


class UserLogicTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test', email="test@test.ru")
        self.admin_user = User.objects.create_user(username='adminuser', password='password123')

        self.org_admin_group = Group.objects.create(name='org_admin')
        self.dashboard_creator_group = Group.objects.create(name='dashboard_creator')
        self.data_contributor_group = Group.objects.create(name='data_contributor')
        self.viewer_group = Group.objects.create(name='viewer')
        self.admin_user.groups.add(self.org_admin_group)

        self.signup_url = reverse('users:signup')
        self.login_url = reverse('users:login')
        self.logout_url = reverse('users:logout')
        self.password_reset_request_url = reverse('users:password-reset-request')
        self.password_reset_confirm_url = reverse('users:password-reset-confirm')
        self.change_user_data_url = reverse('users:change-user-data')
        self.assign_group_url = lambda user_id, group: reverse('users:assign-group', args=[user_id, group])
        self.remove_group_url = lambda user_id, group: reverse('users:remove-group', args=[user_id, group])

    def test_assign_group_as_admin(self):
        self.client.login(username='adminuser', password='password123')
        response = self.client.post(self.assign_group_url(self.user.id, 'dashboard_creator'))
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.dashboard_creator_group, self.user.groups.all())

    def test_remove_group_as_admin(self):
        self.user.groups.add(self.dashboard_creator_group)
        self.client.login(username='adminuser', password='password123')
        response = self.client.post(self.remove_group_url(self.user.id, 'dashboard_creator'))
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.dashboard_creator_group, self.user.groups.all())

    def test_assign_group_as_non_admin(self):
        self.client.login(username='test', password='test')
        response = self.client.post(self.assign_group_url(self.user.id, 'dashboard_creator'))
        self.assertEqual(response.status_code, 403)

    def test_remove_group_as_non_admin(self):
        self.user.groups.add(self.dashboard_creator_group)
        self.client.login(username='test', password='test')
        response = self.client.post(self.remove_group_url(self.user.id, 'dashboard_creator'))
        self.assertEqual(response.status_code, 403)

    def test_signup_view_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signup.html')
        self.assertIn('form', response.context)

    def test_signup_view_valid_post(self):
        data = {'username': 'new_user', 'password1': 'Sfjd84!kjfDJK','password2': 'Sfjd84!kjfDJK', "first_name": "John",
                "last_name": "Mednikov", "email": "smth@evraz.com"}
        response = self.client.post(self.signup_url, data)
        new_user = User.objects.get(username="new_user")
        self.assertEqual(new_user.username, "new_user")
        self.assertEqual(response.status_code, 302)

    def test_signup_view_invalid_post(self):
        data = {'username': 'test', 'password': 'sdfkjsdf'}
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn('form', response.context)

    def test_login_view_valid_post(self):
        data = {'username': 'test', 'password': 'test'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)

    def test_login_view_invalid_post(self):
        data = {'username': 'dfjkh', 'password': 'sdfkjbhsd'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logout_view_get(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)

    def test_logout_view_post(self):
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, 302)

    def test_change_user_data_get(self):
        self.client.login(username='test', password='test')
        response = self.client.get(self.change_user_data_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_user_data.html')
        self.assertIn('form', response.context)

    def test_change_user_data_post_valid(self):
        self.client.login(username='test', password='test')
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.change_user_data_url, data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertEqual(self.user.first_name, 'New')
        self.assertEqual(self.user.last_name, 'User')

    def test_change_user_data_post_invalid(self):
        self.client.login(username='test', password='test')
        data = {'username': '', 'email': 'invalidemail', 'first_name': '', 'last_name': ''}
        response = self.client.post(self.change_user_data_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_user_data.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(form.errors)


class PasswordResetTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='oldpassword', email='testuser@example.com')
        self.password_reset_request_url = reverse('users:password-reset-request')

        self.token = default_token_generator.make_token(self.user)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.password_reset_confirm_url = reverse('users:password-reset-confirm', args=[self.uid, self.token])

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_request_post_valid_email(self):
        data = {'email': 'testuser@example.com'}
        response = self.client.post(self.password_reset_request_url, data)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertContains(response, "Ссылка для восстановления пароля направлена на почту.")
        # self.assertEqual(len(outbox), 1)
        # self.assertIn("Восстановление пароля", outbox[0].subject)
        # self.assertIn(self.token, outbox[0].body)

    def test_password_reset_request_post_invalid_email(self):
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.password_reset_request_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пользователь с такой почтой не нашелся.")

    def test_password_reset_confirm_post_valid(self):
        data = {'new_password': 'newpassword123'}
        response = self.client.post(self.password_reset_confirm_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_password_reset_confirm_invalid_token(self):
        invalid_token = 'invalidtoken'
        invalid_url = reverse('users:password-reset-confirm', args=[self.uid, invalid_token])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Неверная ссылка восстановления пароля")

    def test_password_reset_confirm_invalid_uid(self):
        invalid_uid = 'invaliduid'
        invalid_url = reverse('users:password-reset-confirm', args=[invalid_uid, self.token])
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Неверная ссылка восстановления пароля")

    def test_password_reset_confirm_renders_template(self):
        response = self.client.get(self.password_reset_confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/reset_confirm.html")


class SyncFileTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test', email="test@test.ru")
        self.client.login(username='test', password='test')
        self.valid_file = "simple_main.exe"
        self.invalid_file = "malicious.exe"
        self.url = lambda file_name: reverse('users:sync-file', args=[file_name])

    def test_sync_file_valid_existing(self):
        file_path = os.path.join("Documents", self.valid_file)
        os.makedirs("Documents", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(b"Dummy content")
        response = self.client.get(self.url(self.valid_file))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="file_name"')

    def test_sync_file_invalid(self):
        response = self.client.get(self.url(self.invalid_file))
        self.assertEqual(response.status_code, 404)

    def test_sync_file_valid_but_missing(self):
        file_path = os.path.join("Documents", self.valid_file)
        if os.path.exists(file_path):
            os.remove(file_path)
        response = self.client.get(self.url(self.valid_file))
        self.assertEqual(response.status_code, 404)


class TariffPageTests(TestCase):
    def setUp(self):
        self.client = self.client_class()
        self.user = User.objects.create_user(username="testuser", password="testpassword", email="test@test.com")
        self.client.login(username="testuser", password="testpassword")

        self.org = Organization.objects.create(user=self.user, payment=False)

        self.tariff_data = [
            TariffModel.objects.create(duration='monthly', user_count=50, price_per_user=100),
            TariffModel.objects.create(duration='annually', user_count=50, price_per_user=90),
            TariffModel.objects.create(duration='two_years', user_count=50, price_per_user=85),
            TariffModel.objects.create(duration='monthly', user_count=100, price_per_user=200),
            TariffModel.objects.create(duration='annually', user_count=100, price_per_user=180),
            TariffModel.objects.create(duration='two_years', user_count=100, price_per_user=170),
            TariffModel.objects.create(duration='monthly', user_count=250, price_per_user=200),
            TariffModel.objects.create(duration='annually', user_count=250, price_per_user=180),
            TariffModel.objects.create(duration='two_years', user_count=250, price_per_user=170),
            TariffModel.objects.create(duration='monthly', user_count=500, price_per_user=200),
            TariffModel.objects.create(duration='annually', user_count=500, price_per_user=180),
            TariffModel.objects.create(duration='two_years', user_count=500, price_per_user=170),
            TariffModel.objects.create(duration='monthly', user_count=1000, price_per_user=200),
            TariffModel.objects.create(duration='annually', user_count=1000, price_per_user=180),
            TariffModel.objects.create(duration='two_years', user_count=1000, price_per_user=170),
        ]
        self.tariff_url = reverse('users:choose-tariff-page')

    def test_get_tariff_page(self):
        response = self.client.get(self.tariff_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/choose_tariff_page.html')
        self.assertContains(response, 'Tariff duration')
        self.assertContains(response, 'Number of users')

    @patch('users.views.payment_helper')
    def test_post_valid_data(self, mock_payment_helper):
        mock_payment_helper.return_value = ('http://example.com/payment', 'payment_id_123')
        data = {'duration': 'monthly', 'user_count': 50}
        response = self.client.post(self.tariff_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://example.com/payment', fetch_redirect_response=False)
        payment_history = PaymentHistory.objects.get(user=self.user)
        self.assertEqual(payment_history.payment_id, 'payment_id_123')

    def test_post_invalid_data(self):
        data = {'duration': 'monthly', 'user_count': ''}
        response = self.client.post(self.tariff_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context, "Form is missing from response context")
        form = response.context['form']
        self.assertTrue(form.is_bound, "Form is not bound properly")
        self.assertFormError(form, 'user_count', 'Обязательное поле.')

    def test_organization_payment_required(self):
        self.org.payment = False
        self.org.save()
        response = self.client.get(self.tariff_url)
        self.assertEqual(response.status_code, 200)

    def test_organization_already_paid(self):
        self.org.payment = True
        self.org.save()
        response = self.client.get(self.tariff_url)
        self.assertRedirects(response, reverse('users:org-registration-process-info'))

    def test_organization_not_exists(self):
        self.client.logout()
        self.user.delete()
        new_user = User.objects.create_user(username="newuser", password="newpassword", email="newuser@test.com")
        self.client.login(username="newuser", password="newpassword")
        response = self.client.get(self.tariff_url)
        self.assertRedirects(response, reverse('users:org-registration-process-info'))

    @patch('users.views.payment_helper')
    def test_post_annually_tariff(self, mock_payment_helper):
        mock_payment_helper.return_value = ('http://example.com/payment', 'payment_id_123')
        data = {'duration': 'annually', 'user_count': 50}
        response = self.client.post(self.tariff_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://example.com/payment', fetch_redirect_response=False)
        expected_price = 90 * 50 * 12
        mock_payment_helper.assert_called_with(response.wsgi_request, expected_price)

    @patch('users.views.payment_helper')
    def test_post_two_years_tariff(self, mock_payment_helper):
        mock_payment_helper.return_value = ('http://example.com/payment', 'payment_id_456')
        data = {'duration': 'two_years', 'user_count': 50}
        response = self.client.post(self.tariff_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, 'http://example.com/payment', fetch_redirect_response=False)
        expected_price = 85 * 50 * 24
        mock_payment_helper.assert_called_with(response.wsgi_request, expected_price)

    def test_tariff_not_found(self):
        data = {'duration': 'monthly', 'user_count': 50}
        TariffModel.objects.filter(duration='monthly', user_count=50).delete()
        response = self.client.post(self.tariff_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tariff plan not found.")

    @patch('users.views.payment_helper')
    def test_unexpected_error(self, mock_payment_helper):
        with patch('users.views.TariffModel.objects.get', side_effect=Exception("Unexpected error")):
            data = {'duration': 'monthly', 'user_count': 50}
            response = self.client.post(self.tariff_url, data)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "An unexpected error occurred.")

