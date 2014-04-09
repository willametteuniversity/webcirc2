'''
This file will test the labelsNotCategories API
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


class LabelNotCategoryTest(TestCase):
    def setUp(self):
        pass

    def test_api_url_resolves_correctly(self):
        found = resolve(u'/labelsNotCategories/')
        self.assertEqual(found.func, labelsNotCategories)

    def test_items_returned_not_parents(self):
        client = Client()
        response = client.get(u'/labelsNotCategories/')
        # get a list of all labels, make sure none of them have a parent in response

    def test_items_returned_not_children(self):
        client = Client()
        response = client.get(u'/labelsNotCategories/')
        # make sure each thing in response have a parent of None