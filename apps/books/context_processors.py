# -*- coding: utf-8 -*-

from .models import Genre

def last_read(request):
    return {
        'last_look_book': request.session.get('last_look_book', []),
    }