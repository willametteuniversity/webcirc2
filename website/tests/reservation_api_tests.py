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
from website.views.actionAPIViews import *
from website.models import *
from datetime import datetime
import json


class ActionAPITest(TestCase):
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
                                                       CustomerPhone="",
                                                       CustomerEmail="",
                                                       CustomerDept="",
                                                       CustomerStatus="",
                                                       ReservationNotes="",
                                                       EventTitle="")

        second_reservation = Reservation.objects.create(pk=2,
                                                        CustomerID=generic_user,
                                                        OwnerID=generic_user,
                                                        CustomerPhone="",
                                                        CustomerEmail="",
                                                        CustomerDept="",
                                                        CustomerStatus="",
                                                        ReservationNotes="",
                                                        EventTitle="")

        Action.objects.create(ActionID=1,
                              AssignedOperatorID=generic_user,
                              ActionTypeID=generic_action_type,
                              StartTime=datetime.strptime('Jun 1 2014 1:00PM', '%b %d %Y %I:%M%p'),
                              EndTime=datetime.strptime('Jun 1 2014 3:00PM', '%b %d %Y %I:%M%p'),
                              Origin=generic_location,
                              Destination=generic_location,
                              ActionStatus="",
                              ActionNotes="This is action 1",
                              Reservation=first_reservation)

        Action.objects.create(ActionID=2,
                              AssignedOperatorID=generic_user,
                              ActionTypeID=generic_action_type,
                              StartTime=datetime.strptime('Jun 3 2014 1:00PM', '%b %d %Y %I:%M%p'),
                              EndTime=datetime.strptime('Jun 3 2014 3:00PM', '%b %d %Y %I:%M%p'),
                              Origin=generic_location,
                              Destination=generic_location,
                              ActionStatus="",
                              ActionNotes="This is action 2",
                              Reservation=second_reservation)

        Action.objects.create(ActionID=3,
                              AssignedOperatorID=generic_user,
                              ActionTypeID=generic_action_type,
                              StartTime=datetime.strptime('Jun 7 2014 1:00PM', '%b %d %Y %I:%M%p'),
                              EndTime=datetime.strptime('Jun 7 2014 3:00PM', '%b %d %Y %I:%M%p'),
                              Origin=generic_location,
                              Destination=generic_location,
                              ActionStatus="",
                              ActionNotes="This is action 3",
                              Reservation=second_reservation)

    def test_can_get_all_reservations(self):
        pass

    def test_can_get_one_reservation(self):
        pass

    def test_can_create_reservation(self):
        pass

    def test_can_delete_reservation(self):
        pass

    def test_can_edit_reservation(self):
        pass

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