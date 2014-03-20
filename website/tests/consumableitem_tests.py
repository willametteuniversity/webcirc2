from os.path import abspath, dirname
import sys
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest
# Import all of our views for testing
from website.views.views import *
# Same for models
from website.models import *
from django.contrib.auth.models import User
 
class ConsumableItemAPITests(TestCase):

    def setUp(self):

        label1 = Label.objects.create();
        label2 = Label.objects.create();

        status1 = Status.objects.create();
        status2 = Status.objects.create();

        building = Building.objects.create(BuildingCode=1);

        location1 = Location.objects.create(BuildingID=building);
        location2 = Location.objects.create(BuildingID=building);

        collection1 = Collection.objects.create();
        collection2 = Collection.objects.create();

        inv1 = ConsumableItem.objects.create(Description=u'ConsumableItem1', Quantity=5, MinQuantity=10, Cost=10.00, Notes=u'Note1', CategoryID=label1, StorageLocation=location1)
        inv2 = ConsumableItem.objects.create(Description=u'ConsumableItem2', Quantity=10, MinQuantity=10, Cost=5.00, Notes=u'Note2', CategoryID=label2, StorageLocation=location2)

    def test_can_get_list_of_consumableItems(self):
        c = Client()
        response = c.get(u'/consumableitems/')

        self.assertEqual(u'ConsumableItem1', response.data[0]['Description'])
        self.assertEqual(u'ConsumableItem2', response.data[1]['Description'])

        found = resolve(u'/consumableitems/')
        self.assertEqual(found.func, consumableItemList)

    def test_consumable_url_resolves_to_consumableItemDetail(self):
        found = resolve(u'/consumableitems/1')
        self.assertEqual(found.func, consumableItemDetail)

    def test_can_get_specific_consumableItem(self):
        c = Client()
        response = c.get(u'/consumableitems/1')

        self.assertEqual(u'ConsumableItem1', response.data['Description'])
        self.assertEqual(u'Note1', response.data['Notes'])
        self.assertEqual(1, response.data['ItemID'])

    def test_cannot_get_nonexistant_consumableItem(self):
        c = Client()
        response = c.get(u'/consumableitems/3')

        self.assertEqual(404, response.status_code)

    def test_can_create_new_consumableItem(self):
        c = Client()

        label3 = Label.objects.create();

        status3 = Status.objects.create();

        building = Building.objects.create(BuildingCode=1);

        location3 = Location.objects.create(BuildingID=building);

        collection3 = Collection.objects.create();

        # Make the request to make the consumable item...
        response = c.post(u'/consumableitems/', {u'Description' : u'ConsumableItem3',
                                                 u'ItemName':u'Batteries',
                                         u'Notes' : u'Note3',
                                         u'CategoryID' : label3.pk,
                                         u'StorageLocation' : location3.pk, u'CollectionID' : collection3.pk,
                                         u'Cost':5.00, u'Quantity':10, u'MinQuantity':10})
        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(u'ConsumableItem3', response.data[u'Description'])
        self.assertEqual(u'Note3', response.data[u'Notes'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_consumableItem(self):
        '''
        This tests that we can delete a consumable item
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/consumableitems/2')
        # Let's check the status code
        self.assertEqual(204, response.status_code)