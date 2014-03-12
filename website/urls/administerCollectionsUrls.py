from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^administerCollections/$', 'administerCollectionsViews.administerCollections'),
                       url(r'^addNewCollectionForm/$', 'administerCollectionsViews.addNewCollectionForm'),
                       url(r'^editCollectionForm/$', 'administerCollectionsViews.editCollectionForm'),)