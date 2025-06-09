from django import forms
from .models import Documents, FeedbackComments, BusinessLogic, SomeChoices
from django.conf import settings
from django.contrib.auth.models import User


class SomeForm(forms.ModelForm):
    short_text = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Это поле не может быть пустым'}))
    long_text = forms.CharField(label="Описание компании", widget=forms.Textarea(attrs={'rows':4, 'cols':80, 'placeholder': 'Продукты, объекты\nРегионы продаж и производства\nKлиенты компании', "class": "form-control"}))
    choice_field = forms.ChoiceField(choices=SomeChoices, widget=forms.Select(attrs={'class': 'form-control'}), required=True,)
    model_choice = forms.ModelChoiceField(queryset=BusinessLogic.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    integer_field = forms.IntegerField(label="Срок отсрочки в к.д.", required=True)
    boolean_field = forms.BooleanField(label="Публичный доступ", required=False)


    class Meta:
        model = BusinessLogic
        fields = ["short_text", "long_text", "choice_field", "integre_field"]



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class DocumentsForm(forms.Form):
    document = MultipleFileField()

    class Meta:
        model = Documents
        fields = ['document']


class FeedbackCommentsForm(forms.ModelForm):
    company = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша компания'}))
    email = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваша почта'}))
    comment = forms.CharField(label="Сообщение")
    class Meta:
        model = FeedbackComments
        fields = ['email', 'company', 'comment']
