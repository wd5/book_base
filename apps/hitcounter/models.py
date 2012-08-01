# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import User

class HitCounter(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField('ID объекта')
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    hits = models.PositiveIntegerField('Кол-во просмотров', default=0)

class Hit(models.Model):
    hit = models.ForeignKey(HitCounter)
    ip = models.CharField(max_length=40, blank=True, null=True)
    session = models.CharField(max_length=40, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, related_name='hit_user', blank=True, null=True)