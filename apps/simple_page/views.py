# -*- coding: utf-8 -*-

from django.views.generic.base import TemplateView
from django.contrib.contenttypes.models import ContentType

from apps.books.models import Book
from apps.hitcounter.models import HitCounter

class MainPage(TemplateView):
    template_name = 'simple_page/main_page.html'

    def _get_popular(self):
        ct = ContentType.objects.get_for_model(Book)
        book_ids = HitCounter.objects.filter(content_type=ct).order_by('-hits').values_list('object_id', flat=True)
        books = Book.objects.filter(pk__in=book_ids)[:8]
        return books

    def get_context_data(self, **kwargs):
        context=super(MainPage, self).get_context_data(**kwargs)
        context['books_popular']=self._get_popular()
        return context
