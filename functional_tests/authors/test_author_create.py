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

    def send_input_keys(self, username, email, password1, password2):
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))

        username_field = form.find_element(By.ID, 'id_username')
        email_field = form.find_element(By.ID, 'id_email')
        password1_field = form.find_element(By.ID, 'id_password1')
        password2_field = form.find_element(By.ID, 'id_password2')

        username_field.clear()
        email_field.clear()
        password1_field.clear()
        password2_field.clear()

        username_field.send_keys(username)
        email_field.send_keys(email)
        password1_field.send_keys(password1)
        password2_field.send_keys(password2)

        form.submit()

        return form

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # He sees the Login button and presses it.
        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'login-button'
        ))).click()

        # He realizes that he doesn't have an account
        # and clicks the Sign up button.
        self.browser.find_element(By.CLASS_NAME, 'sign-up-button')

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

        # See the form and decide to fill it out and send
        # the form and notice errors on your screen
        self.send_input_keys(
            'abcd', 'testing@example.com', 'abcd1234', 'defg5678'
        )

        message_error = self.browser.find_element(
            By.CLASS_NAME, 'alert-error'
        ).text
        self.assertEqual(message_error, 'Form inválid.')

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
        self.send_input_keys(
            'testing', 'testing@example.com',
            'testing12!@1dsFG', 'testing12!@1dsFG'
        )

        message_success = self.browser.find_element(
            By.CLASS_NAME, 'alert-success'
        ).text
        self.assertEqual(message_success, 'Account created!')

        self.fail('finish the test!')

        # It worked and was redirected already logged in to the homepage.
        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'test'
        )))
        self.assertEqual(self.browser.title, 'Document')

        username = self.browser.find_element(
            By.CLASS_NAME, 'username-profile'
        ).text

        self.assertEqual(username, 'testing')

    def test_logged_user_cannot_access_registration_page(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # He registers himself
        self.send_input_keys(
            'testing', 'testing@example.com',
            'testing12!@1dsFG', 'testing12!@1dsFG'
        )

        # He tries to go back to the registration page.
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # He noticed that he can no longer enter there and
        # received an error notifying him.
        error_message = self.browser.find_element(
            By.CLASS_NAME, 'alert-error'
        ).text

        self.assertEqual(
            error_message, 'You cannot access this while logged in.'
        )

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # His browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # He notices the Submit button color
        submit_button = self.browser.find_element(
            By.XPATH, '//button[text()="Submit"]'
        )
        self.assertEqual(
            submit_button.value_of_css_property('background-color'),
            'rgba(38, 198, 218, 1)'
        )
