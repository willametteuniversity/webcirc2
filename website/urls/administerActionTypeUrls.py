from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^administerActionTypes/$', 'administerActionTypesViews.administerActionTypes'),
                       url(r'^addNewActionTypeForm/$', 'administerActionTypesViews.addNewActionTypeForm'),
                       url(r'^chooseActionTypeToEditForm/$', 'administerActionTypesViews.chooseActionTypeToEditForm'),)