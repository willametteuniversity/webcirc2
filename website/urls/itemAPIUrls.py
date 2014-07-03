from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^actionInventoryItems/(?P<pk>[0-9]+)$', 'itemAPIViews.actionInventoryItems'),
                       url(r'^actionNonInventoryItems/(?P<pk>[0-9]+)$', 'itemAPIViews.actionNonInventoryItems'),
                       url(r'^actionConsumableItems/(?P<pk>[0-9]+)$', 'itemAPIViews.actionConsumableItems'),
                       url(r'^inventoryItems/$', 'itemAPIViews.inventoryItemList'),
                       url(r'^inventoryItems/(?P<pk>[0-9]+)$', 'itemAPIViews.inventoryItemDetail'),
                       url(r'^nonInventoryItems/$', 'itemAPIViews.nonInventoryItemList'),
                       url(r'^nonInventoryItems/(?P<pk>[0-9]+)$', 'itemAPIViews.nonInventoryItemDetail'),
                       url(r'^consumableItems/$', 'itemAPIViews.consumableItemList'),
                       url(r'^consumableItems/(?P<pk>[0-9]+)$', 'itemAPIViews.consumableItemDetail'),
                       url(r'^addInventoryItemtoAction/(?P<pk>[0-9]+)$', 'itemAPIViews.addInventoryItemtoAction'),
                       url(r'^removeInventoryItemfromAction/(?P<pk>[0-9]+)$', 'itemAPIViews.removeInventoryItemfromAction'),
                       url(r'^addConsumableItemtoAction/(?P<pk>[0-9]+)$', 'itemAPIViews.addConsumableItemtoAction'),
                       url(r'^removeConsumableItemfromAction/(?P<pk>[0-9]+)$', 'itemAPIViews.removeConsumableItemfromAction'),
                       url(r'^addNonInventoryItemtoAction/(?P<pk>[0-9]+)$', 'itemAPIViews.addNonInventoryItemtoAction'),
                       url(r'^removeNonInventoryItemfromAction/(?P<pk>[0-9]+)$', 'itemAPIViews.removeNonInventoryItemfromAction'),
                       )