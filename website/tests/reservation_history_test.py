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
from website.views.views import *
from website.models import *


class ReservationHistoryAPITest(TestCase):
    fixtures = ['User.json', 'InventoryItem.json', 'Label.json', 'Status.json', 'Reservation.json']

    def setUp(self):
        ReservationHistory.objects.create(OperatorID=User.objects.filter(id=1)[0],
                                          ReservationID=Reservation.objects.filter(ReservationID=1)[0],
                                          ChangeDescription=u'Reinstalled',
                                          ChangeDateTime=u'03092014')

    def test_api_url_resolves_correctly(self):
        found = resolve(u'/reservationHistory/1')
        self.assertEqual(found.func, reservationHistoryDetail)

    def test_can_view_reservation_history(self):
        client = Client()
        response = client.get(u'/reservationHistory/1')
        data = json.loads(response.content)
        self.assertEqual(u'user1', data[0][u'Username'])
        self.assertEqual(1, data[0][u'ReservationID'])
        self.assertEqual(u'Reinstalled', data[0][u'ChangeDescription'])
        self.assertEqual(u'03092014', data[0][u'ChangeDateTime'])

    def test_cannot_view_nonexistent_history(self):
        client = Client()
        response = client.get(u'/reservationHistory/2')
        self.assertEqual(404, response.status_code)