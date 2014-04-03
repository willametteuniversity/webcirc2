from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^buildings/$', 'views.buildingList'),
                       url(r'^buildings/(?P<pk>[0-9]+)$', 'views.buildingDetail'),
                       url(r'^buildings/(?P<bc>.+)$', 'views.buildingDetail'),
                       url(r'^collections/$', 'views.collectionList'),
                       url(r'^collections/(?P<pk>[0-9]+)$', 'views.collectionDetail'),
                       url(r'^collections/(?P<cn>.+)$', 'views.collectionDetail'),
                       url(r'^labels/$', 'views.labelList'),
                       url(r'^labels/(?P<pk>[0-9]+)$', 'views.labelDetail'),
                       url(r'^labels/(?P<ln>.+)$', 'views.labelDetail'),
                       url(r'^labelsNotCategories/$', 'views.labelsNotCategories'),
                       url(r'^inventoryitems/$', 'views.inventoryItemList'),
                       url(r'^inventoryitems/(?P<pk>[0-9]+)$', 'views.inventoryItemDetail'),
                       url(r'^noninventoryitems/$', 'views.nonInventoryItemList'),
                       url(r'^noninventoryitems/(?P<pk>[0-9]+)$', 'views.nonInventoryItemDetail'),
                       url(r'^consumableitems/$', 'views.consumableItemList'),
                       url(r'^consumableitems/(?P<pk>[0-9]+)$', 'views.consumableItemDetail'),
                       url(r'^locations/$', 'views.locationList'),
                       url(r'^locations/(?P<pk>[0-9]+)$', 'views.locationDetail'),
                       url(r'^models/$', 'views.itemModelList'),
                       url(r'^models/(?P<pk>[0-9]+)$', 'views.itemModelDetail'),
                       url(r'^models/(?P<mn>.+)$', 'views.itemModelDetail'),
                       url(r'^reservations/$', 'views.reservationList'),
                       url(r'^users/$', 'views.userList'),
                       url(r'^users/(?P<pk>[0-9]+)$', 'views.userDetail'),
                       url(r'^users/(?P<em>.+@.+)$', 'views.userDetail'),
                       url(r'^users/(?P<fn>.+ .+)$', 'views.userDetail'),
                       url(r'^users/(?P<n>.+)$', 'views.userDetail'),
                       url(r'^labelNotes/$', 'views.labelNoteList'),
                       url(r'^labelNotes/(?P<pk>[0-9]+)$', 'views.labelNoteDetail'),
                       url(r'^images/$', 'views.imageList'),
                       url(r'^images/(?P<pk>[0-9]+)$', 'views.imageDetail'),
                       url(r'^statuses/$', 'views.statusList'),
                       url(r'^statuses/(?P<pk>[0-9]+)$', 'views.statusDetail'),
                       url(r'^brands/$', 'views.itemBrandList'),
                       url(r'^brands/(?P<pk>[0-9]+)$', 'views.itemBrandDetail'),
                       url(r'^brands/(?P<bn>.+)$', 'views.itemBrandDetail'),
                       url(r'^actions/$', 'views.actionTypeList'),
                       url(r'^actions/(?P<pk>[0-9]+)$', 'views.actionTypeDetail'),
                       url(r'^itemHistory/(?P<fk>[0-9]+)$', 'views.itemHistoryDetail'),
                       url(r'^categoryHierarchy/', 'views.categoryHierarchy'),
                       url(r'^autocomplete/', 'views.autocomplete'),
                       url(r'^itemHistory/(?P<fk>[0-9]+)$', 'views.itemHistoryDetail'),
                       url(r'^reservationHistory/(?P<fk>[0-9]+)$', 'views.reservationHistoryDetail'),)