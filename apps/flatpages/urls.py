from django.conf.urls import patterns, url

urlpatterns = patterns('apps.flatpages.views',
    (r'^(?P<url>.*)$', 'flatpage'),
)