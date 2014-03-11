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

#FIXTURE_DIR = ('/home/hayden/PycharmProjects/webcirc2/website/fixtures',)


class ItemHistoryAPITest(TestCase):
    fixtures = ['User.json', 'InventoryItem.json', 'Label.json', 'Status.json']

    def setUp(self):
        ItemHistory.objects.create(OperatorID=User.objects.filter(id=1)[0],
                                   ItemID=InventoryItem.objects.filter(ItemID=1)[0],
                                   ChangeDescription=u'Reinstalled',
                                   ChangeDateTime=u'03092014')

    def test_api_url_resolves_correctly(self):
        found = resolve(u'/itemHistory/1')
        self.assertEqual(found.func, itemHistoryDetail)

    def test_can_view_item_history(self):
        client = Client()
        response = client.get(u'/itemHistory/1')
        data = json.loads(response.content)
        self.assertEqual(u'user1', data[0][u'Username'])
        self.assertEqual(1, data[0][u'ItemID'])
        self.assertEqual(u'Reinstalled', data[0][u'ChangeDescription'])
        self.assertEqual(u'03092014', data[0][u'ChangeDateTime'])

    def test_cannot_view_nonexistent_history(self):
        client = Client()
        response = client.get(u'/itemHistory/2')
        self.assertEqual(404, response.status_code)