# -*- coding: utf-8 -*-

import re

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')[:255]

IP_RE = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
def get_ip_address(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))

    if ip_address:
        try:
            ip_address = IP_RE.match(ip_address)
            if ip_address:
                ip_address = ip_address.group(0)
        except IndexError:
            return

    return ip_address

def check_allow_apps(app_name, model_name, allow_apps):
    """
    Проверка разрешены ли комментарии к данной сущности.
    Пример структуры:
        allow_apps = [
            {
                'app_name': 'news',
                'model_name': 'usernews',
            },
        ]
    """
    if app_name is None or model_name is None:
        return False
    for app in allow_apps:
        if app['app_name'] == app_name and app['model_name'] == model_name:
            return True
    return False