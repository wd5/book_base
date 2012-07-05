# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import Http404
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from .models import Book, BookRead

LAST_LOOK_BOOK_COUNT = getattr(settings, 'LAST_LOOK_BOOK_COUNT', 10)

class BookList(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10

class BookSearch(BookList):
    pass

class BookDetail(DetailView):
    model = Book
    context_object_name = 'book'

    def get_object(self, queryset=None):
        obj=super(BookDetail, self).get_object(queryset=queryset)

        last_look_book=self.request.session.get('last_look_book', [])
        if len(last_look_book) >= LAST_LOOK_BOOK_COUNT:
            last_look_book.pop()
        try:
            last_look_book.remove(obj)
        except ValueError:
            pass
        last_look_book.insert(0, obj)

        self.request.session['last_look_book']=last_look_book
        self.request.session.save()

        return obj

class WillRead(View):
    http_method_names = ('post', )

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)

        if request.user.is_authenticated():
            BookRead.objects.get_or_create(user=request.user, book=book)
        else:
            read_ids = request.session.get('read_ids', {})
            book_id=int(book_id)
            read_ids[book_id]=True
            request.session['read_ids']=read_ids
            request.session.save()

        return render_to_response('books/includes/unread.html', {
            'book_id': book_id,
        }, context_instance=RequestContext(self.request))

class UnRead(View):
    http_method_names = ('post', )

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)

        if request.user.is_authenticated():
            try:
                book = BookRead.objects.get(user=request.user, book=book)
                book.delete()
            except BookRead.DoesNotExist:
                raise Http404
        else:
            read_ids = request.session.get('read_ids', {})
            book_id=int(book_id)
            del read_ids[book_id]
            request.session['read_ids']=read_ids
            request.session.save()

        return render_to_response('books/includes/will_read.html', {
            'book_id': book_id,
        }, context_instance=RequestContext(self.request))

class WillReadList(ListView):
    model = Book
    context_object_name = 'books'
    template_name = "books/user_read_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated():
            read_ids=BookRead.objects.filter(user=self.request.user).values('book__id')
        else:
            read_ids=self.request.session.get('read_ids', [])
        books = Book.objects.filter(id__in=read_ids)
        return books

class PrintOrder(View):
    """
    Распечатать формуляр.
    """
    pass