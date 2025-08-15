from selenium.webdriver.common.by import By

import authors.constants as const
from authors.forms import CustomSignupForm
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

        form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

        form = CustomSignupForm(data=form_data)
        form.save()

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
            'username': const.SIGNUP_USERNAME_PLACEHOLDER,
            'password': const.SIGNUP_PASSWORD1_PLACEHOLDER,
        }

        for name, placeholder in inputs_information:
            input = correct_inputs[name]

            if placeholder == input:
                pass
            else:
                self.fail((placeholder, input))

    def send_input_keys(self, username, password):
        form = self.wait_for_element(By.CLASS_NAME, 'author-form')

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
        self.go_to_url()

        # He sees the Login button and presses it.
        self.click_when_visible(By.CLASS_NAME, 'login-button')

        # See the login page
        form = self.wait_for_element(By.CLASS_NAME, 'author-form')
        self.assertEqual(self.browser.title, const.TITLE_LOGIN)

        # Check that all inputs have placeholders.
        inputs = form.find_elements(By.CLASS_NAME, 'form-control')
        inputs_information = self.get_all_placeholders(inputs)
        self.validate_placeholders(inputs_information)

    def test_login_invalid_fields_and_success_redirect(self):
        # User enters the home screen
        self.go_to_url('authors:login')

        self.assertEqual(self.browser.title, const.TITLE_LOGIN)

        # See the form and decide to fill it out and send
        # the form and notice errors on your screen
        self.send_input_keys('abcd', 'abcd1234')

        error_message = self.get_text(By.CLASS_NAME, 'errorlist')

        self.assertEqual(error_message, (
            'Please enter a correct username and password. '
            'Note that both fields may be case-sensitive.'
        ))

        self.wait_for_element(By.CLASS_NAME, 'author-form')

        # Decided to fix the gaps that caused errors and resend it again.
        self.send_input_keys('testing', 'testing12!@1dsFG')

        message_success = self.get_text(By.CLASS_NAME, 'alert-success')

        self.assertEqual(message_success, const.ACCOUNT_LOGGED_SUCCESS)

        # It worked and was redirected already logged in to the homepage.
        self.wait_for_element(By.CLASS_NAME, 'test')
        self.assertEqual(self.browser.title, 'Document')

        username = self.get_text(
            By.CLASS_NAME, 'username-profile', wait_for_element=False
        )

        self.assertEqual(username, 'testing')

    def test_logged_user_cannot_access_login_page(self):
        # User enters the home screen
        self.go_to_url('authors:login')

        # He login himself
        self.send_input_keys('testing', 'testing12!@1dsFG',)

        # He tries to go back to the login page.
        self.go_to_url('authors:login')

        # He noticed that he can no longer enter there and
        # received an error notifying him.
        error_message = self.get_text(By.CLASS_NAME, 'alert-error')

        self.assertEqual(
            error_message, const.CANNOT_ACCESS_LOGGED_ERROR
        )

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.go_to_url('authors:login')

        # His browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # He notices the Submit button color
        submit_button = self.find_element(
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
        self.go_to_url('authors:login')

        # And he found the form in portuguese
        username = self.get_text(
            By.XPATH, '//label[@for="id_username"]', wait_for_element=False
        )

        username_input = self.find_element(By.ID, 'id_username')

        username_placeholder = username_input.get_attribute('placeholder')

        password = self.get_text(
            By.XPATH, '//label[@for="id_password"]', wait_for_element=False
        )

        password_input = self.find_element(By.ID, 'id_password')

        password_placeholder = password_input.get_attribute('placeholder')

        self.assertEqual(username, 'Usuário:')
        self.assertEqual(password, 'Senha:')
        self.assertEqual(
            username_placeholder, 'Escreva seu nome de usuário aqui.'
        )
        self.assertEqual(password_placeholder, 'Escreva sua senha aqui.')
        self.assertEqual(self.browser.title, 'Entrar')
