from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('website.views',
                       url(r'^collections/$', 'collectionList'),
                       url(r'^collections/(?P<pk>[0-9]+)$', 'collectionDetail'))

urlpatterns = format_suffix_patterns(urlpatterns)
