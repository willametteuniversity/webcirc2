from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^reservationLookup/$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationLookup/(?P<pk>[0-9]+)$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationLookup/(?P<em>.+@.+)$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationLookup/(?P<username>.+)$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationLookup/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationLookup/(?P<username>.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationLookup/(?P<em>.+@.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationOwner/(?P<username>.+)$', 'reservationAPIViews.reservationOwnerLookup'),
                       url(r'^reservationOwner/(?P<em>.+@.+)$', 'reservationAPIViews.reservationOwnerLookup'),
                       url(r'^reservationOwner/(?P<username>.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationOwner/(?P<em>.+@.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'reservationAPIViews.reservationLookup'),
                       url(r'^reservationManage/$', 'reservationAPIViews.reservationManage'),
                       url(r'^reservationManage/(?P<pk>[0-9]+)$', 'reservationAPIViews.reservationManage'),
                       )