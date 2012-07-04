# -*- coding: utf-8 -*-

from django.http import Http404
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from .models import Book, BookRead

class BookList(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10

class BookSearch(BookList):
    pass

class BookDetail(DetailView):
    model = Book
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        book_id=self.kwargs.get('pk')
        book = get_object_or_404(Book, pk=book_id)

        is_read = False
        if self.request.user.is_authenticated():
            # TODO: переписать с использоватнием get_or_none
            try:
                BookRead.objects.get(user=self.request.user, book=book)
                is_read=True
            except BookRead.DoesNotExist:
                pass
        else:
            book_reaad=self.request.session.get('book_reaad', {})
            if book_id in book_reaad:
                is_read=True

        context=super(BookDetail, self).get_context_data(**kwargs)
        context['is_read']=is_read
        return context

class WillRead(View):
    http_method_names = ('post', )

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)

        if request.user.is_authenticated():
            BookRead.objects.get_or_create(user=request.user, book=book)
        else:
            book_reaad = request.session.get('book_reaad', {})
            book_reaad[book_id]=True
            request.session['book_reaad']=book_reaad
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
            book_reaad = request.session.get('book_reaad', {})
            del book_reaad[book_id]
            request.session['book_reaad']=book_reaad
            request.session.save()

        return render_to_response('books/includes/will_read.html', {
            'book_id': book_id,
        }, context_instance=RequestContext(self.request))

class PrintOrder(View):
    """
    Распечатать формуляр.
    """