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


class LabelAPITests(TestCase):
    def setUp(self):
        '''
        Let's set up the initial database for later tests.
        '''
        label1 = Label.objects.create(LabelName=u'Test Label 1')
        label2 = Label.objects.create(LabelName=u'Test Label 2', ParentCategory=label1)

    def test_can_get_list_of_labels(self):
        '''
        This functions tests that a call to /labels/ returns
        an appropriate list containing extant labels.
        '''
        # First let's simulate a GET request.
        c = Client()
        response = c.get(u'/labels/')
        # Let's make sure the labels we expect to get are in there
        self.assertEqual(u'Test Label 1', response.data[0]['LabelName'])
        self.assertEqual(u'Test Label 2', response.data[1]['LabelName'])

    def test_labels_url_resolves_to_labelList(self):
        '''
        This tests that the /labels/ URL resolves to the proper function
        '''
        found = resolve(u'/labels/')
        self.assertEqual(found.func, labelList)

    def test_labels_url_resolves_to_labelDetail(self):
        '''
        This tests that the URL with an ID number resolves to the proper function
        '''
        found = resolve(u'/labels/1')
        self.assertEqual(found.func, labelDetail)

    def test_can_get_specific_label(self):
        '''
        This function tests that we can get a specific Label
        '''
        c = Client()
        response = c.get(u'/labels/1')
        # Now lets test that all the attributes are as we expect them to be
        self.assertEqual(u'Test Label 1', response.data[u'LabelName'])
        self.assertEqual(1, response.data[u'LabelID'])

    def test_label_has_proper_parent(self):
        '''
        This function tests to make sure our parent relationship is correct
        '''
        l1 = Label.objects.get(LabelID=1)
        l2 = Label.objects.get(LabelID=2)
        self.assertEqual(l2.ParentCategory, l1)

    def test_cannot_get_nonexistant_label(self):
        '''
        This function requests a label with a non-existant ID and verifies nothing
        is returned. We expect to get a 404 response.
        '''
        c = Client()
        response = c.get(u'/labels/3')
        self.assertEqual(404, response.status_code)

    def test_can_create_new_label(self):
        '''
        This tries to make a new Label
        '''
        c = Client()
        # Make the request to make the label...
        response = c.post(u'/labels/', {u'LabelName': u'Test Label 3'})

        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(201, response.status_code)
        self.assertEqual(u'Test Label 3', response.data[u'LabelName'])


    def test_can_create_child_label(self):
        '''
        This tries to create a new label with some other label as the parent
        '''
        c = Client()
        response = c.post(u'/labels/', {u'LabelName':u'Test Label 3', u'ParentCategory':u'2'})
        newLabel = Label.objects.get(LabelID=3)
        parentLabel = Label.objects.get(LabelID=2)
        self.assertEqual(newLabel.ParentCategory.LabelID, parentLabel.LabelID)

    def test_can_delete_label(self):
        '''
        This tests that we can delete a label
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/labels/2')

        # Let's check the status code
        self.assertEqual(204, response.status_code)

    def test_can_resolve_category_hierarchy(self):
        '''
        This tests the category hierarchy view resolves properly
        '''
        found = resolve(u'/categoryHierarchy/')
        self.assertEqual(found.func, categoryHierarchy)

    def test_can_get_category_hierarchy(self):
        '''
        This tests that a hierarchical JSON data structure can be retrieved at the /categoryHierarchy/ view.
        '''
        rootObj = Label.objects.create(LabelName=u'RootObject')
        childObj = Label.objects.create(LabelName=u'ChildObj', ParentCategory=rootObj)
        c = Client()

        response = c.get(u'/categoryHierarchy/')
        self.assertEqual(200, response.status_code)
