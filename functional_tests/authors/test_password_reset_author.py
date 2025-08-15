from selenium.webdriver.common.by import By

import authors.constants as const
from functional_tests.base import BaseWebDriverForFunctionalTests


class TestPasswordResetAuthorFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.go_to_url()

        self.login_user()

        self.go_to_url('authors:password_reset')

        # See the password reset page
        form = self.wait_for_element(By.CLASS_NAME, 'author-form')
        self.assertEqual(self.browser.title, 'Password reset')

        # Check that all inputs have placeholders.
        input = form.find_element(By.ID, 'id_email')

        placeholder = input.get_attribute('placeholder')
        name = input.get_attribute('name')

        correct_input = {'email': const.EMAIL_PLACEHOLDER}

        if placeholder == correct_input[name]:
            pass
        else:
            self.fail((placeholder, correct_input[name]))

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.go_to_url()

        self.login_user()

        # User enters the password reset page
        self.go_to_url('authors:password_reset')

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
        # So he logged into his account.
        self.go_to_url()
        self.login_user()

        # And decided to change his password
        self.go_to_url('authors:password_reset')

        # He found the form in portuguese
        form = self.wait_for_element(By.CLASS_NAME, 'author-form')

        email_input = form.find_element(By.ID, 'id_email')

        email_placeholder = email_input.get_attribute('placeholder')

        self.assertEqual(email_placeholder, 'Escreva seu e-mail aqui.')
        self.assertEqual(self.browser.title, 'Recuperar senha')
