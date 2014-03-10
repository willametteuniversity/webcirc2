'''
This file will test the itemHistory API
'''

from os.path import abspath, dirname
import sys

project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from website.views import *
from website.models import *


class ItemHistoryAPITest(TestCase):
    def setUp(self):
        ItemHistory.objects.create(OperatorID=1, ItemID=1, ChangeDescription=u'Reinstalled', ChangeDateTime=u'03092014')

    def test_api_url_resolves_correctly(self):
        found = resolve(u'/itemHistory/1')
        self.assertEqual(found.func, itemHistoryDetail)

    def test_can_view_item_history(self):
        client = Client()
        response = client.get(u'/itemHistory/1')
        self.assertEqual(1, response.data[0][u'OperatorID'])
        self.assertEqual(1, response.data[0][u'ItemID'])
        self.assertEqual(u'Reinstalled', response.data[0][u'ChangeDescription'])
        self.assertEqual(u'03092014', response.data[0][u'ChangeDateTime'])

    def test_cannot_view_nonexistent_history(self):
        client = Client()
        response = client.get(u'/itemHistory/2')
        self.assertEqual(404, response.status_code)