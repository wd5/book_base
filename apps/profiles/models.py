# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from django_ulogin.signals import assign
from django_ulogin.models import ULoginUser

class Profile(models.Model):
    """
    Профиль пользовател
    """
    user = models.OneToOneField(User)
    name = models.CharField('Имя на сайте', max_length=64, default='')
    discount = models.PositiveSmallIntegerField('Скидка %', default=0)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

def catch_ulogin_signal(*args, **kwargs):
    json=kwargs['ulogin_data']
    user=kwargs['user']

    if kwargs['registered']:
        user.first_name=json.get('first_name', '')
        user.last_name=json.get('last_name', '')
        user.email=json.get('email', '')
        user.save()

        nickname=json.get('nickname') or '%s %s' % (user.first_name, user.last_name)
        profile = Profile(
            user=user,
            name=nickname
        )
        profile.save()

        # TODO: генерить пароль и отправлять на почту

assign.connect(receiver=catch_ulogin_signal, sender=ULoginUser, dispatch_uid='profiles.models')