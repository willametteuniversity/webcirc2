from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('website.views',
                       url(r'^labelAndCategoryMgmt/', 'labelAndCategoryMgmt'),
                       url(r'^collections/$', 'collectionList'),
                       url(r'^collections/(?P<pk>[0-9]+)$', 'collectionDetail'),
                       url(r'^labels/$', 'labelList'),
                       url(r'^labels/(?P<pk>[0-9]+)$', 'labelDetail'),
                       url(r'^models/$', 'itemModelList'),
                       url(r'^models/(?P<pk>[0-9]+)$', 'itemModelDetail'),
                       url(r'^reservations/$', 'reservationList'),
                       url(r'^reservations/(?P<pk>[0-9]+)$', 'reservationDetail'),
                       url(r'^labelNotes/$', 'labelNoteList'),
                       url(r'^labelNotes/(?P<pk>[0-9]+)$', 'labelNoteDetail'),
                       url(r'^images/$', 'imageList'),
                       url(r'^images/(?P<pk>[0-9]+)$', 'imageDetail'),
                       url(r'^statuses/$', 'statusList'),
                       url(r'^statuses/(?P<pk>[0-9]+)$', 'statusDetail'),
                       url(r'^inventoryItems/$', 'inventoryItemList'),
                       url(r'^inventoryItems/(?P<pk>[0-9]+)$', 'inventoryItemDetail'),
                       url(r'^brands/$', 'itemBrandList'),
                       url(r'^brands/(?P<pk>[0-9]+)$', 'itemBrandDetail'),
                       url(r'^actions/$', 'actionTypeList'),
                       url(r'^actions/(?P<pk>[0-9]+)$', 'actionTypeDetail'),
                       url(r'^categoryHierarchy/', 'categoryHierarchy'),
                       url(r'^addNewInventoryItemForm/', 'addNewInventoryItemForm'),
                       url(r'^', include('website.urls.administerStatusesUrls'))

urlpatterns = format_suffix_patterns(urlpatterns)
