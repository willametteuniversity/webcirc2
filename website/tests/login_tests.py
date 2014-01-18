'''
This file contains tests that test the logging in functionality.
'''

from website.views import login
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.test.client import Client
from django.http import HttpRequest

from website.models import *
from django.contrib.auth.models import User

class LoginTests(TestCase):
    def test_login_user(self):
        self.login_succeeds()
        self.login_fails_with_nonexistant_user()
        self.login_fails_with_wrong_password()

    def test_login_url_resolves_properly(self):
        '''
        This function ensures that the /login/ URL resolves properly.
        '''
        found = resolve(u'/login/')
        self.assertEqual(found.func, login)

    def login_fails_with_nonexistant_user(self):
        '''
        This function attempts to login with a user that does not exist
        '''
        c = Client()
        response = c.post(u'/login/', {u'username': u'testuser1', u'password': u'testpassword'})
        self.assertIn(u'failed', response.content)

    def login_succeeds(self):
        '''
        This test attempts to login with a known good username and password.
        '''

        # First create a test user
        newUser = User.objects.create_user(username=u'testuser', password=u'testpassword')
        newUser.save()

        # Now do a login
        c = Client()
        response = c.post(u'/login/', {u'username': u'testuser', u'password': u'testpassword'})
        self.assertIn(u'succeeded', response.content)

    def login_fails_with_wrong_password(self):
        '''
        This test attempts to login with a known good username but bad password.
        '''
        c = Client()
        response = c.post(u'/login/', {u'username': u'testuser', u'password': u'testpassword1'})
        self.assertIn(u'failed', response.content)