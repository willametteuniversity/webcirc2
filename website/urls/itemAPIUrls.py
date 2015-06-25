from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^actionInventoryItems/(?P<pk>[0-9]+)$', 'itemAPIViews.actionInventoryItems'),
                       url(r'^inventoryItems/$', 'itemAPIViews.inventoryItemList'),
                       url(r'^inventoryItems/(?P<pk>[0-9]+)$', 'itemAPIViews.inventoryItemDetail'),
                       url(r'^inventoryItems/(?P<label>.+)$', 'itemAPIViews.inventoryItemList'),
                       url(r'^addInventoryItemToAction/(?P<pk>[0-9]+)$', 'itemAPIViews.addInventoryItemToAction'),
                       url(r'^removeInventoryItemfromAction/(?P<pk>[0-9]+)$', 'itemAPIViews.removeInventoryItemfromAction'),
                       )