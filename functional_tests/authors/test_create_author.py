from selenium.webdriver.common.by import By

import authors.constants as const
from functional_tests.base import BaseWebDriverForFunctionalTests


class TestCreateAuthorFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

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
            'username': const.SIGNUP_USERNAME_PLACEHOLDER,
            'email': const.SIGNUP_EMAIL_PLACEHOLDER,
            'password1': const.SIGNUP_PASSWORD1_PLACEHOLDER,
            'password2': const.SIGNUP_PASSWORD2_PLACEHOLDER
        }

        for name, placeholder in inputs_information:
            input = correct_inputs[name]

            if placeholder == input:
                pass
            else:
                self.fail((placeholder, input))

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.go_to_url()

        # He sees the Login button and presses it.
        self.click_when_visible(By.CLASS_NAME, 'login-button')

        # He realizes that he doesn't have an account
        # and clicks the Sign up link.
        self.click_when_visible(By.CLASS_NAME, 'sign-up-link')

        # See the registration screen
        form = self.wait_for_element(By.CLASS_NAME, 'author-form')

        self.assertEqual(self.browser.title, const.TITLE_SIGN_UP)

        # Check that all inputs have placeholders.
        inputs = form.find_elements(By.CLASS_NAME, 'form-control')
        inputs_information = self.get_all_placeholders(inputs)
        self.validate_placeholders(inputs_information)

    def test_registration_invalid_fields_and_success_redirect(self):
        # User enters the home screen
        self.go_to_url('authors:signup')

        self.assertEqual(self.browser.title, const.TITLE_SIGN_UP)

        # See the form and decide to fill it out and send
        # the form and notice errors on your screen
        self.fill_credentials(
            id_username='abcd', id_email='testing@example.com',
            id_password1='abcd1234', id_password2='defg5678',
            submit=True,
        )

        self.browser.set_window_size(1200, 800)

        error_message = self.get_text(By.CLASS_NAME, 'alert')

        self.assertEqual(error_message, const.FORM_INVALID_ERROR)

        self.wait_for_element(By.CLASS_NAME, 'author-form')

        errors = self.find_element(
            By.CLASS_NAME, 'errorlist', all_element=True
        )

        errors_messages = [error.text for error in errors]

        self.assertIn(
            const.PASSWORD_MUST_CONTAIN_SYMBOLS_ERROR,
            errors_messages
        )

        self.assertIn(
            const.PASSWORDS_DO_NOT_MATCH_ERROR,
            errors_messages
        )

        # Decided to fix the gaps that caused errors and resend it again.
        self.fill_credentials(
            id_username='testing', id_email='testing@example.com',
            id_password1='testing12!@1dsFG', id_password2='testing12!@1dsFG',
            submit=True,
        )

        message_success = self.get_text(By.CLASS_NAME, 'alert-success')

        self.assertEqual(message_success, const.ACCOUNT_CREATED_SUCCESS)

        # It worked and was redirected already logged in to the homepage.
        self.wait_for_element(By.CLASS_NAME, 'test')

        self.assertEqual(self.browser.title, 'Document')

        username = self.get_text(
            By.CLASS_NAME, 'username-profile'
        )

        self.assertEqual(username, 'testing')

    def test_logged_user_cannot_access_registration_page(self):
        # User enters the home screen
        self.go_to_url('authors:signup')

        self.fill_credentials(
            id_username='testing', id_email='testing@example.com',
            id_password1='testing12!@1dsFG', id_password2='testing12!@1dsFG',
            submit=True,
        )

        # He tries to go back to the registration page.
        self.go_to_url('authors:signup')

        # He noticed that he can no longer enter there and
        # received an error notifying him.
        error_message = self.get_text(By.CLASS_NAME, 'alert-error')

        self.assertEqual(
            error_message, const.CANNOT_ACCESS_LOGGED_ERROR
        )

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.go_to_url('authors:signup')

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
        self.go_to_url('authors:signup')

        # And he found the form in portuguese
        self.wait_for_element(By.CLASS_NAME, 'author-form')

        username = self.get_text(
            By.XPATH, '//label[@for="id_username"]',
            wait_for_element=False
        )

        password1 = self.get_text(
            By.XPATH, '//label[@for="id_password1"]',
            wait_for_element=False
        )

        password2 = self.get_text(
            By.XPATH, '//label[@for="id_password2"]',
            wait_for_element=False
        )

        password2_input = self.find_element(By.ID, 'id_password2')

        password2_placeholder = password2_input.get_attribute('placeholder')

        self.assertEqual(username, 'Nome de usuário:')
        self.assertEqual(password1, 'Senha:')
        self.assertEqual(password2, 'Repita a senha:')
        self.assertEqual(password2_placeholder, 'Repita sua senha')
        self.assertEqual(self.browser.title, 'Criar conta')
