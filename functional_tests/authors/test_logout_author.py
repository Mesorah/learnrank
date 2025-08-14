from selenium.webdriver.common.by import By

import authors.constants as const
from functional_tests.base import BaseWebDriverForFunctionalTests


class TestLogoutAuthorFT(BaseWebDriverForFunctionalTests):
    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_logged_in_user_logout_flow(self):
        # User accessed the site
        self.go_to_url('authors:signup')

        # User logged into the site
        self.login_user()

        # He tried to access the signup page.
        self.go_to_url('authors:signup')

        # He saw that he couldn't enter there while logged in.
        error_message = self.wait_until_element(
            By.CLASS_NAME, 'alert-error'
        ).text

        self.assertEqual(
            error_message, const.CANNOT_ACCESS_LOGGED_ERROR
        )

        # So he decided to log out there to be able to access the page.
        self.browser.find_element(
            By.CLASS_NAME, 'author-logout-button'
        ).click()

        # He saw the success message
        success_message = self.wait_until_element(
            By.CLASS_NAME, 'alert-success'
        ).text

        self.assertEqual(success_message, const.ACCOUNT_LOGOUT_SUCCESS)

        # And managed to enter the sign-up page
        self.go_to_url('authors:signup')

        self.assertEqual(self.browser.title, const.TITLE_SIGN_UP)


class TestLogoutAuthorPtBRFT(BaseWebDriverForFunctionalTests):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_user_can_see_portuguese_translation(self):
        # User accessed the site
        self.go_to_url()

        # User logged into the site
        self.login_user()

        # And he found the sucess message in portuguese
        self.wait_until_element(
            By.CLASS_NAME, 'author-logout-button'
        ).click()

        success_message = self.wait_until_element(
            By.CLASS_NAME, 'alert-success'
        ).text

        self.assertEqual(success_message, 'Você saiu da conta com sucesso!')
