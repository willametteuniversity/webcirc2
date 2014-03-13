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
 
class InventoryItemAPITests(TestCase):

    def setUp(self):

        invw1 = InventoryWidget.objects.create();
        invw2 = InventoryWidget.objects.create();

        brand1 = ItemBrand.objects.create();
        brand2 = ItemBrand.objects.create();

        model1 = ItemModel.objects.create();
        model2 = ItemModel.objects.create();

        label1 = Label.objects.create();
        label2 = Label.objects.create();

        status1 = Status.objects.create();
        status2 = Status.objects.create();

        building = Building.objects.create(BuildingCode=1);

        location1 = Location.objects.create(BuildingID=building);
        location2 = Location.objects.create(BuildingID=building);

        collection1 = Collection.objects.create();
        collection2 = Collection.objects.create();

        inv1 = InventoryItem.objects.create(Description=u'InventoryItem1', Notes=u'Note1', AlternateID=invw1, BrandID=brand1, ModelID=model1, CategoryID=label1, StatusID=status1, StorageLocation=location1, CollectionID=collection1)
        inv2 = InventoryItem.objects.create(Description=u'InventoryItem2', Notes=u'Note2', AlternateID=invw2, BrandID=brand2, ModelID=model2, CategoryID=label2, StatusID=status2, StorageLocation=location2, CollectionID=collection2)

    def test_can_get_list_of_inventoryItems(self):
        c = Client()
        response = c.get(u'/inventoryItems/')

        self.assertEqual(u'InventoryItem1', response.data[0]['Description'])
    	self.assertEqual(u'InventoryItem2', response.data[1]['Description'])

        found = resolve(u'/inventoryItems/')
        self.assertEqual(found.func, inventoryItemList)

    def test_inventoryItems_url_resolves_to_inventoryItemDetail(self):
        found = resolve(u'/inventoryItems/1')
        self.assertEqual(found.func, inventoryItemDetail)

    def test_can_get_specific_inventoryItem(self):
        c = Client()
        response = c.get(u'/inventoryItems/1')

        self.assertEqual(u'InventoryItem1', response.data['Description'])
        self.assertEqual(u'Note1', response.data['Notes'])
        self.assertEqual(1, response.data['ItemID'])

    def test_cannot_get_nonexistant_inventoryItem(self):
        c = Client()
        response = c.get(u'/inventoryItems/3')

        self.assertEqual(404, response.status_code)

    def test_can_create_new_inventoryItem(self):
        c = Client()

        invw3 = InventoryWidget.objects.create();

        brand3 = ItemBrand.objects.create();

        model3 = ItemModel.objects.create();

        label3 = Label.objects.create();

        status3 = Status.objects.create();

        building = Building.objects.create(BuildingCode=1);

        location3 = Location.objects.create(BuildingID=building);

        collection3 = Collection.objects.create();

        inv3 = InventoryItem.objects.create(Description=u'InventoryItem1', Notes=u'Note1', AlternateID=invw3, BrandID=brand3, ModelID=model3, CategoryID=label3, StatusID=status3, StorageLocation=location3, CollectionID=collection3)

        # Make the request to make the inventoryItem...
        response = c.post(u'/inventoryItems/', {u'Description' : u'InventoryItem3',
                                         u'Notes' : u'Note3', u'AlternateID' : invw3.pk, u'BrandID' : brand3.pk, u'StatusID' : status3.pk,
                                         u'ModelID' : model3.pk, u'CategoryID' : label3.pk,
                                         u'StorageLocation' : location3.pk, u'CollectionID' : collection3.pk})
        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(u'InventoryItem3', response.data[u'Description'])
        self.assertEqual(u'Note3', response.data[u'Notes'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_inventoryItem(self):
        '''
        This tests that we can delete a inventoryItem
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/inventoryItems/2')
        # Let's check the status code
        self.assertEqual(204, response.status_code)