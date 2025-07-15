from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests


class TestLoginAuthorFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

        self.form_data = {
            'username': 'testing',
            'password': 'testing12!@1dsFG',
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
            'password': 'Ex 23#$1fsgKDL!',
        }

        for name, placeholder in inputs_information:
            input = correct_inputs[name]

            if placeholder == input:
                pass
            else:
                self.fail((placeholder, input))

    def send_input_keys(self, username, password):
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))

        username_field = form.find_element(By.ID, 'id_username')
        password_field = form.find_element(By.ID, 'id_password')

        username_field.clear()
        password_field.clear()

        username_field.send_keys(username)
        password_field.send_keys(password)

        form.submit()

        return form

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.browser.get(self.live_server_url)

        # He sees the Login button and presses it.
        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'login-button'
        ))).click()

        # See the login page
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))
        self.assertEqual(self.browser.title, 'Login')

        # Check that all inputs have placeholders.
        inputs = form.find_elements(By.CLASS_NAME, 'form-control')
        inputs_information = self.get_all_placeholders(inputs)
        self.validate_placeholders(inputs_information)

    def test_login_invalid_fields_and_success_redirect(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:login'))

        self.assertEqual(self.browser.title, 'Login')

        # See the form and decide to fill it out and send
        # the form and notice errors on your screen
        self.send_input_keys('abcd', 'abcd1234')

        error_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-error'
        ))).text

        self.assertEqual(error_message, 'Form invalid.')

        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))

        errors = self.browser.find_elements(By.CLASS_NAME, 'errorlist')

        errors_messages = [error.text for error in errors]

        self.fail(errors_messages)

        # Decided to fix the gaps that caused errors and resend it again.
        self.send_input_keys('testing', 'testing12!@1dsFG')

        message_success = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-success'
        ))).text

        self.assertEqual(message_success, 'Account logged!')

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
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # He login himself
        self.send_input_keys('testing', 'testing12!@1dsFG',)

        # He tries to go back to the login page.
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # He noticed that he can no longer enter there and
        # received an error notifying him.
        error_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-error'
        ))).text

        self.assertEqual(
            error_message, 'You cannot access this while logged in.'
        )

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:login'))

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


class TestCreateAuthorPtBRFT(BaseWebDriverForFunctionalTests):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_user_can_see_portuguese_translation(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # And he found the form in portuguese
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))

        username = form.find_element(
            By.XPATH, '//label[@for="id_username"]'
        ).text

        password = form.find_element(
            By.XPATH, '//label[@for="id_password"]'
        ).text

        password_input = form.find_element(By.ID, 'id_password')

        password_placeholder = password_input.get_attribute('placeholder')

        self.assertEqual(username, 'Nome de usuário:')
        self.assertEqual(password, 'Senha:')
        self.assertEqual(password_placeholder, 'Repita sua senha')
        self.assertEqual(self.browser.title, 'Registrar-se')
