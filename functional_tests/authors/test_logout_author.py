from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests


class TestLogoutAuthorFT(BaseWebDriverForFunctionalTests):
    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_logged_in_user_logout_flow(self):
        # User accessed the site
        self.browser.get(self.live_server_url)

        # User logged into the site
        self.login_user()

        # He tried to access the signup page.
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # He saw that he couldn't enter there while logged in.
        error_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-error'
        ))).text

        self.assertEqual(
            error_message, 'You cannot access this while logged in.'
        )

        # So he decided to log out there to be able to access the page.
        self.browser.find_element(
            By.CLASS_NAME, 'author-logout-button'
        ).click()

        # He saw the success message
        success_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-success'
        ))).text

        self.assertEqual(success_message, 'Success, you have logged out!')

        # And managed to enter the sign-up page
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        self.assertEqual(self.browser.title, 'Sign Up')


class TestLogoutAuthorPtBRFT(BaseWebDriverForFunctionalTests):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_user_can_see_portuguese_translation(self):
        # User accessed the site
        self.browser.get(self.live_server_url)

        # User logged into the site
        self.login_user()

        # And he found the sucess message in portuguese
        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-logout-button'
        ))).click()

        success_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-success'
        ))).text

        self.assertEqual(success_message, 'Você saiu da conta com sucesso!')
