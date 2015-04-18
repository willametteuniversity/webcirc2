'''
This file will test the Consumable Item API
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


class ConsumableItemAPITest(TestCase):
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
                                             ActionNotes="This is action 1")

        first_action.Reservation.add(first_reservation)

        second_action = Action.objects.create(ActionID=2,
                                              AssignedOperatorID=generic_user,
                                              ActionTypeID=generic_action_type,
                                              StartTime=datetime.strptime('Jun 1 2014 1:00PM', '%b %d %Y %I:%M%p'),
                                              EndTime=datetime.strptime('Jun 1 2014 3:00PM', '%b %d %Y %I:%M%p'),
                                              Origin=generic_location,
                                              Destination=generic_location,
                                              ActionStatus="",
                                              ActionNotes="This is action 2")

        second_action.Reservation.add(second_reservation)

        generic_category = Label.objects.create(LabelID=1,
                                                LabelName="Label",
                                                ParentCategory=None)

        generic_collection = Collection.objects.create(CollectionID=1,
                                                       CollectionName="Collection 1",
                                                       CollectionDescription="")

        item1 = ConsumableItem.objects.create(ItemID=1,
                                      Description="Item 1",
                                      CategoryID=generic_category,
                                      StorageLocation=generic_location,
                                      CollectionID=generic_collection,
                                      Notes="Created by unit test",
                                      ItemName="Consumable Item 1",
                                      Quantity="5",
                                      MinQuantity="2",
                                      Cost="1.00")

        item2 = ConsumableItem.objects.create(ItemID=2,
                                      Description="Item 2",
                                      CategoryID=generic_category,
                                      StorageLocation=generic_location,
                                      CollectionID=generic_collection,
                                      Notes="Created by unit test",
                                      ItemName="Consumable Item 2",
                                      Quantity="5",
                                      MinQuantity="2",
                                      Cost="1.00")

        first_action.consumableitem_set.add(item1)
        first_action.consumableitem_set.add(item2)
        second_action.consumableitem_set.add(item1)

    def test_api_urls_resolve_correctly(self):
        found = resolve(u'/actionConsumableItems/1')
        self.assertEqual(found.func, actionConsumableItems)
        found = resolve(u'/consumableItems/')
        self.assertEqual(found.func, consumableItemList)
        found = resolve(u'/consumableItems/1')
        self.assertEqual(found.func, consumableItemDetail)

    def test_can_view_all_consumable_items(self):
        client = Client()
        response = client.get(u'/consumableItems/')
        self.assertEqual(1, response.data[0][u'ItemID'])
        self.assertEqual(2, response.data[1][u'ItemID'])

    def test_can_add_new_inventory_item(self):
        client = Client()
        response = client.post(u'/consumableItems/', {u'Description': u'Item 3',
                                                      u'CategoryID': u'1',
                                                      u'StorageLocation': u'1',
                                                      u'CollectionID': u'1',
                                                      u'Notes': u'Created by a unit test',
                                                      u'Action': u'1',
                                                      u'ItemName': u'Consumable Item 3',
                                                      u'Quantity': u'5',
                                                      u'MinQuantity': u'2',
                                                      u'Cost': u'1.00'})
        self.assertEqual(3, response.data[u'ItemID'])
        self.assertEqual(u'Consumable Item 3', response.data[u'ItemName'])
        self.assertEqual(201, response.status_code)

    def test_can_view_one_item(self):
        client = Client()
        response = client.get(u'/consumableItems/1')
        self.assertEqual(1, response.data[u'ItemID'])
        response = client.get(u'/consumableItems/2')
        self.assertEqual(2, response.data[u'ItemID'])

    def test_can_edit_inventory_item(self):
        client = Client()
        response = client.put(u'/consumableItems/2',
                              data=json.dumps({u'Description': u'Item 2, updated',
                                               u'CategoryID': u'1',
                                               u'StorageLocation': u'1',
                                               u'CollectionID': u'1',
                                               u'Notes': u'Created by a unit test',
                                               u'Action': u'1',
                                               u'ItemName': u'Consumable Item 3',
                                               u'Quantity': u'5',
                                               u'MinQuantity': u'2',
                                               u'Cost': u'1.00'}),
                              content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = client.get(u'/consumableItems/2')
        self.assertEqual(u'Item 2, updated', response.data[u'Description'])

    def test_cant_view_nonexistent_action(self):
        client = Client()
        response = client.get(u'/consumableItems/3')
        self.assertEqual(404, response.status_code)

    def test_can_get_consumable_items_from_action(self):
        client = Client()
        response = client.get(u'/actionConsumableItems/1')
        self.assertEqual(response.data[0][u'ItemName'], u'Consumable Item 1')
        self.assertEqual(response.data[1][u'ItemName'], u'Consumable Item 2')
        response = client.get(u'/actionConsumableItems/2')
        self.assertEqual(response.data[0][u'ItemName'], u'Consumable Item 1')
        response = client.get(u'/actionConsumableItems/3')
        self.assertEqual(response.status_code, 404)

    def test_can_delete_action(self):
        client = Client()
        response = client.delete(u'/consumableItems/2')
        self.assertEqual(204, response.status_code)

    def test_can_add_item_to_action(self):
        client = Client()
        response = client.post(u'/addConsumableItemtoAction/2', {u'action': u'2'})
        self.assertEqual(201, response.status_code)
        response = client.get(u'/actionConsumableItems/2')
        self.assertEqual(response.data[0][u'Description'], u'Item 1')
        self.assertEqual(response.data[1][u'Description'], u'Item 2')

    def test_can_remove_item_from_action(self):
        client = Client()
        response = client.post(u'/removeConsumableItemfromAction/1', {u'action': u'1'})
        self.assertEqual(200, response.status_code)
        response = client.get(u'/actionConsumableItems/1')
        self.assertEqual(response.data[0][u'Description'], u'Item 1')