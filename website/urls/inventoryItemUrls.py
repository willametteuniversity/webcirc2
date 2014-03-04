from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('website.views',
                       url(r'^addNewEquipment/', 'addNewEquipment'),
                       url(r'^addNewInventoryItemForm/', 'addNewInventoryItemForm'),
                       url(r'^addNewNonInventoryItemForm/', 'addNewNonInventoryItemForm'),)

