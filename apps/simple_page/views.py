# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView

from apps.books.models import Book

class MainPage(TemplateView):
    template_name = 'simple_page/main_page.html'

    def get_context_data(self, **kwargs):
        context=super(MainPage, self).get_context_data(**kwargs)
        context['latest_book']=Book.objects.order_by('-update')
        return context
