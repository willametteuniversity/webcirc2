from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^administerStatuses/$', 'statusViews.administerStatuses'),
                       url(r'^addNewStatusForm/$', 'statusViews.addNewStatusForm'),
                       url(r'^chooseStatusToEditForm/$', 'statusViews.chooseStatusToEditForm'),)