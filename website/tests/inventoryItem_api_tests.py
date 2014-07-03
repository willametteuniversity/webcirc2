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

        item1 = InventoryItem.objects.create(ItemID=1,
                                             Description="Item 1",
                                             CategoryID=generic_category,
                                             StorageLocation=generic_location,
                                             CollectionID=generic_collection,
                                             Notes="Created by unit test",
                                             #Action=None,
                                             AlternateID=None,
                                             BrandID=generic_item_brand,
                                             ModelID=generic_model,
                                             ParentItem=None,
                                             StatusID=generic_status)

        item2 = InventoryItem.objects.create(ItemID=2,
                                             Description="Item 2",
                                             CategoryID=generic_category,
                                             StorageLocation=generic_location,
                                             CollectionID=generic_collection,
                                             Notes="Created by unit test",
                                           #  Action=None,
                                             AlternateID=None,
                                             BrandID=generic_item_brand,
                                             ModelID=generic_model,
                                             ParentItem=None,
                                             StatusID=generic_status)

        first_action.inventoryitem_set.add(item1)
        first_action.inventoryitem_set.add(item2)
        second_action.inventoryitem_set.add(item1)

    def test_api_urls_resolve_correctly(self):
        found = resolve(u'/actionInventoryItems/1')
        self.assertEqual(found.func, actionInventoryItems)
        found = resolve(u'/inventoryItems/')
        self.assertEqual(found.func, inventoryItemList)
        found = resolve(u'/inventoryItems/1')
        self.assertEqual(found.func, inventoryItemDetail)

    def test_can_view_all_inventory_items(self):
        client = Client()
        response = client.get(u'/inventoryItems/')
        self.assertEqual(1, response.data[0][u'ItemID'])
        self.assertEqual(2, response.data[1][u'ItemID'])

    def test_can_add_new_inventory_item(self):
        client = Client()
        response = client.post(u'/inventoryItems/', {u'Description': u'Item 3',
                                                     u'CategoryID': u'1',
                                                     u'StorageLocation': u'1',
                                                     u'CollectionID': u'1',
                                                     u'Notes': u'Created by a unit test',
                                                     u'Action': u'1',
                                                     u'BrandID': u'1',
                                                     u'ModelID': u'1',
                                                     u'StatusID': u'1'})
        self.assertEqual(3, response.data[u'ItemID'])
        self.assertEqual(u'Created by a unit test', response.data[u'Notes'])
        self.assertEqual(201, response.status_code)

    def test_can_view_one_item(self):
        client = Client()
        response = client.get(u'/inventoryItems/1')
        self.assertEqual(1, response.data[u'ItemID'])
        response = client.get(u'/inventoryItems/2')
        self.assertEqual(2, response.data[u'ItemID'])

    def test_can_edit_inventory_item(self):
        client = Client()
        response = client.put(u'/inventoryItems/2',
                              data=json.dumps({u'Description': u'Updated item 2',
                                               u'CategoryID': u'1',
                                               u'StorageLocation': u'1',
                                               u'CollectionID': u'1',
                                               u'Notes': u'Created by a unit test',
                                               u'Action': u'2',
                                               u'BrandID': u'1',
                                               u'ModelID': u'1',
                                               u'StatusID': u'1'}),
                              content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = client.get(u'/inventoryItems/2')
        self.assertEqual(u'Updated item 2', response.data[u'Description'])

    def test_cant_view_nonexistent_action(self):
        client = Client()
        response = client.get(u'/inventoryItems/3')
        self.assertEqual(404, response.status_code)

    def test_can_get_inventory_items_from_action(self):
        client = Client()
        response = client.get(u'/actionInventoryItems/1')
        self.assertEqual(response.data[0][u'Description'], u'Item 1')
        self.assertEqual(response.data[1][u'Description'], u'Item 2')
        response = client.get(u'/actionInventoryItems/2')
        self.assertEqual(response.data[0][u'Description'], u'Item 1')
        response = client.get(u'/actionInventoryItems/3')
        self.assertEqual(response.status_code, 404)

    def test_can_delete_action(self):
        client = Client()
        response = client.delete(u'/inventoryItems/2')
        self.assertEqual(204, response.status_code)

    def test_can_add_item_to_action(self):
        pass
        # add item 2 to action 2
        # check action 2 has both items

    def test_can_remove_item_from_action(self):
        pass
        # remove item 1 from action 2
        # check that action 2 only has item 2