# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import BookList, BookDetail, BookSearch
from .views import WillReadList, WillRead, UnRead
from .views import PrintOrder, RenderOrderBookForm, MakeOrderBook

urlpatterns = patterns('',
    url(r'^$', BookList.as_view(), name='book_list'),
    url(r'^search/$', BookSearch.as_view(), name='book_search'),
    url(r'^will-read/$', WillReadList.as_view(), name='book_will_read_list'),
    url(r'^(?P<pk>\d+)/$', BookDetail.as_view(), name='book_detail'),
    url(r'^(?P<pk>\d+)/will-read/$', WillRead.as_view(), name='book_will_read_add'),
    url(r'^(?P<pk>\d+)/unread/$', UnRead.as_view(), name='book_unread'),
    url(r'^(?P<pk>\d+)/print-blank/$', PrintOrder.as_view(), name='print_order'),

    url(r'^order/render-form/$', RenderOrderBookForm.as_view(), name='order_book_render_form'),
    url(r'^order/make/$', MakeOrderBook.as_view(), name='order_book_make'),
)