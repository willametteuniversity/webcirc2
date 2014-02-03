'''
This file contains tests that test the new user registration system.
'''

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


class CollectionAPITests(TestCase):
    def setUp(self):
        '''
        Let's set up the initial database for later tests.
        '''
        col1 = Collection.objects.create(CollectionName=u'Test Collection 1', CollectionDescription=u'Test Description 1')
        col2 = Collection.objects.create(CollectionName=u'Test Collection 2', CollectionDescription=u'Test Description 2')

    def test_can_get_list_of_collections(self):
        '''
        This functions tests that a call to /collections/ returns
        an appropriate list containing extant collections.
        '''
        # First let's simulate a GET request.
        c = Client()
        response = c.get(u'/collections/')
        # Let's make sure the collections we expect to get are in there
        self.assertEqual(u'Test Collection 1', response.data[0]['CollectionName'])
        self.assertEqual(u'Test Collection 2', response.data[1]['CollectionName'])

    def test_collections_url_resolves_to_collectionList(self):
        '''
        This tests that the /collections/ URL resolves to the proper function
        '''
        found = resolve(u'/collections/')
        self.assertEqual(found.func, collectionList)

    def test_collections_url_resolves_to_collectionDetail(self):
        '''
        This tests that the URL with an ID number resolves to the proper function
        '''
        found = resolve(u'/collections/1')
        self.assertEqual(found.func, collectionDetail)

    def test_can_get_specific_collection(self):
        '''
        This function tests that we can get a specific Collection
        '''
        c = Client()
        response = c.get(u'/collections/1')
        # Now lets test that all the attributes are as we expect them to be
        self.assertEqual(u'Test Collection 1', response.data['CollectionName'])
        self.assertEqual(u'Test Description 1', response.data['CollectionDescription'])
        self.assertEqual(1, response.data['CollectionID'])

    def test_cannot_get_nonexistant_collection(self):
        '''
        This function requests a collection with a non-existant ID and verifies nothing
        is returned. We expect to get a 404 response.
        '''
        c = Client()
        response = c.get(u'/collections/3')
        self.assertEqual(404, response.status_code)

    def test_can_create_new_collection(self):
        '''
        This tries to make a new Collection
        '''
        c = Client()
        # Make the request to make the collection...
        response = c.post(u'/collections/', {u'CollectionName': u'Test Collection 3',
                                             u'CollectionDescription': u'Test Description 3'})

        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(u'Test Collection 3', response.data[u'CollectionName'])
        self.assertEqual(u'Test Description 3', response.data[u'CollectionDescription'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_collection(self):
        '''
        This tests that we can delete a collection
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/collections/2')

        # Let's check the status code
        self.assertEqual(204, response.status_code)

