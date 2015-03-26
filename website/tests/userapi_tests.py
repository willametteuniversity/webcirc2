'''
This file contains tests that test the User API.
'''

from os.path import abspath, dirname
import sys
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest

# Import all of our views for testing
from website.views.views import *

# Same for models
from website.models import *
from django.contrib.auth.models import User


class CollectionAPITests(TestCase):
    def setUp(self):
        '''
        Let's set up the initial database for later tests.
        '''
        self.fail("Implement this!")

    def test_can_get_list_of_users(self):
        '''
        This functions tests that a call to /collections/ returns
        an appropriate list containing extant collections.
        '''
        self.fail("Implement this!")

    def test_users_url_resolves_to_userList(self):
        '''
        This tests that the /users/ URL resolves to the proper function
        '''
        self.fail("Implement this!")

    def test_users_url_resolves_to_userDetail(self):
        '''
        This tests that the URL with an ID number resolves to the proper function
        '''
        self.fail("Implement this!")

    def test_can_get_specific_user(self):
        '''
        This function tests that we can get a specific User
        '''
        self.fail("Implement this!")


    def test_cannot_get_nonexistant_user(self):
        '''
        This tests that we cannot get a non-existanat user
        '''
        self.fail("Implement this!")

    def test_can_create_new_user(self):
        '''
        This tries to make a new user
        '''
        self.fail("Implement this!")

    def test_can_delete_user(self):
        '''
        This tests that we can delete a user
        '''
        self.fail("Implement this!")

