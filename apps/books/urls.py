# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import BookList, BookDetail, BookSearch
from .views import WillRead, UnRead
from .views import PrintOrder

urlpatterns = patterns('',
    url(r'^$', BookList.as_view(), name='book_list'),
    url(r'^search/$', BookSearch.as_view(), name='book_search'),
    url(r'^(?P<pk>\d+)/$', BookDetail.as_view(), name='book_detail'),
    url(r'^(?P<pk>\d+)/will-read/$', WillRead.as_view(), name='book_will_read'),
    url(r'^(?P<pk>\d+)/unread/$', UnRead.as_view(), name='book_unread'),
    url(r'^(?P<pk>\d+)/print-order/$', PrintOrder.as_view(), name='print_order'),
)
