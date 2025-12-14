from selenium.webdriver.common.by import By

import authors.constants as const
import utils.constants_informations as const_informations
from functional_tests.base import BaseWebDriverForFunctionalTests


class TestCreateAuthorFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def validate_placeholders(self, inputs_information):
        correct_inputs = {
            'username': const.SIGNUP_USERNAME_PLACEHOLDER,
            'email': const.SIGNUP_EMAIL_PLACEHOLDER,
            'password1': const.SIGNUP_PASSWORD1_PLACEHOLDER,
            'password2': const.SIGNUP_PASSWORD2_PLACEHOLDER
        }

        for name, placeholder in inputs_information:
            correct_input = correct_inputs[name]

            if placeholder != correct_input:
                self.fail((placeholder, correct_input))

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.go_to_url()

        # He sees the Login button and presses it.
        self.click_when_visible(By.CLASS_NAME, 'login-button')

        # He realizes that he doesn't have an account
        # and clicks the Sign up link.
        self.click_when_visible(By.CLASS_NAME, 'sign-up-link')

        self.assertEqual(self.browser.title, const.TITLE_SIGN_UP)

        # Check that all inputs have placeholders.
        inputs_information = self.get_all_placeholders()

        self.validate_placeholders(inputs_information)

    def test_registration_invalid_fields_and_success_redirect(self):
        # User enters the home screen
        self.go_to_url('authors:signup')

        self.assertEqual(self.browser.title, const.TITLE_SIGN_UP)

        # See the form and decide to fill it out and send
        # the form and notice errors on your screen
        self.fill_credentials(
            id_username='abcd', id_email=const_informations.TEST_EMAIL,
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
            id_username=const_informations.TEST_USERNAME,
            id_email=const_informations.TEST_EMAIL,
            id_password1=const_informations.TEST_PASSWORD,
            id_password2=const_informations.TEST_PASSWORD,
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

        self.assertEqual(username, const_informations.TEST_USERNAME)

    def test_logged_user_cannot_access_registration_page(self):
        # User enters the home screen
        self.go_to_url('authors:signup')

        self.fill_credentials(
            id_username=const_informations.TEST_USERNAME,
            id_email=const_informations.TEST_EMAIL,
            id_password1=const_informations.TEST_PASSWORD,
            id_password2=const_informations.TEST_PASSWORD,
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
