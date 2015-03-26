'''
This file contains tests that test the building creation/editing system.
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
from website.views.views import *

# Same for models
from website.models import *
from django.contrib.auth.models import User


class BuildingAPITests(TestCase):
    def setUp(self):
        '''
        Let's set up the initial database for later tests.
        '''
        col1 = Building.objects.create(BuildingName=u'Test Building 1', BuildingCode=u'TB1')
        col2 = Building.objects.create(BuildingName=u'Test Building 2', BuildingCode=u'TB2')

    def test_can_get_list_of_Buildings(self):
        '''
        This functions tests that a call to /buildings/ returns
        an appropriate list containing extant Buildings.
        '''
        # First let's simulate a GET request.
        c = Client()
        response = c.get(u'/buildings/')
        # Let's make sure the Buildings we expect to get are in there
        self.assertEqual(u'Test Building 1', response.data[0]['BuildingName'])
        self.assertEqual(u'Test Building 2', response.data[1]['BuildingName'])

    def test_buildings_url_resolves_to_BuildingList(self):
        '''
        This tests that the /Buildings/ URL resolves to the proper function
        '''
        found = resolve(u'/buildings/')
        self.assertEqual(found.func, buildingList)

    def test_Buildings_url_resolves_to_BuildingDetail(self):
        '''
        This tests that the URL with an ID number resolves to the proper function
        '''
        found = resolve(u'/buildings/1')
        self.assertEqual(found.func, buildingDetail)

        # This tests that we can resolve things by building code
        found = resolve(u'/buildings/TB1')
        self.assertEqual(found.func, buildingDetail)

    def test_can_get_specific_building(self):
        '''
        This function tests that we can get a specific Building
        '''
        c = Client()
        response = c.get(u'/buildings/1')
        # Now lets test that all the attributes are as we expect them to be
        self.assertEqual(u'Test Building 1', response.data['BuildingName'])
        self.assertEqual(u'TB1', response.data['BuildingCode'])
        self.assertEqual(1, response.data['BuildingID'])

    def test_can_get_specific_building_by_code(self):
        '''
        This function tests that we can get a specific building by code.
        '''
        c = Client()
        response = c.get(u'/buildings/TB1')
        # Now lets test that all the attributes are as we expect them to be
        self.assertEqual(u'Test Building 1', response.data['BuildingName'])
        self.assertEqual(u'TB1', response.data['BuildingCode'])
        self.assertEqual(1, response.data['BuildingID'])

    def test_cannot_get_nonexistant_Building(self):
        '''
        This function requests a Building with a non-existant ID and verifies nothing
        is returned. We expect to get a 404 response.
        '''
        c = Client()
        response = c.get(u'/buildings/3')
        self.assertEqual(404, response.status_code)

    def test_can_create_new_building(self):
        '''
        This tries to make a new Building
        '''
        c = Client()
        # Make the request to make the Building...
        response = c.post(u'/buildings/', {u'BuildingName': u'Test Building 3',
                                             u'BuildingCode': u'TB3'})

        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(u'Test Building 3', response.data[u'BuildingName'])
        self.assertEqual(u'TB3', response.data[u'BuildingCode'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_Building(self):
        '''
        This tests that we can delete a Building
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/buildings/2')

        # Let's check the status code
        self.assertEqual(204, response.status_code)

