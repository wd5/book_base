# -*- coding: utf-8 -*-

import uuid
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .forms import SignUpForm, SignInForm, RestorePasswordForm

from .models import Profile
from django.contrib.auth.models import User

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

class SignUpUser(FormView):
    form_class = SignUpForm
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'profiles/signup.html'

    def form_valid(self, form):
        cd = form.cleaned_data
        name = cd['name']
        email = cd['email']

        # Регистрация пользователя
        password = uuid.uuid4().hex[:8]
        username = 'regform_' + uuid.uuid4().hex[:8]
        user, created = User.objects.get_or_create(email=email)

        user.username=username
        user.is_active=True
        user.set_password(password)
        user.save()

        # Создание профиля
        profile,created=Profile.objects.get_or_create(user=user)
        profile.name=name
        profile.save()

        user = authenticate(username=username, password=password)
        login(self.request, user)

        context = {
            'email': user.email,
            'password': password,
            'sitename': Site.objects.get_current().domain,
        }

        from_email = settings.EMAIL_ADDRESS_FROM
        to = user.email
        subject = render_to_string('profiles/email/signup_subject.txt', context)
        text_content = render_to_string('profiles/email/signup_content.txt', context)
        html_content = render_to_string('profiles/email/signup_content.html', context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to, ])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponseRedirect(self.success_url)


class SignInUser(FormView):
    form_class = SignInForm
    template_name = 'profiles/signin.html'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        cd = form.cleaned_data

        username = cd['username']
        password = cd['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())

        return render_to_response(self.template_name,
        {
            'form': form,
        }, context_instance=RequestContext(self.request))

class RestorePassword(FormView):
    form_class = RestorePasswordForm
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'profiles/restore.html'

    def form_valid(self, form):
        subject = render_to_string('profiles/email/restore_subject.txt')
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = form.cleaned_data['email']

        # Смена пароля
        new_password = uuid.uuid4().hex[:8]
        user = User.objects.get(email=to_email)
        user.set_password(new_password)
        user.save()

        context = {
            'email': to_email,
            'new_password': new_password,
            'sitename': Site.objects.get_current().domain,
        }
        html_content = render_to_string('profiles/email/restore_content.html', context)
        text_content = render_to_string('profiles/email/restore_content.txt', context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email, ])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return HttpResponseRedirect(self.success_url)