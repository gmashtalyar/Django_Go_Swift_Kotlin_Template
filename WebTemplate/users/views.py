import json
import os
from typing import Any, Dict, List, Optional, Union

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

from main_app.models import BusinessLogic
from WebTemplate import settings
from .decorators import allowed_users, organization_payment_required
from .forms import SignUpForm, LoginForm, UserDataChangeForm, OrgCreationForm, AddUserForm, DemoForm, TariffForm, \
    FeedbackCommentsForm, NotificationsForm
from .helpers import payment_helper, check_payment
from .models import Organization, TariffModel, PaymentHistory, EmailNotificationSettings, WebNotifications


@csrf_exempt
def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')


def password_reset_request(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        email = request.POST['email'].lower()
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f"password_reset/reset/{uid}/{token}/")
            subject = "ХХХХХХ: Восстановление пароля"
            message = render_to_string("users/reset_email.html", {
                "user": user,
                "reset_url": reset_url})
            send_mail(subject, None, settings.DEFAULT_FROM_EMAIL, [email], html_message=message)
            messages.success(request, "Ссылка для восстановления пароля направлена на почту.")
            return redirect("users:password-reset-request")
        else:
            messages.error(request, "Пользователь с такой почтой не нашелся.")
    return render(request, "users/reset_request.html")


