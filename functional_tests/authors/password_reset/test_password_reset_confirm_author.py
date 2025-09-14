from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from selenium.webdriver.common.by import By

import authors.constants as const
from functional_tests.base import BaseWebDriverForFunctionalTests

User = get_user_model()


class TestPasswordResetConfirmAuthorFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

        self.user = self.create_valid_user()

        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('authors:password_reset_confirm', kwargs={
            'uidb64': self.uidb64,
            'token': self.token
        })

    def test_user_can_see_all_the_placeholders(self):
        # User enters the password reset confirm screen
        self.browser.get(self.live_server_url + self.url)

        # See the registration screen
        form = self.wait_for_element(By.CLASS_NAME, 'author-form')
        self.assertEqual(self.browser.title, 'Enter new password')

        # Check that all inputs have placeholders.
        new_password1_input = form.find_element(
            By.ID, 'id_new_password1'
        )

        new_password2_input = form.find_element(
            By.ID, 'id_new_password2'
        )

        new_password1_placeholder = new_password1_input.get_attribute(
            'placeholder'
        )
        new_password2_placeholder = new_password2_input.get_attribute(
            'placeholder'
        )

        correct_inputs = {
            'new_password1': const.NEW_PASSWORD1_PLACEHOLDER,
            'new_password2': const.NEW_PASSWORD2_PLACEHOLDER
        }

        self.assertEqual(
            new_password1_placeholder, correct_inputs['new_password1']
        )
        self.assertEqual(
            new_password2_placeholder, correct_inputs['new_password2']
        )

    def test_registration_invalid_fields_and_success_redirect(self):
        # User enters the password reset confirm screen
        self.browser.get(self.live_server_url + self.url)

        # See the form and decide to fill it out and send
        # the form and notice errors on your screen
        self.fill_credentials(
            id_new_password1='abcd', id_new_password2='efgh', submit=True
        )

        error_message = self.get_text(By.CLASS_NAME, 'errorlist')

        self.assertEqual(
            error_message, "The two password fields didn’t match."  # TODO fix error message
        )

        self.fill_credentials(
            id_new_password1='abcd', id_new_password2='abcd', submit=True
        )

        errors = self.wait_for_element(
            By.CLASS_NAME, 'errorlist', all_element=True
        )

        errors_messages = [error.text for error in errors]

        self.assertIn(
            'This password is too short. It must contain at least '
            '8 characters.',
            errors_messages[0]
        )

        self.assertIn(
            'This password is too common.',
            errors_messages[0]
        )

        # Decided to fix the gaps that caused errors and resend it again.
        self.fill_credentials(
            id_new_password1='testing12!@1dsFG',
            id_new_password2='testing12!@1dsFG',
            submit=True
        )

        message_success = self.get_text(By.CLASS_NAME, 'alert-success')

        self.assertEqual(message_success, 'Password changed successfully!')

        # It worked and was redirected already logged in to the homepage.
        self.wait_for_element(By.CLASS_NAME, 'test')
        self.assertEqual(self.browser.title, 'Document')

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + self.url)

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

        self.user = self.create_valid_user()

        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = default_token_generator.make_token(self.user)
        self.url = reverse('authors:password_reset_confirm', kwargs={
            'uidb64': self.uidb64,
            'token': self.token
        })

    def test_user_can_see_portuguese_translation(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + self.url)

        # And he found the form in portuguese
        new_password1 = self.get_text(
            By.XPATH, '//label[@for="id_new_password1"]',
            wait_for_element=False
        )

        new_password2 = self.get_text(
            By.XPATH, '//label[@for="id_new_password2"]',
            wait_for_element=False
        )

        password1_input = self.find_element(By.ID, 'id_new_password1')
        password2_input = self.find_element(By.ID, 'id_new_password2')

        password1_placeholder = password1_input.get_attribute('placeholder')
        password2_placeholder = password2_input.get_attribute('placeholder')

        self.assertEqual(new_password1, 'Nova senha:')
        self.assertEqual(new_password2, 'Confirmação da nova senha:')
        self.assertEqual(password1_placeholder, 'Escreva sua nova senha.')
        self.assertEqual(password2_placeholder, 'Confirme sua nova senha.')
        self.assertEqual(self.browser.title, 'Digite a nova senha')
