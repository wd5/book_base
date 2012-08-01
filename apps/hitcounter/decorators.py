# -*- coding: utf-8 -*-

from functools import wraps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from .utils import get_ip_address, get_user_agent

from .models import Hit, HitCounter

ip_limited = getattr(settings, 'HITCOUNTER_IP_LIMITED', 5)

def _hit_entity(request, app_name, model_name, entity_id):
    type = ContentType.objects.get(app_label=app_name, model=model_name)
    hitcounter, created = HitCounter.objects.get_or_create(
        content_type=type,
        object_id=entity_id
    )

    user_agent = get_user_agent(request)
    ip_address = get_ip_address(request)

    def _update_hit(hit, created):
        if created:
            hit.ip = ip_address
            hit.user_agent = user_agent
            hit.session = request.session.session_key
            hit.save()

            hitcounter.hits += 1
            hitcounter.save()

    if request.user.is_authenticated():
        hit, created = Hit.objects.get_or_create(
            hit=hitcounter,
            user=request.user
        )
        _update_hit(hit, created)
    else:
        hit_count = Hit.objects.filter(ip=ip_address, user_agent=user_agent).count()
        if hit_count < ip_limited:
            hit, created = Hit.objects.get_or_create(
                hit=hitcounter,
                session=request.session.session_key
            )
            _update_hit(hit, created)

def hit_entity(app_name, model_name):
    """
    Просмотр сущности.
    Именованный аргумент pk обязателен!
    """
    def inner_decorator(fn):
        def wrapped(entity, request, *args, **kwargs):
            try:
                _hit_entity(request, app_name, model_name, kwargs.get('pk'))
                return fn(entity, request, *args, **kwargs)
            except :
                raise Http404
        return wraps(fn)(wrapped)
    return inner_decorator
