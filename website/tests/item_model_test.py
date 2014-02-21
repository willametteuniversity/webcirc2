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
from django.http import HttpRequest
from website.views import *
from website.models import *
from django.contrib.auth.models import User

class CollectionAPITest(TestCase):
    def setUp(self):
        pass

    def test_can_view_all_item_models(self):
        pass

    def test_can_add_new_item_model(self):
        pass

    def test_can_view_item_model_detail(self):
        pass
    
    def test_can_edit_item_model_detail(self):
        pass