def password_reset_confirm(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user: Optional[User] = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            messages.success(request, "Пароль обновлен успешно. Можете войти с новым паролем.")
            return redirect('/accounts/login/')
        return render(request, "users/reset_confirm.html")
    else:
        messages.error(request, "Неверная ссылка восстановления пароля.")
        return HttpResponse("Неверная ссылка восстановления пароля")


@login_required
def change_user_data(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserDataChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserDataChangeForm(instance=request.user)
    return render(request, "users/change_user_data.html", {"form": form})


@login_required
def organization_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = OrgCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['corporate_email']
            email_parts = email.split('@')
            if len(email_parts) != 2:
                form.add_error('corporate_email', 'Введите действительный адрес корпоративной электронной почты.')
            elif Organization.objects.filter(user=request.user).exists():
                form.add_error("org", 'Вы уже создали организацию. Чтобы создать новую - зарегистрируйтесь с другой корпоративной почтой.')
            else:
                Organization.objects.create(org=form.cleaned_data['org'], corporate_email=email_parts[1].lower(), user_id=request.user.id)
                groups_to_assign = [Group.objects.get(name='org_admin'), Group.objects.get(name='data_contributor'), Group.objects.get(name='viewer'), Group.objects.get(name='dashboard_creator')]
                request.user.groups.add(*groups_to_assign)
                return redirect(reverse('users:company-properties'))
        return render(request, 'users/create_organization.html', {'form': form})
    else:
        form = OrgCreationForm()
    return render(request, 'users/create_organization.html', {'form': form})


@allowed_users(allowed_roles=['org_admin'])
def organization_add_users(request: HttpRequest, org_id: int) -> HttpResponse:
    org = Organization.objects.get(pk=org_id)
    user_emails = [user.email for user in User.objects.filter(email__endswith=org.corporate_email).exclude(pk=org.user_id)]
    if request.method == 'POST':
        form = AddUserForm(request.POST, user_emails=user_emails, organization=org)
        if form.is_valid():
            form.save(organization=org.org)
            return redirect(reverse('users:company-properties'))
        else:
            return render(request, 'users/organization_add_users.html', {'form': form})
    else:
        form = AddUserForm(user_emails=user_emails, organization=org)
    return render(request, 'users/organization_add_users.html', {'form': form})


@allowed_users(allowed_roles=['org_admin'])
def org_settings(request: HttpRequest) -> HttpResponse:
    org = Organization.objects.get(user_id=request.user.id)
    return render(request, 'users/org_settings.html', {"org": org})


@login_required
def company_properties(request: HttpRequest) -> HttpResponse:
    org = Organization.objects.get(user_id=request.user.id)
    users = Organization.objects.filter(org=org.org)
    return render(request, 'users/company_properties.html', {"org": org, "users": users})


@login_required
def cabinet(request: HttpRequest) -> HttpResponse:
    try:
        org: Optional[Organization] = Organization.objects.get(user_id=request.user.id)
        user_organizations = Organization.objects.filter(user=request.user)
        dashboards = BusinessLogic.objects.filter(user__in=user_organizations.values('user'))
    except:
        org = None
        dashboards = None
    return render(request, 'users/cabinet.html', {"org": org, "dashboards": dashboards})


def tariff_plan(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/tariff_plan.html')


def demo_booking(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DemoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = DemoForm()
    return render(request, 'users/demo_booking.html', {'form': form})


def ask_signup(request: HttpRequest) -> HttpResponse:
     return render(request, 'users/ask_signup.html')


def payment_success_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/payment_success_page.html')


def org_registration_process_info(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/org_registration_process_info.html')


@organization_payment_required
def choose_tariff_page(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TariffForm(request.POST)
        if form.is_valid():
            duration = form.cleaned_data['duration']
            user_count = form.cleaned_data['user_count']
            try:
                tariff_plan_instance = TariffModel.objects.get(duration=duration, user_count=user_count)
                base_price = tariff_plan_instance.price_per_user * int(user_count)
                if duration == 'annually':
                    total_price = base_price * 12
                elif duration == 'two_years':
                    total_price = base_price * 24
                else:
                    total_price = base_price
                url, payment_id = payment_helper(request, total_price)
                PaymentHistory.objects.create(user=request.user, payment_id=payment_id)
                return HttpResponseRedirect(url)
            except TariffModel.DoesNotExist:
                form.add_error(None, "Tariff plan not found.")
                return render(request, 'users/choose_tariff_page.html', {'form': form})
            except Exception as e:
                print(e)
                form.add_error(None, "An unexpected error occurred.")
                return render(request, 'users/choose_tariff_page.html', {'form': form})
        else:
            return render(request, 'users/choose_tariff_page.html', {"form": form})
    else:
        form = TariffForm()
    prices = {user_count: {duration: TariffModel.objects.filter(user_count=user_count, duration=duration).first().price_per_user for duration, _ in TariffModel.duration_choices}for user_count, _ in TariffModel.user_count_choices}
    return render(request, 'users/choose_tariff_page.html', {"form": form, "prices_json": json.dumps(prices)})


def payment_return_page(request: HttpRequest) -> HttpResponse:
    payment_history = PaymentHistory.objects.filter(user=request.user).last()
    check = check_payment(payment_history)
    if check:
        return render(request, 'users/payment_success_page.html')
    else:
        return render(request, 'users/payment_failure_page.html')


def oferta(request: HttpRequest) -> HttpResponse:
    file_path = os.path.join("Documents", 'oferta.pdf')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="oferta.pdf"'
        return response
    else:
        raise Http404('The oferta policy file does not exist.')


def privacy_policy(request: HttpRequest) -> HttpResponse:
    file_path = os.path.join("Documents", 'privacy_policy.pdf')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="privacy_policy.pdf"'
        return response
    else:
        raise Http404('The privacy policy file does not exist.')


def feedback(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = FeedbackCommentsForm(request.POST)
        if form.is_valid():
            data = form.save()
            send_mail("Обратная связь", None, 'ХХХХХХ@fintechdocs.ru', ['ХХХХХХ@fintechdocs.ru'], html_message=data.comment)
            return HttpResponseRedirect("/")
    else:
        form = FeedbackCommentsForm()
    context = {'form': form}
    return render(request, 'users/feedback.html', context)


def error(request: HttpRequest, exception: Optional[Any] = None, status_code: Optional[int] = None) -> HttpResponse:
    return render(request, "users/error.html", status=404)


@allowed_users(allowed_roles=['org_admin'])
def user_management(request: HttpRequest) -> HttpResponse:
    org = Organization.objects.get(user_id=request.user.id)
    user_organizations = Organization.objects.filter(org=org.org, corporate_email=org.corporate_email)
    if not user_organizations.exists():
        processed_users: List[Dict[str, Any]] = []
    else:
        user_ids = user_organizations.values_list('user_id', flat=True)
        users = User.objects.filter(id__in=user_ids).prefetch_related('groups')
        processed_users = []
        for user in users:
            user_data = {'user': user, 'is_viewer': user.groups.filter(name='viewer').exists(),
                'is_dashboard_creator': user.groups.filter(name='dashboard_creator').exists(),
                'is_data_contributor': user.groups.filter(name='data_contributor').exists(),
                'is_external_user': user.groups.filter(name='external_user').exists()}
            processed_users.append(user_data)
    return render(request, 'users/user_management.html', {"org": org, "users": processed_users})


@allowed_users(allowed_roles=['org_admin'])
def assign_group(request: HttpRequest, user_id: int, group_name: str) -> HttpResponse:
    user = get_object_or_404(User, id=user_id)
    group = Group.objects.get(name=group_name)
    if group not in user.groups.all():
        user.groups.add(group)
    return redirect('users:user-management')


@allowed_users(allowed_roles=['org_admin'])
def remove_group(request: HttpRequest, user_id: int, group_name: str) -> HttpResponse:
    user = get_object_or_404(User, id=user_id)
    group = get_object_or_404(Group, name=group_name)
    if group in user.groups.all():
        user.groups.remove(group)
    return redirect('users:user-management')


# @cache_page(60 * 60 * 24 * 7)
def faq(request: HttpRequest) -> HttpResponse:
    return render(request, 'users/faq.html')


def download_android_app(request: HttpRequest) -> HttpResponse:
    file_path = "/app/Documents/app.apk"
    if not os.path.exists(file_path):
        raise Http404("File not found")
    with open(file_path, 'rb') as file:
        file_data = file.read()
        file_content = ContentFile(file_data)
    response = HttpResponse(file_content, content_type='application/vnd.android.package-archive')
    response['Content-Disposition'] = f'attachment; filename="app.apk"'
    return response


@login_required
def notification_preferences(request: HttpRequest) -> HttpResponse:
    settings, created = EmailNotificationSettings.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = NotificationsForm(request.POST, instance=settings)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect("/")
    else:
        form = NotificationsForm(instance=settings)
    return render(request, "users/notification_preferences.html", {"form": form, "email": request.user.email})


@login_required()  # todo: test ()
def user_settings(request: HttpRequest) -> HttpResponse:
    user = User.objects.get(id=request.user.id)
    try:
        preferences: Union[EmailNotificationSettings, str] = EmailNotificationSettings.objects.get(user_id=request.user.id)
    except:
        preferences = "no_preferences"
    return render(request, 'main/settings.html', {'user': user, "preferences": preferences})


@login_required
def show_notifications(request: HttpRequest) -> HttpResponse:
    notifications = WebNotifications.objects.filter(is_new=True, user_id=request.user.id)
    notifications_count = notifications.count()

    context = {"notifications": notifications, "notifications_count": notifications_count}
    return render(request, 'user/show_notifications.html', context)


@login_required
def clear_notifications(request: HttpRequest) -> HttpResponse:
    WebNotifications.objects.filter(user=request.user.id).update(is_new=False)
    return HttpResponseRedirect("accounts/show-notifications/")