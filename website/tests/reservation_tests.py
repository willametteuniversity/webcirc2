from os.path import abspath, dirname
import sys
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest
# Import all of our views for testing
from website.views import *
# Same for models
from website.models import *
from django.contrib.auth.models import User
 
class ReservationAPITests(TestCase):

    def setUp(self):

        user1 = User.objects.create()

        res1 = Reservation.objects.create(EventTitle='Reservation1', CustomerEmail='billybob@test.com', CustomerID=user1, CustomerPhone=5555555551, CustomerDept='Test1', ReservationNotes='This is a test')
        res2 = Reservation.objects.create(EventTitle='Reservation2', CustomerEmail='jimmyjohn@test.com', CustomerID=user1, CustomerPhone=5555555552, CustomerDept='Test2', ReservationNotes='This is a test')

    def test_can_get_list_of_reservations(self):
        c = Client()
        response = c.get(u'/reservations/')

        self.assertEqual(u'Reservation1', response.data[0]['EventTitle'])
    	self.assertEqual(u'Reservation2', response.data[1]['EventTitle'])

        found = resolve(u'/reservations/')
        self.assertEqual(found.func, reservationList)

    def test_reservations_url_resolves_to_reservationDetail(self):
        found = resolve(u'/reservations/1')
        self.assertEqual(found.func, reservationDetail)

    def test_can_get_specific_reservation(self):
        c = Client()
        response = c.get(u'/reservations/1')

        self.assertEqual(u'Reservation1', response.data['EventTitle'])
        self.assertEqual(u'billybob@test.com', response.data['CustomerEmail'])
        self.assertEqual(1, response.data['ReservationID'])

    def test_cannot_get_nonexistant_reservation(self):
        c = Client()
        response = c.get(u'/reservations/3')

        self.assertEqual(404, response.status_code)

    def test_can_create_new_reservation(self):
        c = Client()
        # Make the request to make the reservation...

        user1 = Reservation.objects.get(pk=1).CustomerID

        response = c.post(u'/reservations/', {u'EventTitle' : u'Reservation3', u'CustomerEmail' : u'sallysal@test.com',
                                                u'CustomerID' : user1.pk, u'CustomerPhone' : 5555555553, u'CustomerDept' : u'Test3',
                                                u'ReservationNotes' : u'This is a test', u'CustomerStatus' : u'A Status'})
        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(u'Reservation3', response.data[u'EventTitle'])
        self.assertEqual(u'sallysal@test.com', response.data[u'CustomerEmail'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_reservation(self):
        '''
        This tests that we can delete a reservation
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/reservations/2')
        # Let's check the status code
        self.assertEqual(204, response.status_code)