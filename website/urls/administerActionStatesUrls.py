from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^administerActionStates/$', 'actionStateViews.administerActionStates'),
                       url(r'^addNewActionStateForm/$', 'actionStateViews.addNewActionStateForm'),
                       url(r'^chooseActionStateToEditForm/$', 'actionStateViews.chooseActionStateToEditForm'),)