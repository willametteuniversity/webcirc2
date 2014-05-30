from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^reservationLookup/$', 'views.reservationLookup'),
                       url(r'^reservationLookup/(?P<pk>[0-9]+)$', 'views.reservationLookup'),
                       url(r'^reservationLookup/(?P<em>.+@.+)$', 'views.reservationLookup'),
                       url(r'^reservationLookup/(?P<username>.+)$', 'views.reservationLookup'),
                       url(r'^reservationLookup/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'views.reservationLookup'),
                       url(r'^reservationLookup/(?P<username>.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'views.reservationLookup'),
                       url(r'^reservationLookup/(?P<em>.+@.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'views.reservationLookup'),
                       url(r'^reservationOwner/(?P<username>.+)$', 'views.reservationOwnerLookup'),
                       url(r'^reservationOwner/(?P<em>.+@.+)$', 'views.reservationOwnerLookup'),
                       url(r'^reservationOwner/(?P<username>.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'views.reservationLookup'),
                       url(r'^reservationOwner/(?P<em>.+@.+)/(?P<start_date>[0-9]+-+[0-9]+-+[0-9])/(?P<end_date>[0-9]+-+[0-9]+-+[0-9])$', 'views.reservationLookup'),
                       url(r'^reservationManage/$', 'views.reservationManage'),
                       url(r'^reservationManage/(?P<pk>[0-9]+)$', 'views.reservationManage'),
                       )