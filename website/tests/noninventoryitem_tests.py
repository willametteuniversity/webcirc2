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
 
class NonInventoryItemAPITests(TestCase):

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

        inv1 = NonInventoryItem.objects.create(Description=u'NonInventoryItem1', Quantity=5, Notes=u'Note1', CategoryID=label1, StatusID=status1, StorageLocation=location1, CollectionID=collection1)
        inv2 = NonInventoryItem.objects.create(Description=u'NonInventoryItem2', Quantity=10, Notes=u'Note2', CategoryID=label2, StatusID=status2, StorageLocation=location2, CollectionID=collection2)

    def test_can_get_list_of_nonInventoryItems(self):
        c = Client()
        response = c.get(u'/noninventoryitems/')

        self.assertEqual(u'NonInventoryItem1', response.data[0]['Description'])
        self.assertEqual(u'NonInventoryItem2', response.data[1]['Description'])

        found = resolve(u'/noninventoryitems/')
        self.assertEqual(found.func, nonInventoryItemList)

    def test_inventoryItems_url_resolves_to_inventoryItemDetail(self):
        found = resolve(u'/noninventoryItems/1')
        self.assertEqual(found.func, inventoryItemDetail)

    def test_can_get_specific_inventoryItem(self):
        c = Client()
        response = c.get(u'/noninventoryItems/1')

        self.assertEqual(u'NonInventoryItem1', response.data['Description'])
        self.assertEqual(u'Note1', response.data['Notes'])
        self.assertEqual(1, response.data['ItemID'])

    def test_cannot_get_nonexistant_nonInventoryItem(self):
        c = Client()
        response = c.get(u'/noninventoryitems/3')

        self.assertEqual(404, response.status_code)

    def test_can_create_new_inventoryItem(self):
        c = Client()

        label3 = Label.objects.create();

        status3 = Status.objects.create();

        building = Building.objects.create(BuildingCode=1);

        location3 = Location.objects.create(BuildingID=building);

        collection3 = Collection.objects.create();

        # Make the request to make the inventoryItem...
        response = c.post(u'/inventoryItems/', {u'Description' : u'NonInventoryItem3',
                                         u'Notes' : u'Note3', u'StatusID' : status3.pk,
                                         u'CategoryID' : label3.pk,
                                         u'StorageLocation' : location3.pk, u'CollectionID' : collection3.pk})
        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(u'NonInventoryItem3', response.data[u'Description'])
        self.assertEqual(u'Note3', response.data[u'Notes'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_inventoryItem(self):
        '''
        This tests that we can delete a inventoryItem
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/noninventoryitems/2')
        # Let's check the status code
        self.assertEqual(204, response.status_code)