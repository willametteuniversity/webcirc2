from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                   url(r'^administerLocations/$', 'administerLocationsViews.administerLocations'),
                   url(r'^addNewLocationForm/$', 'administerLocationsViews.addNewLocationForm'),
                   url(r'^chooseLocationToEditForm/$', 'administerLocationsViews.chooseLocationToEditForm'),)