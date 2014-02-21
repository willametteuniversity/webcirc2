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
 
class ImageAPITests(TestCase):

    def setUp(self):
	   inv1 = Image.objects.create(ImageName='Image1')
	   inv2 = Image.objects.create(ImageName='Image2')

    def test_can_get_list_of_images(self):
        c = Client()
        response = c.get(u'/images/')

        self.assertEqual(u'Image1', response.data[0]['ImageName'])
    	self.assertEqual(u'Image2', response.data[1]['ImageName'])

        found = resolve(u'/images/')
        self.assertEqual(found.func, imageList)

    def test_images_url_resolves_to_imageDetail(self):
	   found = resolve(u'/images/1')
	   self.assertEqual(found.func, imageDetail)

    def test_can_get_specific_image(self):
	   c = Client()
	   response = c.get(u'/images/1')

	   self.assertEqual(1, response.data['ImageID'])

    def test_cannot_get_nonexistant_image(self):
        c = Client()
        response = c.get(u'/images/3')

        self.assertEqual(404, response.status_code)

    def test_can_create_new_image(self):
        c = Client()
        # Make the request to make the image...
        response = c.post(u'/images/', {u'ImageName' : u'Image3'})
        # We expect the server to return a proper status code and the item it made. So lets check all of those
        self.assertEqual(u'Image3', response.data[u'ImageName'])
        self.assertEqual(201, response.status_code)

    def test_can_delete_image(self):
        '''
        This tests that we can delete a image
        '''
        c = Client()
        # Make the delete request
        response = c.delete(u'/images/2')
        # Let's check the status code
        self.assertEqual(204, response.status_code)