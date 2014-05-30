from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^users/$', 'userAPIViews.userList'),
                       url(r'^users/(?P<pk>[0-9]+)$', 'userAPIViews.userDetail'),
                       url(r'^users/(?P<em>.+@.+)$', 'userAPIViews.userDetail'),
                       url(r'^users/(?P<fn>.+ .+)$', 'userAPIViews.userDetail'),
                       url(r'^users/(?P<n>.+)$', 'userAPIViews.userDetail'),)