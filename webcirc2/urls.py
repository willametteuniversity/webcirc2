from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webcirc2.views.home', name='home'),
    # url(r'^webcirc2/', include('webcirc2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'website.views.login'),
    url(r'^registerNewUser/', 'website.views.registerNewUser'),
    url(r'^$', 'website.views.index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
