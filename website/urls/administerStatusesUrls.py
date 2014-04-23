from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^administerStatuses/$', 'views.administerStatuses'),
                       url(r'^addNewStatusForm/$', 'views.addNewStatusForm'),
                       url(r'^chooseStatusToEditForm/$', 'views.chooseStatusToEditForm'),)