from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import authors.constants as const
from authors.forms import CustomSignupForm
from functional_tests.base import BaseWebDriverForFunctionalTests


class TestDeleteAuthorFT(BaseWebDriverForFunctionalTests):
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

        # User login in your account
        self.browser.get(self.live_server_url)

        self.login_user()

    def test_user_can_see_all_the_placeholders(self):
        # User enters the delete screen
        self.browser.get(self.live_server_url + reverse('authors:delete'))

        # See the delete page
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))
        self.assertEqual(self.browser.title, const.TITLE_DELETE_ACCOUNT)

        # Check that all inputs have placeholders.
        confirm_input = form.find_element(
            By.ID, 'id_confirm'
        )

        confirm_placeholder = confirm_input.get_attribute(
            'placeholder'
        )

        self.assertEqual(
            confirm_placeholder,
            const.DELETE_ACCOUNT_PLACEHOLDER
        )

    def test_form_invalid_fields_and_success_redirect(self):
        # User enters the delete screen
        self.browser.get(self.live_server_url + reverse('authors:delete'))

        # See the form and decide to fill it out and send
        # the form and notice errors on your screen
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))

        confirm_field = form.find_element(By.ID, 'id_confirm')
        confirm_field.send_keys('false')
        form.submit()

        error_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'errorlist'
        ))).text

        self.assertEqual(error_message, const.DELETE_ACCOUNT_ERROR)

        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))

        # Decided to fix the gaps that caused errors and resend it again.
        confirm_field = form.find_element(By.ID, 'id_confirm')
        confirm_field.clear()
        confirm_field.send_keys('DELETE')
        form.submit()

        message_success = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-success'
        ))).text

        self.assertEqual(
            message_success, const.ACCOUNT_DELETED_SUCCESS
        )

        # It worked and was redirected already logged in to the homepage.
        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'test'
        )))
        self.assertEqual(self.browser.title, 'Document')

    def test_not_logged_user_cannot_access_login_page(self):
        self.logout_user()

        # User enters the delete screen
        self.browser.get(self.live_server_url + reverse('authors:delete'))

        # He noticed that he can no longer enter there and
        # received an error notifying him.
        error_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-error'
        ))).text

        self.assertEqual(
            error_message, const.CANNOT_ACCESS_NOT_LOGGED_ERROR
        )

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:delete'))

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

        # User login in your account
        self.browser.get(self.live_server_url)

        self.login_user()

    def test_user_can_see_portuguese_translation(self):
        # User enters the delete screen
        self.browser.get(self.live_server_url + reverse('authors:delete'))

        # And he found the form in portuguese
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))

        confirm = form.find_element(
            By.XPATH, '//label[@for="id_confirm"]'
        ).text

        confirm_input = form.find_element(By.ID, 'id_confirm')

        confirm_placeholder = confirm_input.get_attribute('placeholder')

        self.assertEqual(confirm, 'Confirmação de exclusão da conta:')
        self.assertEqual(
            confirm_placeholder,
            'Digite "DELETE" para deletar sua conta permanentemente.'
        )
        self.assertEqual(self.browser.title, 'Exclua sua conta')
