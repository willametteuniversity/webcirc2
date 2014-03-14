"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from os.path import abspath, dirname
import sys
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest

# Import all of our views for testing
from website.views.views import *

# Same for models
from website.models import *
from django.contrib.auth.models import User

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        '''
        This test insures the root URL resolves properly.
        '''
        found = resolve(u'/')
        self.assertEqual(found.func, index)

    def test_index_page_returns_correct_html(self):
        '''
        This test makes sure the index page returns some valid HTML.
        '''
        request = HttpRequest()
        response = index(request)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(b'<title>WebCirc 2</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

    def test_navbar_not_shown_when_not_logged_in(self):
        '''
        This test ensures that none of the navbar is shown if the user is not logged in.
        '''
        request = HttpRequest()
        response = index(request)
        self.assertNotIn(u'New', response)
        self.assertNotIn(u'Daily', response)
        self.assertNotIn(u'Monthly', response)
        self.assertNotIn(u'Overdue Stuff', response)
        self.assertNotIn(u'Admin Tools', response)
