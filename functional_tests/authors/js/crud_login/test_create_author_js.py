from selenium.webdriver.common.by import By

from functional_tests.base import BaseWebDriverForFunctionalTests


class CreateAuthorMessagesTest(BaseWebDriverForFunctionalTests):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_username_length_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'a'
        self.fill_credentials(id_username='a')

        # get errors
        error_messages = self.wait_for_element(
            By.CLASS_NAME, 'error-span', all_element=True
        )

        messages = [error_message.text for error_message in error_messages]

        self.assertIn(
            'Por favor, insira pelo menos 4 caracteres.', messages
        )

    def test_password_length_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'a'
        self.fill_credentials(id_password1='a1!')

        # get errors
        error_messages = self.wait_for_element(
            By.CLASS_NAME, 'error-span', all_element=True
        )

        messages = [error_message.text for error_message in error_messages]

        self.assertIn(
            'Por favor, aumente este texto para 8 caracteres ou mais '
            '(você está usando atualmente 3 caracteres).', messages
        )

    def test_password_symbols_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'a'
        self.fill_credentials(id_password1='abcd1234')

        # get errors
        error_messages = self.wait_for_element(
            By.CLASS_NAME, 'error-span', all_element=True
        )

        messages = [error_message.text for error_message in error_messages]

        self.assertIn('A senha deve conter símbolos.', messages)

    def test_password_numbers_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'a'
        self.fill_credentials(id_password1='abcd!@#$')

        # get errors
        error_messages = self.wait_for_element(
            By.CLASS_NAME, 'error-span', all_element=True
        )

        messages = [error_message.text for error_message in error_messages]

        self.assertIn('A senha deve conter números.', messages)
