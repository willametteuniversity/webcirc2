from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^viewTodaysActions/', 'actionViews.viewTodaysActions'))