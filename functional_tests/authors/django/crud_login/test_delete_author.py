from selenium.webdriver.common.by import By

import authors.constants as const
from functional_tests.base import BaseWebDriverForFunctionalTests


class TestDeleteAuthorFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

        # User login in your account
        self.go_to_url()

        self.create_valid_user(auto_login=True)

    def test_user_can_see_all_the_placeholders(self):
        # User enters the delete screen
        self.go_to_url('authors:delete')

        # See the delete page
        form = self.wait_for_element(By.CLASS_NAME, 'author-form')

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
        self.go_to_url('authors:delete')

        # See the form and decide to fill it out and send
        # the form and notice errors on your screen
        self.fill_credentials(id_confirm='false', submit=True)

        error_message = self.get_text(By.CLASS_NAME, 'errorlist')

        self.assertEqual(error_message, const.DELETE_ACCOUNT_ERROR)

        # Decided to fix the gaps that caused errors and resend it again.
        self.fill_credentials(id_confirm='DELETE', submit=True)

        message_success = self.get_text(By.CLASS_NAME, 'alert-success')

        self.assertEqual(
            message_success, const.ACCOUNT_DELETED_SUCCESS
        )

        # It worked and was redirected already logged in to the homepage.
        self.wait_for_element(By.CLASS_NAME, 'test')
        self.assertEqual(self.browser.title, 'Document')

    def test_not_logged_user_cannot_access_login_page(self):
        self.logout_user()

        # User enters the delete screen
        self.go_to_url('authors:delete')

        # He noticed that he can no longer enter there and
        # received an error notifying him.
        error_message = self.get_text(By.CLASS_NAME, 'alert-error')

        self.assertEqual(
            error_message, const.CANNOT_ACCESS_NOT_LOGGED_ERROR
        )

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.go_to_url('authors:delete')

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

        # User login in your account
        self.go_to_url()

        self.create_valid_user(auto_login=True)

    def test_user_can_see_portuguese_translation(self):
        # User enters the delete screen
        self.go_to_url('authors:delete')

        # And he found the form in portuguese
        confirm = self.get_text(
            By.XPATH, '//label[@for="id_confirm"]',
            wait_for_element=False
        )

        confirm_input = self.find_element(By.ID, 'id_confirm')

        confirm_placeholder = confirm_input.get_attribute('placeholder')

        self.assertEqual(confirm, 'Confirmação de exclusão da conta:')
        self.assertEqual(
            confirm_placeholder,
            'Digite "DELETE" para deletar sua conta permanentemente.'
        )
        self.assertEqual(self.browser.title, 'Exclua sua conta')
