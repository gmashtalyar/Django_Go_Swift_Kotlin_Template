from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group
from .models import Organization, Demo, TariffModel, FeedbackComments, BusinessModelComments
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Имя", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Фамилия", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Рабочая почта", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Этот email уже зарегистрирован. Если вы забыли пароль, вы можете <a href='accounts/password_reset_request/'>восстановить его</a>.")
        return email

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email'].lower()

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserDataChangeForm(UserChangeForm):
    email = forms.EmailField(label="Корпоративная почта", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name']

    def clean_email(self):
        return self.cleaned_data['email'].lower()


class OrgCreationForm(forms.Form):
    org = forms.CharField(label="Название организации", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    corporate_email = forms.CharField(label="Корпоративная почта", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Organization
        fields = ['org', 'corporate_email']


class AddUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user_emails = kwargs.pop('user_emails', [])
        self.organization = kwargs.pop('organization', None)
        super(AddUserForm, self).__init__(*args, **kwargs)
        for email in self.user_emails:
            is_added = Organization.objects.filter(org=self.organization.org, corporate_email=email).exists()
            self.fields[email] = forms.BooleanField(label=email, required=False, initial=is_added)

    def is_valid(self):
        if any(email for email in self.data if email not in self.user_emails and email != "csrfmiddlewaretoken"):
            return False
        return super().is_valid()

    def save(self, organization):
        viewer_group = Group.objects.get(name='viewer')
        for email, value in self.cleaned_data.items():
            user = User.objects.get(email=email)
            if value:
                check = Organization.objects.filter(user=user).count()
                if not check:
                    Organization.objects.create(org=organization, corporate_email=email, user=user)
                    user.groups.add(viewer_group)
            else:
                Organization.objects.filter(user=user, org=organization).delete()
                user.groups.remove(viewer_group)


class DemoForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    company_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(required=False, label="Сообщение", widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Пожелание ко встрече', "class": "form-control"}))
    channel = forms.CharField(required=False, label="Как вы о нас узнали?", widget=forms.Textarea(attrs={'rows':4, 'cols':40, 'placeholder': 'Подскажите, откуда вы о нас узнали?', "class": "form-control"}))

    class Meta:
        model = Demo
        fields = "__all__"


class TariffForm(forms.Form):
    duration = forms.ChoiceField(choices=TariffModel.duration_choices, label="Срок тарифа ", required=True)
    user_count = forms.ChoiceField(choices=TariffModel.user_count_choices, label="Кол-во пользователей", required=True)


class FeedbackCommentsForm(forms.ModelForm):
    company = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша компания'}))
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша почта'}))
    comment = forms.CharField(label="Сообщение")

    class Meta:
        model = FeedbackComments
        fields = ['email', 'company', 'comment']


class ItemCommentForm(forms.ModelForm):
    comment = forms.CharField(label="Новый комментарий", widget=forms.Textarea(attrs={'rows': 4, 'cols': 6}))

    class Meta:
        labels = {'comment': "Новый комментарий"}
        model = BusinessModelComments
        fields = ['comment']
