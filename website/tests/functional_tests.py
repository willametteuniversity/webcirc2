from os.path import abspath, dirname
import sys
project_dir = abspath(dirname(dirname(__file__)))
sys.path.insert(0, project_dir)
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewOperatorRegistrationTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_register_new_operator(self):
        '''
        This checks that we can register a new user if we will out the form with all the proper values.
        '''
        self.browser.get('http://localhost:8000')
        assert 'WebCirc 2' in self.browser.title, 'Browser title was '+self.browser.title

        # Click the button to bring up the registration form
        registerFormBtn = self.browser.find_element_by_id('registerBtn')
        registerFormBtn.click();

        # Fill out the form
        usernameInput = self.browser.find_element_by_id('inputUsername')
        emailInput = self.browser.find_element_by_id('inputEmail')
        passwordInput = self.browser.find_element_by_id('inputPassword')
        confirmPasswordInput = self.browser.find_element_by_id('inputConfirmPassword')
        usernameInput.send_keys('testuser')
        emailInput.send_keys('testuser@nothing.com')
        passwordInput.send_keys('testpassword')
        confirmPasswordInput.send_keys('testpassword')

        # Let's submit the form
        submitRegistrationBtn = self.browser.find_element_by_id('submitRegistrationBtn')
        submitRegistrationBtn.click()

        # We should get back a success message that replaces the registration form.
        registrationSuccess = self.browser.find_element_by_id('registrationSuccessMessage')

        self.fail('Finish the test!')



