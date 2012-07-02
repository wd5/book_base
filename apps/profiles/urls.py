# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from .views import logout_view, SignInUser, SignUpUser, RestorePassword

urlpatterns = patterns('',
    url(r'^signup/$', SignUpUser.as_view(), name='profile_signup'),
    url(r'^signin/$', SignInUser.as_view(), name='profile_signin'),
    url(r'^signout/$', logout_view, name='profile_signout'),
    url(r'^restore/$', RestorePassword.as_view(), name='profile_restore'),
)