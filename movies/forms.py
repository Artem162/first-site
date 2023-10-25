from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import *


# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label="Заголовок",
#                             widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label="URL")
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
#     is_published = forms.BooleanField(label="Опубліковано?", required=False, initial=True)
#     cat = forms.ModelChoiceField(queryset=Category.objects.all(),
#                                  label="Категорія",
#                                  empty_label="Категорію не обрано"
#                                  )
class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категорію не обрано"

    class Meta:
        model = Movie
        # fields = '__all__'
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})
        }


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Email:', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор паролю:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        # НЕ ОБОВ'ЯЗКОВО
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-input'}),
        #     'email': forms.TextInput(attrs={'class': 'form-input'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        # }

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if len(title) > 200:
    #         raise ValidationError('Довжина перевищує 200 символів')
    #     return title


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label="ім'я", max_length=255)
    email = forms.CharField(label='Email:', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
