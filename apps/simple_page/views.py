# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView

class MainPage(TemplateView):
    template_name = 'simple_page/main_page.html'
