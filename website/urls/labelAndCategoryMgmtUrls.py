from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('website.views',
                       url(r'^labelAndCategoryMgmt/', 'labelAndCategoryMgmt'),
                       url(r'^categoryHierarchy/', 'categoryHierarchy'),)