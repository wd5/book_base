# -*- coding: utf-8 -*-

from .models import Genre

def get_genries(request):
    return {
        'genries': Genre.objects.all(),
    }