from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^administerBuildings/$', 'administerBuildingsViews.administerBuildings'),
                       url(r'^addNewBuildingForm/$', 'administerBuildingsViews.addNewBuildingForm'),
                       url(r'^chooseBuildingToEditForm/$', 'administerBuildingsViews.chooseBuildingToEditForm'),)