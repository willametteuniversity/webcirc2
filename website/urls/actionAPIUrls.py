from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^reservationActions/(?P<pk>[0-9]+)$', 'actionAPIViews.reservationActions'),
                       #url(r'^actions/(?P<pk>[0-9]+)$', 'views.actionDetail'),
                       )