# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import FormView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from annoying.functions import get_object_or_None
from django.contrib.auth.signals import user_logged_in

from .forms import MakeOrderForm
from .models import Book, Bookmark, Library, OrderBook

LAST_LOOK_BOOK_COUNT = getattr(settings, 'LAST_LOOK_BOOK_COUNT', 10)

class BookList(ListView):
    model = Book
    context_object_name = 'books'
    paginate_by = 10

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

class BookBlank(DetailView):
    """
    Распечатать формуляр.
    """
    model = Book
    template_name = 'books/book_blank.html'
    context_object_name = 'book'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BookBlank, self).dispatch(request, *args, **kwargs)

class BookmarkList(ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'books'
    template_name = 'books/bookmark_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated():
            bookmarks_id=Bookmark.objects.filter(user=self.request.user).values('book__id')
        else:
            bookmarks_id=self.request.session.get('bookmarks_id', [])
        books = Book.objects.filter(id__in=bookmarks_id)
        return books

class BookmarkAdd(View):
    http_method_names = ('post', )

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)

        if request.user.is_authenticated():
            Bookmark.objects.get_or_create(user=request.user, book=book)
        else:
            bookmarks_id = request.session.get('bookmarks_id', {})
            book_id=int(book_id)
            bookmarks_id[book_id]=True
            request.session['bookmarks_id']=bookmarks_id
            request.session.save()

        return render_to_response('books/includes/bookmark_button_del.html', {
            'book_id': book_id,
        }, context_instance=RequestContext(self.request))

class BookmarkDelAll(View):
    http_method_names = ('post', )

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            Bookmark.objects.filter(user=request.user).delete()
        else:
            request.session['bookmarks_id']={}
            request.session.save()

        return HttpResponse('')

class BookmarkDel(View):
    http_method_names = ('post', )

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, pk=book_id)

        if request.user.is_authenticated():
            try:
                book = Bookmark.objects.get(user=request.user, book=book)
                book.delete()
            except Bookmark.DoesNotExist:
                raise Http404
        else:
            bookmarks_id = request.session.get('bookmarks_id', {})
            book_id=int(book_id)
            del bookmarks_id[book_id]
            request.session['bookmarks_id']=bookmarks_id
            request.session.save()

        return render_to_response('books/includes/bookmark_button_add.html', {
            'book_id': book_id,
        }, context_instance=RequestContext(self.request))

class BookBlankFromBookmark(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/book_blank.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BookBlankFromBookmark, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        books_pk = Bookmark.objects.filter(user=self.request.user).values_list('book__pk', flat=True)
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
    template_name = 'books/order_complite.html'
    http_method_names = ('post', )
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
        order.save()

        return render_to_response('books/order_complite.html', {
            'order': order,
        }, context_instance=RequestContext(self.request))

class CancelOrderBook(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CancelOrderBook, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(OrderBook,
            pk=request.POST.get('order_id'),
            user=request.user,
        )
        order.delete()

        return render_to_response('books/includes/order_cancel.html', {

        }, context_instance=RequestContext(self.request))


def user_login_handler(sender, **kwargs):
    user = kwargs['user']
    request = kwargs['request']

    for id in request.session.get('bookmarks_id', {}):
        book = get_object_or_None(Book, pk=id)
        if not book:
            continue
        Bookmark.objects.get_or_create(user=user, book=book)

user_logged_in.connect(user_login_handler)