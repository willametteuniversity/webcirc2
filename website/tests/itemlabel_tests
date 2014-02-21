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


class ItemLabelAPITests(TestCase):
    def setUp(self):
        '''
        Let's set up the initial database for later tests.
        '''
        label1 = ItemLabel.objects.create(LabelName=u'Test Label 1')
        label2 = ItemLabel.objects.create(LabelName=u'Test Label 2', ParentCategory=label1)
        itemLabel1 = ItemLabel.objects.create(LabelID=label1)


    def test_can_get_list_of_itemlabels(self):
        '''
        This functions tests that a call to /itemlabels/ returns
        an appropriate list containing extant labels.
        '''
        # First let's simulate a GET request.
        c = Client()
        response = c.get(u'/itemlabels/')
        # Let's make sure the labels we expect to get are in there
        self.assertEqual(u'Test Label 1', response.data[0]['LabelID'])
        self.assertEqual(u'Test Label 2', response.data[1]['LabelID'])

    def test_labels_url_resolves_to_itemLabelList(self):
        '''
        This tests that the /labels/ URL resolves to the proper function
        '''
        found = resolve(u'/labels/')
        self.assertEqual(found.func, itemLabelList)

    def test_labels_url_resolves_to_itemLabelDetail(self):
        '''
        This tests that the URL with an ID number resolves to the proper function
        '''
        found = resolve(u'/itemlabels/1')
        self.assertEqual(found.func, itemLabelDetail)

    def test_can_get_specific_label(self):
        '''
        This function tests that we can get a specific Label
        '''
        c = Client()
        response = c.get(u'/itemlabels/1')
        # Now lets test that all the attributes are as we expect them to be
        self.assertEqual(u'Test Label 1', response.data[u'LabelID'])
        self.assertEqual(1, response.data[u'LabelID'])

    def test_cannot_get_nonexistant_label(self):
        '''
        This function requests a label with a non-existant ID and verifies nothing
        is returned. We expect to get a 404 response.
        '''
        c = Client()
        response = c.get(u'/itemlabels/3')
        self.assertEqual(404, response.status_code)

    def test_can_create_new_itemlabel(self):
        '''
        This tries to make a new Label
        '''
        c = Client()
        # Make the request to make the label...
        response = c.post(u'/itemlabels/', {u'LabelID': u'Test Label 3', u'ItemID': u'1'})

        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(201, response.status_code)

    def test_can_create_child_itemlabel(self):
        '''
        This tries to create a new label with some other label as the parent
        '''
        c = Client()
        response = c.post(u'/labels/', {u'LabelName':u'Test Label 3', u'ParentCategory':u'2'})
        newLabel = Label.objects.get(LabelID=3)
        parentLabel = Label.objects.get(LabelID=2)
        self.assertEqual(newLabel.ParentCategory.LabelID, parentLabel.LabelID)

    def test_can_delete_itemlabel(self):
        '''
        This tests that we can delete a label
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/itemlabels/2')

        # Let's check the status code
        self.assertEqual(204, response.status_code)

