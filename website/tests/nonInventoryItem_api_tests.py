'''
This file will test the Non-Inventory Item API
'''

from os.path import abspath, dirname
import sys

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from website.views.itemAPIViews import *
from website.models import *
from datetime import datetime
import json


class NonInventoryItemAPITest(TestCase):
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

        first_action = Action.objects.create(ActionID=1,
                                             AssignedOperatorID=generic_user,
                                             ActionTypeID=generic_action_type,
                                             StartTime=datetime.strptime('Jun 1 2014 1:00PM', '%b %d %Y %I:%M%p'),
                                             EndTime=datetime.strptime('Jun 1 2014 3:00PM', '%b %d %Y %I:%M%p'),
                                             Origin=generic_location,
                                             Destination=generic_location,
                                             ActionStatus="",
                                             ActionNotes="This is action 1",
                                             Reservation=first_reservation)

        second_action = Action.objects.create(ActionID=2,
                                              AssignedOperatorID=generic_user,
                                              ActionTypeID=generic_action_type,
                                              StartTime=datetime.strptime('Jun 1 2014 1:00PM', '%b %d %Y %I:%M%p'),
                                              EndTime=datetime.strptime('Jun 1 2014 3:00PM', '%b %d %Y %I:%M%p'),
                                              Origin=generic_location,
                                              Destination=generic_location,
                                              ActionStatus="",
                                              ActionNotes="This is action 2",
                                              Reservation=second_reservation)

        generic_category = Label.objects.create(LabelID=1,
                                                LabelName="Label",
                                                ParentCategory=None)

        generic_collection = Collection.objects.create(CollectionID=1,
                                                       CollectionName="Collection 1",
                                                       CollectionDescription="")

        NonInventoryItem.objects.create(ItemID=1,
                                        Description="Item 1",
                                        CategoryID=generic_category,
                                        StorageLocation=generic_location,
                                        CollectionID=generic_collection,
                                        Notes="Created by unit test",
                                        Action=first_action,
                                        Quantity="5")

        NonInventoryItem.objects.create(ItemID=2,
                                      Description="Item 2",
                                      CategoryID=generic_category,
                                      StorageLocation=generic_location,
                                      CollectionID=generic_collection,
                                      Notes="Created by unit test",
                                      Action=second_action,
                                      Quantity="5")

    def test_api_urls_resolve_correctly(self):
        found = resolve(u'/actionNonInventoryItems/1')
        self.assertEqual(found.func, actionNonInventoryItems)
        found = resolve(u'/nonInventoryItems/')
        self.assertEqual(found.func, nonInventoryItemList)
        found = resolve(u'/nonInventoryItems/1')
        self.assertEqual(found.func, nonInventoryItemDetail)

    def test_can_view_all_consumable_items(self):
        client = Client()
        response = client.get(u'/nonInventoryItems/')
        self.assertEqual(1, response.data[0][u'ItemID'])
        self.assertEqual(2, response.data[1][u'ItemID'])

    def test_can_add_new_inventory_item(self):
        client = Client()
        response = client.post(u'/nonInventoryItems/', {u'Description': u'Item 3',
                                                        u'CategoryID': u'1',
                                                        u'StorageLocation': u'1',
                                                        u'CollectionID': u'1',
                                                        u'Notes': u'Created by a unit test',
                                                        u'Action': u'1',
                                                        u'Quantity': u'5'})
        self.assertEqual(3, response.data[u'ItemID'])
        self.assertEqual(u'Created by a unit test', response.data[u'Notes'])
        self.assertEqual(201, response.status_code)

    def test_can_view_one_item(self):
        client = Client()
        response = client.get(u'/nonInventoryItems/1')
        self.assertEqual(1, response.data[u'ItemID'])
        response = client.get(u'/nonInventoryItems/2')
        self.assertEqual(2, response.data[u'ItemID'])

    def test_can_edit_inventory_item(self):
        client = Client()
        response = client.put(u'/nonInventoryItems/2',
                              data=json.dumps({u'Description': u'Item 2, updated',
                                               u'CategoryID': u'1',
                                               u'StorageLocation': u'1',
                                               u'CollectionID': u'1',
                                               u'Notes': u'Created by a unit test',
                                               u'Action': u'1',
                                               u'Quantity': u'5'}),
                              content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = client.get(u'/nonInventoryItems/2')
        self.assertEqual(u'Item 2, updated', response.data[u'Description'])

    def test_cant_view_nonexistent_action(self):
        client = Client()
        response = client.get(u'/nonInventoryItems/3')
        self.assertEqual(404, response.status_code)

    def test_can_get_consumable_items_from_action(self):
        client = Client()
        response = client.get(u'/actionNonInventoryItems/1')
        self.assertEqual(response.data[0][u'Description'], u'Item 1')
        response = client.get(u'/actionNonInventoryItems/2')
        self.assertEqual(response.data[0][u'Description'], u'Item 2')
        response = client.get(u'/actionNonInventoryItems/3')
        self.assertEqual(response.status_code, 404)

    def test_can_delete_action(self):
        client = Client()
        response = client.delete(u'/nonInventoryItems/2')
        self.assertEqual(204, response.status_code)