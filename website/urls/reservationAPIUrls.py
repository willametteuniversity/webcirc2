from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^reservationSearch/(?P<em>.+@.+)$', 'reservationAPIViews.reservationSearch'),
                       url(r'^reservationSearch/(?P<username>.+)$', 'reservationAPIViews.reservationSearch'),
                       url(r'^reservationSearch/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationSearch'),
                       url(r'^reservationSearch/(?P<username>.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationSearch'),
                       url(r'^reservationSearch/(?P<em>.+@.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationSearch'),
                       url(r'^reservationOwnerSearch/(?P<em>.+@.+)$', 'reservationAPIViews.reservationOwnerSearch'),
                       url(r'^reservationOwnerSearch/(?P<username>.+)$', 'reservationAPIViews.reservationOwnerSearch'),
                       url(r'^reservationOwnerSearch/(?P<username>.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationSearch'),
                       url(r'^reservationOwnerSearch/(?P<em>.+@.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationSearch'),
                       url(r'^reservations/$', 'reservationAPIViews.reservationList'),
                       url(r'^reservations/(?P<pk>[0-9]+)$', 'reservationAPIViews.reservationDetail'),
                       )