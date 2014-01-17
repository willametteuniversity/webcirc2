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
from django.http import HttpRequest

# Import all of our views for testing
from website.views import *


class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_register_new_user_url_resolves_to_new_user_view(self):
        found = resolve('/registerNewUser/')
        self.assertEqual(found.func, registerNewUser)

    def test_index_page_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertTrue(response.content.startswith(b'\n<!DOCTYPE html>'))
        self.assertIn(b'<title>WebCirc 2</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

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