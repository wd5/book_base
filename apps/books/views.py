# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from annoying.functions import get_object_or_None

from .forms import MakeOrderForm
from .models import Book, BookRead, Library, OrderBook

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

class PrintOrder(DetailView):
    """
    Распечатать формуляр.
    """
    model = Book
    template_name = 'books/order_blank.html'
    context_object_name = 'book'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrintOrder, self).dispatch(request, *args, **kwargs)

class PrintBookmark(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/order_blank.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PrintBookmark, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        books_pk = BookRead.objects.filter(user=self.request.user).values_list('book__pk', flat=True)
        return Book.objects.filter(pk__in=books_pk).order_by('name')

class RenderOrderBookForm(View):
    """
    Вывод формы для заказа книги
    """
    def post(self, request, *args, **kwargs):
        return render_to_response('books/order_form.html', {
            'libraries': Library.objects.all(),
            'book': get_object_or_404(Book, pk=request.POST.get('book_id')),
        }, context_instance=RequestContext(self.request))

class MakeOrderBook(FormView):
    """
    Заказать книгу
    """
    template_name = 'books/includes/order_queue.html'
    form_class = MakeOrderForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(MakeOrderBook, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        exist_order=get_object_or_None(OrderBook,
            user=self.request.user,
            book=get_object_or_404(Book, pk=self.request.POST.get('book')),
            library=get_object_or_404(Library, pk=self.request.POST.get('library')),
        )
        if exist_order:
            raise Http404

        order = form.save(commit=False)
        order.user = self.request.user
        order.queue_num = OrderBook.objects.filter(book=order.book).count() + 1
        order.save()

        return render_to_response('books/includes/order_queue.html', {
            'queue_num': order.queue_num,
        }, context_instance=RequestContext(self.request))


class CancelOrderBook(View):
    """
    Отменить заказ книги
    """
    def post(self, request, *args, **kwargs):
        pass