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
        Label.objects.create(LabelName=u'Alone 1')
        root_1 = Label.objects.create(LabelName=u'Root 1')
        Label.objects.create(LabelName=u'Child 1', ParentCategory=root_1)

    def test_api_url_resolves_correctly(self):
        found = resolve(u'/labelsNotCategories/')
        self.assertEqual(found.func, labelsNotCategories)

    def test_items_returned_not_related(self):
        c = Client()
        response = c.get(u'/labelsNotCategories/')
        self.assertEqual(response.data[0][u'LabelName'], u'Alone 1')
        self.assertEqual(len(response.data), 1)