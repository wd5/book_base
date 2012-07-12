# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import BookList, BookDetail
from .views import BookBlank, BookBlankFromBookmark
from .views import BookmarkList, BookmarkAdd, BookmarkDel, BookmarkDelAll
from .views import RenderOrderBookForm, MakeOrderBook, CancelOrderBook

urlpatterns = patterns('',
    url(r'^$', BookList.as_view(), name='book_list'),
    url(r'^(?P<pk>\d+)/$', BookDetail.as_view(), name='book_detail'),
    url(r'^(?P<pk>\d+)/blank/$', BookBlank.as_view(), name='book_blank'),

    url(r'^bookmark/$', BookmarkList.as_view(), name='bookmark_list'),
    url(r'^bookmark/add/$', BookmarkAdd.as_view(), name='bookmark_add'),
    url(r'^bookmark/del/$', BookmarkDel.as_view(), name='bookmark_del'),
    url(r'^bookmark/del/all/$', BookmarkDelAll.as_view(), name='bookmark_del_all'),
    url(r'^bookmark/print-all/$', BookBlankFromBookmark.as_view(), name='bookmarks_print_all'),
#
    url(r'^order/form/$', RenderOrderBookForm.as_view(), name='order_form'),
    url(r'^order/make/$', MakeOrderBook.as_view(), name='order_make'),
    url(r'^order/calcel/$', CancelOrderBook.as_view(), name='order_cancel'),
)