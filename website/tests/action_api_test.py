'''
This file will test the Action API
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


class ActionAPITest(TestCase):
    def setUp(self):
#        ItemBrand.objects.create(BrandID=1, BrandName=u'Brand 1')
#        ItemBrand.objects.create(BrandID=2, BrandName=u'Brand 2')
        pass

    def test_api_urls_resolve_correctly(self):
#        found = resolve(u'/brands/')
#        self.assertEqual(found.func, itemBrandList)
#        found = resolve(u'/brands/1')
#        self.assertEqual(found.func, itemBrandDetail)
        pass

    def test_can_view_all_actions(self):
#        client = Client()
#        response = client.get(u'/brands/')
#        self.assertEqual(1, response.data[0][u'BrandID'])
#        self.assertEqual(2, response.data[1][u'BrandID'])
        pass

    def test_can_add_new_action(self):
#        client = Client()
#        response = client.post(u'/brands/', {u'BrandName': u'Brand 3'})
#        self.assertEqual(3, response.data[u'BrandID'])
#        self.assertEqual(u'Brand 3', response.data[u'BrandName'])
#        self.assertEqual(201, response.status_code)
        pass

    def test_can_view_one_action(self):
#        client = Client()
#        response = client.get(u'/brands/1')
#        self.assertEqual(1, response.data[u'BrandID'])
#        self.assertEqual(u'Brand 1', response.data[u'BrandName'])
#        response = client.get(u'/brands/2')
#        self.assertEqual(2, response.data[u'BrandID'])
#        self.assertEqual(u'Brand 2', response.data[u'BrandName'])
        pass

    def test_can_edit_action(self):
#        client = Client()
#        response = client.put(u'/brands/1',
#                              data=json.dumps({u'BrandName': u'Brand 1, edited'}),
#                              content_type='application/json')
#        self.assertEqual(200, response.status_code)
#        response = client.get(u'/brands/1')
#        self.assertEqual(u'Brand 1, edited', response.data[u'BrandName'])
        pass

    def test_cant_view_nonexistent_action(self):
#        client = Client()
#        response = client.get(u'/brands/3')
#        self.assertEqual(404, response.status_code)
        pass

    def test_can_delete_action(self):
#        client = Client()
#        response = client.delete(u'/brands/2')
#        self.assertEqual(204, response.status_code)
        pass

    def test_cannot_delete_nonexistent_action(self):
#        client = Client()
#        response = client.delete(u'/brands/3')
#        self.assertEqual(404, response.status_code)
        pass

    def test_can_get_inventory_items(self):
        pass

    def test_can_get_consumable_items(self):
        pass

    def test_can_get_non_inventory_items(self):
        pass