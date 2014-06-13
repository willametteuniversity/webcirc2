'''
This file will test the Inventory Item API
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


class InventoryItemAPITest(TestCase):
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

        generic_item_brand = ItemBrand.objects.create(BrandID=1,
                                                      BrandName="Unit test brand")

        generic_model = ItemModel.objects.create(ModelID=1,
                                                 ModelDesignation="Unit test model")

        generic_status = Status.objects.create(StatusID=1,
                                               StatusDescription="Unit test")

        InventoryItem.objects.create(ItemID=1,
                                     Description="Item 1",
                                     CategoryID=generic_category,
                                     StorageLocation=generic_location,
                                     CollectionID=generic_collection,
                                     Notes="Created by unit test",
                                     Action=first_action,
                                     AlternateID=None,
                                     BrandID=generic_item_brand,
                                     ModelID=generic_model,
                                     ParentItem=None,
                                     StatusID=generic_status)

        InventoryItem.objects.create(ItemID=2,
                                     Description="Item 2",
                                     CategoryID=generic_category,
                                     StorageLocation=generic_location,
                                     CollectionID=generic_collection,
                                     Notes="Created by unit test",
                                     Action=second_action,
                                     AlternateID=None,
                                     BrandID=generic_item_brand,
                                     ModelID=generic_model,
                                     ParentItem=None,
                                     StatusID=generic_status)

    def test_api_urls_resolve_correctly(self):
        found = resolve(u'/actionInventoryItems/1')
        self.assertEqual(found.func, actionInventoryItems)
        found = resolve(u'/actionNonInventoryItems/1')
        self.assertEqual(found.func, actionNonInventoryItems)
        found = resolve(u'/actionConsumableItems/1')
        self.assertEqual(found.func, actionConsumableItems)
        found = resolve(u'/inventoryItems/')
        self.assertEqual(found.func, inventoryItemList)
        found = resolve(u'/inventoryItems/1')
        self.assertEqual(found.func, inventoryItemDetail)
        found = resolve(u'/nonInventoryItems/')
        self.assertEqual(found.func, nonInventoryItemList)
        found = resolve(u'/nonInventoryItems/1')
        self.assertEqual(found.func, nonInventoryItemDetail)
        found = resolve(u'/consumableItems/')
        self.assertEqual(found.func, consumableItemList)
        found = resolve(u'/consumableItems/1')
        self.assertEqual(found.func, consumableItemDetail)

    def test_can_view_all_actions(self):
        client = Client()
        response = client.get(u'/actions/')
        self.assertEqual(1, response.data[0][u'ActionID'])
        self.assertEqual(2, response.data[1][u'ActionID'])

    def test_can_add_new_action(self):
        client = Client()
        response = client.post(u'/actions/', {u'AssignedOperatorID': u'1',
                                              u'ActionTypeID': u'1',
                                              u'StartTime': u'2014-6-2T13:00',
                                              u'EndTime': u'2014-6-2T15:00',
                                              u'Origin': u'1',
                                              u'Destination': u'1',
                                              u'ActionStatus': u'Unit testing',
                                              u'ActionNotes': u'Created by a unit test',
                                              u'Reservation': u'1'})
        self.assertEqual(3, response.data[u'ActionID'])
        self.assertEqual(u'Created by a unit test', response.data[u'ActionNotes'])
        self.assertEqual(201, response.status_code)

    def test_can_view_one_action(self):
        client = Client()
        response = client.get(u'/actions/1')
        self.assertEqual(1, response.data[u'ActionID'])
        response = client.get(u'/actions/2')
        self.assertEqual(2, response.data[u'ActionID'])

    def test_can_edit_action(self):
        client = Client()
        response = client.put(u'/actions/2',
                              data=json.dumps({u'AssignedOperatorID': u'1',
                                              u'ActionTypeID': u'1',
                                              u'StartTime': u'2014-6-2T13:00',
                                              u'EndTime': u'2014-6-2T15:00',
                                              u'Origin': u'1',
                                              u'Destination': u'1',
                                              u'ActionStatus': u'Unit testing',
                                              u'ActionNotes': u'Edited by a unit test',
                                              u'Reservation': u'2'}),
                              content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = client.get(u'/actions/2')
        self.assertEqual(u'Edited by a unit test', response.data[u'ActionNotes'])

    def test_cant_view_nonexistent_action(self):
        client = Client()
        response = client.get(u'/actions/3')
        self.assertEqual(404, response.status_code)

    def test_can_actions_from_reservations(self):
        client = Client()
        response = client.get(u'/reservationActions/1')
        self.assertEqual(response.data[0][u'ActionNotes'], u'This is action 1')
        response = client.get(u'/reservationActions/2')
        self.assertEqual(response.data[0][u'ActionNotes'], u'This is action 2')
        response = client.get(u'/reservationActions/3')
        self.assertEqual(response.status_code, 404)

    def test_can_delete_action(self):
        client = Client()
        response = client.delete(u'/actions/2')
        self.assertEqual(204, response.status_code)