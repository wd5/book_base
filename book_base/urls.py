# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from apps.simple_page.views import MainPage

urlpatterns = patterns('',
    url(r'^$', MainPage.as_view(), name='main_page'),

    url(r'^book/', include('apps.books.urls')),
    url(r'^profile/', include('apps.profiles.urls')),

    url(r'^captcha/', include('captcha.urls')),
    url(r'^ulogin/', include('django_ulogin.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/?', include('grappelli.urls')),
    url(r'^', include('apps.flatpages.urls')),
)