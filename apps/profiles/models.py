# -*- coding: utf-8 -*-

import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django_ulogin.signals import assign
from django_ulogin.models import ULoginUser

class Profile(models.Model):
    """
    Профиль пользовател
    """
    user = models.OneToOneField(User)
    name = models.CharField('Имя на сайте', max_length=64, default='')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

def catch_ulogin_signal(*args, **kwargs):
    json=kwargs['ulogin_data']
    user=kwargs['user']

    if kwargs['registered']:
        user.user_name = 'social_' + str(uuid.uuid1())[:10]
        user.first_name=json.get('first_name', '')
        user.last_name=json.get('last_name', '')
        user.email=json.get('email', '')
        user.save()

        profile, created = Profile.objects.get_or_create(user=user)

        profile.name=json.get('nickname') or '%s %s' % (user.first_name, user.last_name)
        profile.save()

        password = str(uuid.uuid1())[:7]
        user.set_password(password)
        user.save()

        context = {
            'email': user.email,
            'password': password,
            'sitename': Site.objects.get_current().domain,
        }

        from_email = settings.EMAIL_ADDRESS_FROM
        to = user.email
        subject = render_to_string('profiles/email/registration_subject.txt', context)
        text_content = render_to_string('profiles/email/registration_content.txt', context)
        html_content = render_to_string('profiles/email/registration_content.html', context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to, ])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

assign.connect(receiver=catch_ulogin_signal, sender=ULoginUser, dispatch_uid='profiles.models')