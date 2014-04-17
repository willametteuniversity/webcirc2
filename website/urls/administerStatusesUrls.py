from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^administerStatuses/$', 'administerStatuses'),
                       url(r'^addNewStatusForm/$', 'addNewStatusForm'),
                       url(r'^chooseStatusToEditForm/$', 'chooseStatusToEditForm'),)