'''
This file will test the Reservation API
'''

from os.path import abspath, dirname
import sys

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from website.views.reservationAPIViews import *
from website.models import *
from datetime import datetime
import json


class ReservationAPITest(TestCase):
    def setUp(self):
        generic_user = User.objects.create(pk=1, username='Test User 1')
        generic_action_type = ActionType.objects.create(pk=1, ActionTypeName="Action 1")
        generic_location = Location.objects.create(pk=1,
                                                   BuildingID=Building.objects.create(pk=1),
                                                   RoomNumber="404",
                                                   LocationDescription="Generic location")

        first_reservation = Reservation.objects.create(pk=1,
                                                       CustomerID=generic_user,
                                                       OwnerID=generic_user,
                                                       CustomerPhone="Test",
                                                       CustomerEmail="Test",
                                                       CustomerDept="Test",
                                                       CustomerStatus="Test",
                                                       ReservationNotes="Reservation 1",
                                                       EventTitle="Test")

        second_reservation = Reservation.objects.create(pk=2,
                                                        CustomerID=generic_user,
                                                        OwnerID=generic_user,
                                                        CustomerPhone="Test",
                                                        CustomerEmail="Test",
                                                        CustomerDept="Test",
                                                        CustomerStatus="Test",
                                                        ReservationNotes="Reservation 2",
                                                        EventTitle="Test")

        action1 = Action.objects.create(ActionID=1,
                                        AssignedOperatorID=generic_user,
                                        ActionTypeID=generic_action_type,
                                        StartTime=datetime.strptime('Jun 1 2014 1:00PM', '%b %d %Y %I:%M%p'),
                                        EndTime=datetime.strptime('Jun 1 2014 3:00PM', '%b %d %Y %I:%M%p'),
                                        Origin=generic_location,
                                        Destination=generic_location,
                                        ActionStatus="",
                                        ActionNotes="This is action 1")

        action2 = Action.objects.create(ActionID=2,
                                        AssignedOperatorID=generic_user,
                                        ActionTypeID=generic_action_type,
                                        StartTime=datetime.strptime('Jun 3 2014 1:00PM', '%b %d %Y %I:%M%p'),
                                        EndTime=datetime.strptime('Jun 3 2014 3:00PM', '%b %d %Y %I:%M%p'),
                                        Origin=generic_location,
                                        Destination=generic_location,
                                        ActionStatus="",
                                        ActionNotes="This is action 2")

        action3 = Action.objects.create(ActionID=3,
                                        AssignedOperatorID=generic_user,
                                        ActionTypeID=generic_action_type,
                                        StartTime=datetime.strptime('Jun 7 2014 1:00PM', '%b %d %Y %I:%M%p'),
                                        EndTime=datetime.strptime('Jun 7 2014 3:00PM', '%b %d %Y %I:%M%p'),
                                        Origin=generic_location,
                                        Destination=generic_location,
                                        ActionStatus="",
                                        ActionNotes="This is action 3")

    def test_urls_resolve_correctly(self):
        found = resolve(u'/reservations/')
        self.assertEqual(found.func, reservationList)
        found = resolve(u'/reservations/1')
        self.assertEqual(found.func, reservationDetail)
        found = resolve(u'/reservationSearch/test')
        self.assertEqual(found.func, reservationSearch)
        found = resolve(u'/reservationOwnerSearch/test')
        self.assertEqual(found.func, reservationOwnerSearch)

    def test_can_get_all_reservations(self):
        client = Client()
        response = client.get(u'/reservations/')
        self.assertEqual(1, response.data[0][u'ReservationID'])
        self.assertEqual(2, response.data[1][u'ReservationID'])

    def test_can_get_one_reservation(self):
        client = Client()
        response = client.get(u'/reservations/1')
        self.assertEqual(1, response.data[u'ReservationID'])
        response = client.get(u'/reservations/2')
        self.assertEqual(2, response.data[u'ReservationID'])

    def test_can_create_reservation(self):
        client = Client()
        response = client.post(u'/reservations/', {u'CustomerID': u'1',
                                                   u'OwnerID': u'1',
                                                   u'CustomerPhone': u'Test',
                                                   u'CustomerEmail': u'Test',
                                                   u'CustomerDept': u'Test',
                                                   u'CustomerStatus': u'Test',
                                                   u'ReservationNotes': u'Test',
                                                   u'EventTitle': u'Test'})
        self.assertEqual(3, response.data[u'ReservationID'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_reservation(self):
        client = Client()
        response = client.delete(u'/reservations/1')
        self.assertEqual(204, response.status_code)

    def test_can_edit_reservation(self):
        client = Client()
        response = client.put(u'/reservations/2',
                              data=json.dumps({u'CustomerID': u'1',
                                               u'OwnerID': u'1',
                                               u'CustomerPhone': u'Test',
                                               u'CustomerEmail': u'Test',
                                               u'CustomerDept': u'Test',
                                               u'CustomerStatus': u'Test',
                                               u'ReservationNotes': u'Test, edited',
                                               u'EventTitle': u'Test'}),
                              content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = client.get(u'/reservations/2')
        self.assertEqual(u'Test, edited', response.data[u'ReservationNotes'])\

    # Todo: Create lookup views
    # Lookup views:

    def test_can_lookup_by_username(self):
        pass

    def test_can_lookup_by_email(self):
        pass

    def test_can_filter_lookup_by_date(self):
        pass

    def test_can_lookup_by_owner_email(self):
        pass

    def test_can_lookup_by_owner_username(self):
        pass

    def test_can_filter_owner_lookup_by_date(self):
        pass