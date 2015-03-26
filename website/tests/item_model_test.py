'''
This file will test the itemModel API
'''

from os.path import abspath, dirname
import sys

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from website.views.views import *
from website.models import *


class ItemModelAPITest(TestCase):
    def setUp(self):
        ItemModel.objects.create(ModelID=1, ModelDesignation=u'Model type 1')
        ItemModel.objects.create(ModelID=2, ModelDesignation=u'Model type 2')

    def test_api_url_resolves_correctly(self):
        found = resolve(u'/models/')
        self.assertEqual(found.func, itemModelList)
        found = resolve(u'/models/1')
        self.assertEqual(found.func, itemModelDetail)

    def test_can_view_all_item_models(self):
        client = Client()
        response = client.get(u'/models/')
        self.assertEqual(1, response.data[0][u'ModelID'])
        self.assertEqual(2, response.data[1][u'ModelID'])

    def test_can_add_new_item_model(self):
        client = Client()
        response = client.post(u'/models/', {u'ModelDesignation': u'Model type 3'})
        self.assertEqual(3, response.data[u'ModelID'])
        self.assertEqual(u'Model type 3', response.data[u'ModelDesignation'])
        self.assertEqual(201, response.status_code)

    def test_can_view_item_model_detail(self):
        client = Client()
        response = client.get(u'/models/1')
        self.assertEqual(1, response.data[u'ModelID'])
        self.assertEqual(u'Model type 1', response.data[u'ModelDesignation'])
        response = client.get(u'/models/2')
        self.assertEqual(2, response.data[u'ModelID'])
        self.assertEqual(u'Model type 2', response.data[u'ModelDesignation'])

    def test_can_edit_item_model_detail(self):
        client = Client()
        response = client.put(u'/models/1',
                              data=json.dumps({u'ModelDesignation': u'Model type 1, edited'}),
                              content_type='application/json')
        self.assertEqual(200, response.status_code)
        response = client.get(u'/models/1')
        self.assertEqual(u'Model type 1, edited', response.data[u'ModelDesignation'])

    def test_cant_view_nonexistent_item_model_detail(self):
        client = Client()
        response = client.get(u'/models/3')
        self.assertEqual(404, response.status_code)

    def test_can_delete_model(self):
        client = Client()
        response = client.delete(u'/models/2')
        self.assertEqual(204, response.status_code)

    def test_cannot_delete_nonexistent_model(self):
        client = Client()
        response = client.delete(u'/models/3')
        self.assertEqual(404, response.status_code)