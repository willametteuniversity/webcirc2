from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^administerStatuses/$', 'administerStatusesViews.administerStatuses'),
                       url(r'^addNewStatusForm/$', 'administerStatusesViews.addNewStatusForm'),
                       url(r'^chooseStatusToEditForm/$', 'administerStatusesViews.chooseStatusToEditForm'),)