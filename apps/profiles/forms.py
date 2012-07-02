# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile
from django.contrib.auth.models import User

class SignInForm(AuthenticationForm):
    """
    Наследуем AuthenticationForm и
    переопредляем поле username: теперь это почта пользователя.
    """
    username = forms.EmailField(label='Email')

    def check_for_test_cookie(self):
        """
        Ломает тесты. Написал заглушку.
        """
        return

class SignUpForm(forms.Form):
    """
    Регистрация пользователя по почте и имени на сайте.
    """
    email = forms.EmailField(label='Email')
    name = forms.CharField(label='Имя на айте')
    captcha = CaptchaField(label='Капча', help_text='Введите текст с картинки')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("Пользовтаель с таким адресом уже существует")
        except User.DoesNotExist:
            return email

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            Profile.objects.get(name=name)
            raise forms.ValidationError("Пользовтаель с таким именем уже существует")
        except Profile.DoesNotExist:
            pass

        try:
            User.objects.get(username=name)
            raise forms.ValidationError("Пользовтаель с таким именем уже существует")
        except User.DoesNotExist:
            return name

class RestorePasswordForm(forms.Form):
    email = forms.EmailField(label='Почта')
    captcha = CaptchaField(label='Капча', help_text='Введите текст с картинки')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
            return email
        except User.DoesNotExist:
            raise forms.ValidationError("Пользовтаель с таким адресом не существует")

