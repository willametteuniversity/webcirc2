from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^labelAndCategoryMgmt/', 'views.labelAndCategoryMgmt'),
                       url(r'^categoryHierarchy/', 'views.categoryHierarchy'),
                       url(r'^categoryHierarchyWithEquipment/(?P<root>.+)$', 'views.categoryHierarchyWithEquipment'),
                       url(r'^categoryHierarchyWithEquipment/$', 'views.categoryHierarchyWithEquipment'),)
