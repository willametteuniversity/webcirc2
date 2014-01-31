from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('website.views',
                       url(r'^collections/$', 'collectionList'),
                       url(r'^collections/(?P<pk>[0-9]+)$', 'collectionDetail'),
                       url(r'^labels/$', 'labelList'),
                       url(r'^labels/(?P<pk>[0-9]+)$', 'labelDetail'))

urlpatterns = format_suffix_patterns(urlpatterns)
