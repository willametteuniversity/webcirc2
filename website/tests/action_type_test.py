'''
This file will test the ActionType API
'''

from os.path import abspath, dirname
import sys

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from website.views.views import *
from website.views.actionTypeAPIViews import *
from website.models import *


class ActionTypeAPITest(TestCase):
    def setUp(self):
        ActionType.objects.create(ActionTypeID=1, ActionTypeName=u'Action 1')
        ActionType.objects.create(ActionTypeID=2, ActionTypeName=u'Action 2')

    def test_api_url_resolves_correctly(self):
        found = resolve(u'/actionTypes/')
        self.assertEqual(found.func, actionTypeList)
        found = resolve(u'/actionTypes/1')
        self.assertEqual(found.func, actionTypeDetail)

    def test_can_view_all_actions(self):
        client = Client()
        response = client.get(u'/actionTypes/')
        self.assertEqual(1, response.data[0][u'ActionTypeID'])
        self.assertEqual(2, response.data[1][u'ActionTypeID'])

    def test_can_add_new_action(self):
        client = Client()
        response = client.post(u'/actionTypes/', {u'ActionTypeName': u'Action 3'})
        self.assertEqual(3, response.data[u'ActionTypeID'])
        self.assertEqual(u'Action 3', response.data[u'ActionTypeName'])
        self.assertEqual(201, response.status_code)

    def test_can_view_action_detail(self):
        client = Client()
        response = client.get(u'/actionTypes/1')
        self.assertEqual(1, response.data[u'ActionTypeID'])
        self.assertEqual(u'Action 1', response.data[u'ActionTypeName'])
        response = client.get(u'/actionTypes/2')
        self.assertEqual(2, response.data[u'ActionTypeID'])
        self.assertEqual(u'Action 2', response.data[u'ActionTypeName'])

    def test_can_edit_action_detail(self):
        client = Client()
        response = client.put(u'/actionTypes/1',
                              data=json.dumps({u'ActionTypeName': u'Action 1, edited'}),
                              content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = client.get(u'/actionTypes/1')
        self.assertEqual(u'Action 1, edited', response.data[u'ActionTypeName'])

    def test_cant_view_nonexistent_action_detail(self):
        client = Client()
        response = client.get(u'/actionTypes/3')
        self.assertEqual(404, response.status_code)

    def test_can_delete_action(self):
        client = Client()
        response = client.delete(u'/actionTypes/2')
        self.assertEqual(204, response.status_code)

    def test_cannot_delete_nonexistent_model(self):
        client = Client()
        response = client.delete(u'/actionTypes/3')
        self.assertEqual(404, response.status_code)