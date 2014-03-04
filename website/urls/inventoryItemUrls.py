from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^addNewEquipment/', 'addNewEquipment'),
                       url(r'^addNewInventoryItemForm/', 'addNewInventoryItemForm'),
                       url(r'^addNewNonInventoryItemForm/', 'addNewNonInventoryItemForm'),)

