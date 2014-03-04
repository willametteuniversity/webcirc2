from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^labelAndCategoryMgmt/', 'labelAndCategoryMgmt'),
                       url(r'^categoryHierarchy/', 'categoryHierarchy'),)