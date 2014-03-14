'''
This file contains tests that test the new user registration system.
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


class RegistrationFormTests(TestCase):
    def test_register_new_user_url_resolves_to_new_user_view(self):
        '''
        This tests that the register new user URL resolves to the proper
        function.
        '''
        found = resolve(u'/registerNewUser/')
        self.assertEqual(found.func, registerNewUser)

    def test_register_button_returns_correct_form(self):
        '''
        This tests that the register button returns a form containing
        at least the proper form inputs.
        '''
        request = HttpRequest()
        response = registerNewUser(request)
        # Making sure the form title is there, and that it at least has all
        # proper input fields and registration button.
        self.assertIn(u'Operator Registration Form', response.content)
        self.assertIn(u'inputUsername', response.content)
        self.assertIn(u'inputEmail', response.content)
        self.assertIn(u'inputPassword', response.content)
        self.assertIn(u'inputConfirmPassword', response.content)
        self.assertIn(u'submitRegistrationBtn', response.content)

    def test_register_new_user(self):
        '''
        This runs some related tests in sequence because we need the created user from the first
        function to be in the database to test the subsequent functions.
        '''
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

        response = c.post(u'/registerNewUser/', {u'username': u'testuser',
                                                 u'email': u'testuser@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        # Let's make sure it created the User in the database...
        testUser = User.objects.get(username=u'testuser')
        self.assertEqual(testUser.username, u'testuser')
        self.assertEqual(testUser.email, u'testuser@nothing.com')

        # Make sure the function returns a valid response
        self.assertEqual(200, response.status_code)

        # Now let's check that the server returned some HTML with a success message
        self.assertIn(u'succeeded', response.content)

    def register_new_operator_with_existing_username_fails(self):
        '''
        This attempts to register a user with the username of an already existing user, namely
        the testuser from the test above. It should fail and provide an error message.
        '''
        c = Client()

        response = c.post(u'/registerNewUser/', {u'username': u'testuser',
                                                 u'email': u'testuser@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def register_new_operator_with_existing_username_but_different_case_fails(self):
        '''
        This attempts to register a user with the username of an already existing user, namely
        the testuser from the test above, but with a different case. It should fail and provide
        an error message.
        '''
        c = Client()

        response = c.post(u'/registerNewUser/', {u'username': u'testUser',
                                                 u'email': u'testuser@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def register_new_operator_with_existing_email_fails(self):
        '''
        This attempts to register a user with a valid username, but with an already existing
        e-mail, namely from the test above. It should fail and provide an error message.
        '''
        c = Client()
        response = c.post(u'/registerNewUser/', {u'username': u'testuser1',
                                                 u'email': u'testuser@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def test_new_operator_with_mismatched_passwords_fails(self):
        '''
        This attempts to create a user with a password and confirm password that
        do not match.
        '''
        c = Client()
        response = c.post(u'/registerNewUser/', {u'username': u'testuser',
                                                 u'email': u'testuser@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword1'})

        self.assertIn(u'failed', response.content)

    def test_too_long_username_in_registration_fails(self):
        '''
        This attempts to test what happens when the user tries to register a username that is too long.abspath
        '''
        c = Client()
        response = c.post(u'/registerNewUser/', {u'username': u'thisisaverylongusernamethatshouldnotbeallowed',
                                                 u'email': u'thisisaverylongusernamethatshouldnotbeallowed@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def test_username_with_invalid_characters_fails(self):
        '''
        This attempts to register a username with invalid characters. It should not let the user
        register and provide an error message.
        '''
        # Cases to test:
        # 1. Username contains one or more spaces
        # 2. Username contains non-alphanumeric characters
        c = Client()

        response = c.post(u'/registerNewUser/', {u'username': u'testuser!',
                                                 u'email': u'testuser!@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

        response = c.post(u'/registerNewUser/', {u'username': u'testuser@',
                                                 u'email': u'testuser@@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

        response = c.post(u'/registerNewUser/', {u'username': u'testuser$',
                                                 u'email': u'testuser$@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

        response = c.post(u'/registerNewUser/', {u'username': u'test user',
                                                 u'email': u'test user@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def test_registration_without_username_fails(self):
        '''
        This attempts to register without a username.
        '''
        c = Client()
        response = c.post(u'/registerNewUser/', {u'email': u'testuser@nothing.com',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def test_registration_without_email_fails(self):
        '''
        This attempts to register without an e-mail.
        '''
        c = Client()
        response = c.post(u'/registerNewUser/', {u'username': u'testuser',
                                                 u'password': u'testpassword',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def test_registration_without_password_fails(self):
        '''
        This tests registration without sending a password
        '''
        c = Client()
        response = c.post(u'/registerNewUser/', {u'username': u'testuser',
                                                 u'email': u'testuser@nothing.com',
                                                 u'confirmPassword': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def test_registration_without_confirm_password_fails(self):
        '''
        This tests registration without sending a password confirmation.
        '''
        c = Client()
        response = c.post(u'/registerNewUser/', {u'username': u'testuser',
                                                 u'email': u'testuser@nothing.com',
                                                 u'password': u'testpassword'})

        self.assertIn(u'failed', response.content)

    def test_registration_get_returns_501(self):
        '''
        This tests that making a GET request to /registerNewUser/ returns a proper 501 page/status
        '''
        c = Client()
        response = c.get(u'/registerNewUser/', {u'username': u'testuser',
                                                u'email': u'testuser@nothing.com',
                                                u'password': u'testpassword'})
        self.assertEqual(501, response.status_code)
