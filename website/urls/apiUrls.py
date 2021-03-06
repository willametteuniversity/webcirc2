from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^buildings/$', 'buildingAPIViews.buildingList'),
                       url(r'^buildings/(?P<pk>[0-9]+)$', 'buildingAPIViews.buildingDetail'),
                       url(r'^buildings/(?P<bc>.+)$', 'buildingAPIViews.buildingDetail'),
                       url(r'^collections/$', 'collectionAPIViews.collectionList'),
                       url(r'^collections/(?P<pk>[0-9]+)$', 'collectionAPIViews.collectionDetail'),
                       url(r'^collections/(?P<cn>.+)$', 'collectionAPIViews.collectionDetail'),
                       url(r'^labels/$', 'labelAPIViews.labelList'),
                       url(r'^labels/(?P<pk>[0-9]+)$', 'labelAPIViews.labelDetail'),
                       url(r'^labels/(?P<ln>.+)$', 'labelAPIViews.labelDetail'),
                       url(r'^labelsNotCategories/$', 'views.labelsNotCategories'),
                       url(r'^locations/$', 'locationAPIViews.locationList'),
                       url(r'^locations/(?P<pk>[0-9]+)$', 'locationAPIViews.locationDetail'),
                       url(r'^models/$', 'itemModelAPIViews.itemModelList'),
                       url(r'^models/(?P<pk>[0-9]+)$', 'itemModelAPIViews.itemModelDetail'),
                       url(r'^models/(?P<mn>.+)$', 'itemModelAPIViews.itemModelDetail'),
                       url(r'^customerProfiles/$', 'customerProfileViews.customerProfileList'),
                       url(r'^customerProfiles/(?P<uid>[0-9]+)$', 'customerProfileViews.customerProfileDetail'),
                       url(r'^labelNotes/$', 'labelNoteAPIViews.labelNoteList'),
                       url(r'^labelNotes/(?P<pk>[0-9]+)$', 'labelNoteAPIViews.labelNoteDetail'),
                       url(r'^images/$', 'imageAPIViews.imageList'),
                       url(r'^images/(?P<pk>[0-9]+)$', 'imageAPIViews.imageDetail'),
                       url(r'^statuses/$', 'statusViews.statusList'),
                       url(r'^statuses/(?P<pk>[0-9]+)$', 'statusViews.statusDetail'),
                       url(r'^actionstates/$', 'actionStateViews.actionStateList'),
                       url(r'^actionstates/(?P<pk>[0-9]+)$', 'actionStateViews.actionStateDetail'),
                       url(r'^brands/$', 'itemBrandAPIViews.itemBrandList'),
                       url(r'^brands/(?P<pk>[0-9]+)$', 'itemBrandAPIViews.itemBrandDetail'),
                       url(r'^brands/(?P<bn>.+)$', 'itemBrandAPIViews.itemBrandDetail'),
                       url(r'^actionTypes/$', 'actionTypeAPIViews.actionTypeList'),
                       url(r'^actionTypes/(?P<pk>[0-9]+)$', 'actionTypeAPIViews.actionTypeDetail'),
                       url(r'^itemHistory/(?P<fk>[0-9]+)$', 'views.itemHistoryDetail'),
                       url(r'^categoryHierarchy/', 'views.categoryHierarchy'),
                       url(r'^autocomplete/', 'views.autocomplete'),
                       url(r'^itemHistory/(?P<fk>[0-9]+)$', 'views.itemHistoryDetail'),
                       url(r'^reservationHistory/(?P<fk>[0-9]+)$', 'views.reservationHistoryDetail'),)