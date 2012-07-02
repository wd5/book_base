# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView

from .models import Book

class BookList(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 20

class BookSearch(BookList):
    template_name = ''

class BookDetail(DetailView):
    model = Book
    context_object_name = 'book'


class TakeBook(CreateView):
    model = Book

class RefuseBook(View):
    http_method_names = ('post', )

    def post(self):
        if self.request.user.is_authenticated():
            pass
        else:
            pass

class PrintOrder(View):
    """
    Распечатать формуляр.
    """