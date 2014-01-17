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
from website.views import *

# Same for models
from website.models import *
from django.contrib.auth.models import User


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(b'<title>WebCirc 2</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

class RegistrationFormTests(TestCase):
    def test_register_new_user_url_resolves_to_new_user_view(self):
        found = resolve('/registerNewUser/')
        self.assertEqual(found.func, registerNewUser)

    def test_register_button_returns_correct_form(self):
        request = HttpRequest()
        response = registerNewUser(request)
        # Making sure the form title is there, and that it at least has all
        # proper input fields and registration button.
        self.assertIn('Operator Registration Form', response.content)
        self.assertIn('inputUsername', response.content)
        self.assertIn('inputEmail', response.content)
        self.assertIn('inputPassword', response.content)
        self.assertIn('inputConfirmPassword', response.content)
        self.assertIn('submitRegistrationBtn', response.content)

    def test_register_new_user(self):
        self.submit_registration_creates_new_user()
        self.register_new_operator_with_existing_username_fails()
        self.register_new_operator_with_existing_username_but_different_case_fails()
        self.register_new_operator_with_existing_email_fails()

    def submit_registration_creates_new_user(self):
        '''
        This simulates a POST request to create a new user and checks that the URL is good
        and that we get back expected responses.
        '''
        c = Client()

        response = c.post('/registerNewUser/', {'username': 'testuser',\
                                               'email': 'testuser@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        # Let's make sure it created the User in the database...
        testUser = User.objects.get(username=u'testuser')
        self.assertEqual(testUser.username, 'testuser')
        self.assertEqual(testUser.email, 'testuser@nothing.com')

        # Make sure the function returns a valid response
        self.assertEqual(200, response.status_code)

        # Now let's check that the server returned some HTML with a success message
        self.assertIn('succeeded', response.content)

    def register_new_operator_with_existing_username_fails(self):
        '''
        This attempts to register a user with the username of an already existing user, namely
        the testuser from the test above. It should fail and provide an error message.
        '''
        c = Client()

        response = c.post('/registerNewUser/', {'username': 'testuser',\
                                               'email': 'testuser@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

    def register_new_operator_with_existing_username_but_different_case_fails(self):
        '''
        This attempts to register a user with the username of an already existing user, namely
        the testuser from the test above, but with a different case. It should fail and provide
        an error message.
        '''
        c = Client()

        response = c.post('/registerNewUser/', {'username': 'testUser',\
                                               'email': 'testuser@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

    def register_new_operator_with_existing_email_fails(self):
        '''
        This attempts to register a user with a valid username, but with an already existing
        e-mail, namely from the test above. It should fail and provide an error message.
        '''
        c = Client()

        response = c.post('/registerNewUser/', {'username': 'testuser',\
                                               'email': 'testuser@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

    def test_new_operator_with_mismatched_passwords_fails(self):
        '''
        This attempts to create a user with a password and confirm password that
        do not match.
        '''
        c = Client()
        response = c.post('/registerNewUser/', {'username': 'testuser',\
                                               'email': 'testuser@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword1'})

        self.assertIn('failed', response.content)

    def test_too_long_username_in_registration_fails(self):
        '''
        This attempts to test what happens when the user tries to register a username that is too long.abspath
        '''
        c = Client()
        response = c.post('/registerNewUser/', {'username': 'thisisaverylongusernamethatshouldnotbeallowed',\
                                               'email': 'thisisaverylongusernamethatshouldnotbeallowed@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

    def test_username_with_invalid_characters_fails(self):
        '''
        This attempts to register a username with invalid characters. It should not let the user
        register and provide an error message.
        '''
        # Cases to test:
        # 1. Username contains one or more spaces
        # 2. Username contains non-alphanumeric characters
        c = Client()

        response = c.post('/registerNewUser/', {'username': 'testuser!',\
                                               'email': 'testuser!@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

        response = c.post('/registerNewUser/', {'username': 'testuser@',\
                                               'email': 'testuser@@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

        response = c.post('/registerNewUser/', {'username': 'testuser$',\
                                               'email': 'testuser$@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

        response = c.post('/registerNewUser/', {'username': 'test user',\
                                               'email': 'test user@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

    def test_registration_without_username_fails(self):
        c = Client()
        response = c.post('/registerNewUser/', {'email': 'testuser@nothing.com',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

    def test_registration_without_email_fails(self):
        c = Client()
        response = c.post('/registerNewUser/', {'username': 'testuser',\
                                               'password': 'testpassword',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

    def test_registration_without_password_fails(self):
        c = Client()
        response = c.post('/registerNewUser/', {'username': 'testuser',\
                                               'email': 'testuser@nothing.com',\
                                               'confirmPassword': 'testpassword'})

        self.assertIn('failed', response.content)

    def test_registration_without_confirm_password_fails(self):
        c = Client()
        response = c.post('/registerNewUser/', {'username': 'testuser',\
                                               'email': 'testuser@nothing.com',\
                                               'password': 'testpassword'})

        self.assertIn('failed', response.content)