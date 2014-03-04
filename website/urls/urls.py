from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('website.views',
                        url(r'^', include('website.urls.apiUrls')),
                        url(r'^', include('website.urls.inventoryItemUrls')),
                        url(r'^', include('website.urls.labelAndCategoryMgmtUrls')),
                        )

urlpatterns = format_suffix_patterns(urlpatterns)
