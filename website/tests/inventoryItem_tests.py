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
	   inv1 = InventoryItem.objects.create(Description='InventoryItem1', Notes='Note1')
	   inv2 = InventoryItem.objects.create(Description='InventoryItem2', Notes='Note2')

    def test_can_get_list_of_reservations(self):
        c = Client()
        response = c.get(u'/inventoryItems/')

        self.assertEqual(u'InventoryItem1', response.data[0]['Description'])
    	self.assertEqual(u'InventoryItem2', response.data[1]['Description'])

        found = resolve(u'/inventoryItems/')
        serlf.assertEqual(found.func, inventoryItemList)

    def test_inventoryItems_url_resolves_to_inventoryItemDetail(self):
	   found = resolve(u'/inventoryItems/1')
	   self.assertEqual(found.func, inventoryItemDetail)

    def test_can_get_specific_inventoryItem(self):
	   c = Client()
	   response = c.get(u'/inventoryItems/1')

	   self.assertEqual(u'InventoryItem1', response.data['Description'])
	   self.assertEqual(u'Note1', response.data['Notes'])
	   self.assertEqual(1, response.data['InventoryItemID'])

    def test_cannot_get_nonexistant_inventoryItem(self):
        c = Client()
        response = c.get(u'/inventoryItems/3')

        self.assertEqual(404, response.status_code)

    def test_can_create_new_inventoryItem(self):
        c = Client()
        # Make the request to make the inventoryItem...
        response = c.post(u'/inventoryItems/', {u'Description' : u'InventoryItem3',
                                         u'Notes' : u'Note3'})
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