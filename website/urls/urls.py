from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('website.views',
                        url(r'^', include('website.urls.apiUrls')),
                        url(r'^', include('website.urls.labelAndCategoryMgmtUrls')),
                        url(r'^', include('website.urls.newItemUrls')),
                        url(r'^', include('website.urls.administerCollectionsUrls')),
                        url(r'^', include('website.urls.administerBuildingsUrls')),
                        url(r'^', include('website.urls.administerActionTypeUrls')),
                        url(r'^', include('website.urls.newReservationUrls')),
                        url(r'^', include('website.urls.administerStatusesUrls')),
                        url(r'^', include('website.urls.administerLocationsUrls')),
                        url(r'^', include('website.urls.reservationAPIUrls')),
                        url(r'^', include('website.urls.actionAPIUrls')),
                        url(r'^', include('website.urls.actionUrls')),
                        url(r'^', include('website.urls.userAPIUrls')),
                        url(r'^', include('website.urls.itemAPIUrls')),
                        )

urlpatterns = format_suffix_patterns(urlpatterns)
