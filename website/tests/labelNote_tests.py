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
 
class LabelNotesAPITests(TestCase):

    def setUp(self):
	   
        lbl1 = Label.objects.create(LabelName='Label1', ParentCategory=self.id)
        lbl2 = Label.objects.create(LabelName='Label2', ParentCategory=self.id)

        lbln1 = LabelNotes.objects.create(LabelNote='LabelNotes1', LabelID=lbl1.LabelID)
        lbln2 = LabelNotes.objects.create(LabelNote='LabelNotes2', LabelID=lbl2.LabelID)

    def test_can_get_list_of_reservations(self):
        c = Client()
        response = c.get(u'/labelNotes/')

        self.assertEqual(u'LabelNotes1', response.data[0]['LabelNote'])
    	self.assertEqual(u'LabelNotes2', response.data[1]['LabelNote'])

        found = resolve(u'/labelNotes/')
        serlf.assertEqual(found.func, labelNoteList)

    def test_labelNotes_url_resolves_to_labelNoteDetail(self):
	   found = resolve(u'/labelNotes/1')
	   self.assertEqual(found.func, labelNoteDetail)

    def test_can_get_specific_labelNote(self):
	   c = Client()
	   response = c.get(u'/labelNotes/1')

	   self.assertEqual(u'LabelNotes1', response.data['LabelNote'])
	   self.assertEqual(1, response.data['LabelNotesID'])

    def test_cannot_get_nonexistant_labelNote(self):
        c = Client()
        response = c.get(u'/labelNotes/3')

        self.assertEqual(404, response.status_code)

    def test_can_create_new_labelNote(self):
        c = Client()
        # Make the request to make the labelNote...
        response = c.post(u'/labelNotes/', {u'LabelNote' : u'LabelNotes3'})
        # We expect the server to return a proper status code and the item it made. So lets check all of those:
        self.assertEqual(u'LabelNotes3', response.data[u'LabelNote'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_labelNote(self):
        '''
        This tests that we can delete a labelNote
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/labelNotes/2')
        # Let's check the status code
        self.assertEqual(204, response.status_code)