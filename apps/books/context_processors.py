# -*- coding: utf-8 -*-

def last_read(request):
    return {
        'last_look_book': request.session.get('last_look_book', []),
    }