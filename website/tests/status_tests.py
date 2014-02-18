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
 
class StatusAPITests(TestCase):

    def setUp(self):
	   inv1 = Status.objects.create(StatusDescription='Status1')
	   inv2 = Status.objects.create(StatusDescription='Status2')

    def test_can_get_list_of_reservations(self):
        c = Client()
        response = c.get(u'/states/')

        self.assertEqual(u'Status1', response.data[0]['StatusDescription'])
    	self.assertEqual(u'Status2', response.data[1]['StatusDescription'])

        found = resolve(u'/states/')
        serlf.assertEqual(found.func, stateList)

    def test_states_url_resolves_to_stateDetail(self):
	   found = resolve(u'/states/1')
	   self.assertEqual(found.func, stateDetail)

    def test_can_get_specific_state(self):
	   c = Client()
	   response = c.get(u'/states/1')

	   self.assertEqual(u'Status1', response.data['StatusDescription'])
	   self.assertEqual(1, response.data['StatusID'])

    def test_cannot_get_nonexistant_state(self):
        c = Client()
        response = c.get(u'/states/3')

        self.assertEqual(404, response.status_code)

    def test_can_create_new_state(self):
        c = Client()
        # Make the request to make the state...
        response = c.post(u'/states/', {u'StatusDescription' : u'Status3'})
        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(u'Status3', response.data[u'StatusDescription'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_state(self):
        '''
        This tests that we can delete a state
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/states/2')
        # Let's check the status code
        self.assertEqual(204, response.status_code)