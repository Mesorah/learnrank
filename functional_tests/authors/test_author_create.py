from django.urls import reverse
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests


class TestAuthorCreate(BaseWebDriverForFunctionalTests):
    def setUp(self):
        super().setUp()
        self.wait = self.delay()

        self.form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

    def get_all_placeholders(self, inputs):
        inputs_information = []

        for input in inputs:
            placeholder = input.get_attribute('placeholder')
            name = input.get_attribute('name')
            inputs_information.append((name, placeholder))

        return inputs_information

    def validate_placeholders(self, inputs_information):
        correct_inputs = {
            'username': 'Ex: Gabriel Rodrigues',
            'email': 'Ex: gabrielrodrigues@example.com',
            'password1': 'Ex 23#$1fsgKDL!',
            'password2': 'Repeat your password'
        }

        for name, placeholder in inputs_information:
            input = correct_inputs[name]

            if placeholder == input:
                pass
            else:
                self.fail((placeholder, input))

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # He sees the Login button and presses it.
        # self.wait.until(EC.visibility_of_element_located((
        #     By.CLASS_NAME, 'login-button'
        # ))).click()

        # He realizes that he doesn't have an account
        # and clicks the Sign up button.
        # self.browser.find_element(By.CLASS_NAME, 'sign-up-button')

        # See the registration screen
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))
        self.assertEqual(self.browser.title, 'Sign Up')

        # Check that all inputs have placeholders.
        inputs = form.find_elements(By.CLASS_NAME, 'form-control')
        inputs_information = self.get_all_placeholders(inputs)
        self.validate_placeholders(inputs_information)

    def test_registration_invalid_fields_and_success_redirect(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))

        # See the form and decide to fill it out.
        username = form.find_element(By.ID, 'id_username')
        email = form.find_element(By.ID, 'id_email')
        password1 = form.find_element(By.ID, 'id_password1')
        password2 = form.find_element(By.ID, 'id_password2')

        username.send_keys('abcd')
        email.send_keys('testing@example.com')
        password1.send_keys('abcd1234')
        password2.send_keys('defg5678')

        # Send the form and notice errors on your screen
        form.submit()

        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))

        errors = self.browser.find_elements(By.CLASS_NAME, 'errorlist')

        errors_messages = [error.text for error in errors]

        self.assertIn(
            'Without the use of symbols.',
            errors_messages
        )

        self.assertIn(
            'Passwords are not the same.',
            errors_messages
        )

        # Decided to fix the gaps that caused errors and resend it again.
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))

        username = form.find_element(By.ID, 'id_username')
        email = form.find_element(By.ID, 'id_email')
        password1 = form.find_element(By.ID, 'id_password1')
        password2 = form.find_element(By.ID, 'id_password2')

        username.send_keys('testing')
        email.send_keys('testing@example.com')
        password1.send_keys('testing12!@1dsFG')
        password2.send_keys('testing12!@1dsFG')

        form.submit()

        # It worked and was redirected already logged in to the homepage.
        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'home'
        )))
        self.assertEqual(self.browser.title, 'Home')
