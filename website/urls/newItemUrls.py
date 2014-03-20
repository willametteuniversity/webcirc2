from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^addNewEquipment/', 'views.addNewEquipment'),
                       url(r'^addNewInventoryItemForm/', 'views.addNewInventoryItemForm'),
                       url(r'^addNewNonInventoryItemForm/', 'views.addNewNonInventoryItemForm'),
                       url(r'^addNewConsumableItemForm/', 'views.addNewConsumableItemForm'))