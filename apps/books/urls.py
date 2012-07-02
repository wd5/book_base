# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import BookList, BookDetail, BookSearch
from .views import TakeBook, RefuseBook
from .views import PrintOrder

urlpatterns = patterns('',
    url(r'^$', BookList.as_view(), name='book_list'),
    url(r'^search/$', BookSearch.as_view(), name='book_search'),
    url(r'^(?P<pk>\d+)/$', BookDetail.as_view(), name='book_detail'),
    url(r'^(?P<pk>\d+)/take/$', TakeBook.as_view(), name='book_take'),
    url(r'^(?P<pk>\d+)/refuse/$', RefuseBook.as_view(), name='book_refuse'),
    url(r'^(?P<pk>\d+)/print-order/$', PrintOrder.as_view(), name='print_order'),

#    url(r'bookmark/$', , name='bookmark_list'),
#    url(r'bookmark/(?P<book_id>\d+)/add-to-bookmark/$', , name='bookmark_add'),
#    url(r'bookmark/((?P<pk>\d+)/remove/$', , name='bookmark_renove'),
)
