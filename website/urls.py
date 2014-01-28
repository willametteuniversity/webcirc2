from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
    url(r'^collections/$', 'collectionList'),
    url(r'^collections/?P<pk>[0-9]+)/$', 'collectionDetail')
)