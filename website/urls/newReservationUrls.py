from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
                       url(r'^addNewReservation/', 'reservationViews.addNewReservation'),
                       url(r'^addNewReservationForm/', 'reservationViews.addNewReservationForm',),
                       url(r'^findAvailableEquipment/', 'reservationViews.findAvailableEquipment'))