from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests


class TestPasswordResetAuthorFT(BaseWebDriverForFunctionalTests):
    language_header = 'en-US,en'
    locale = 'en'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_messages_are_correct(self):
        # User enters the reset password done page
        self.browser.get(
            self.live_server_url + reverse('authors:password_reset_done')
        )

        # He found the container in portuguese
        container = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-password-container'
        )))

        h1 = container.find_element(By.TAG_NAME, 'h1').text
        p = container.find_element(By.TAG_NAME, 'p').text

        self.assertEqual(self.browser.title, 'Password reset sent')
        self.assertEqual(h1, 'Check your email')
        self.assertEqual(
            p,
            'If an account exists with the provided email address, '
            'you will receive a message with instructions to reset '
            'your password.'
        )

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the reset password done page
        self.browser.get(
            self.live_server_url + reverse('authors:password_reset_done')
        )

        # He notices the Submit button color
        text = self.browser.find_element(
            By.TAG_NAME, 'p'
        )
        self.assertEqual(
            text.value_of_css_property('color'),
            'rgba(75, 85, 99, 1)'
        )


class TestCreateAuthorPtBRFT(BaseWebDriverForFunctionalTests):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_user_can_see_portuguese_translation(self):
        # User enters the reset password done page
        self.browser.get(
            self.live_server_url + reverse('authors:password_reset_done')
        )

        # He found the container in portuguese
        container = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-password-container'
        )))

        h1 = container.find_element(By.TAG_NAME, 'h1').text
        p = container.find_element(By.TAG_NAME, 'p').text

        self.assertEqual(self.browser.title, 'Redefinição de senha enviada')
        self.assertEqual(h1, 'Verifique seu e-mail')
        self.assertEqual(
            p,
            'Se existir uma conta associada ao endereço de '
            'e-mail fornecido, você receberá uma mensagem com instruções para '
            'redefinir sua senha.'
        )
