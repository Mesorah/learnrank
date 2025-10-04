from selenium.webdriver.common.by import By

from functional_tests.base import BaseWebDriverForFunctionalTests


class CreateAuthorMessagesTest(BaseWebDriverForFunctionalTests):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def get_errors(self):
        error_messages = self.wait_for_element(
            By.CLASS_NAME, 'error-span', all_element=True
        )

        return [error_message.text for error_message in error_messages]

    def test_username_length_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'a'
        self.fill_credentials(id_username='a')

        error_messages = self.get_errors()

        self.assertIn(
            'Por favor, insira pelo menos 4 caracteres.', error_messages
        )

    def test_password_length_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'a1!'
        self.fill_credentials(id_password1='a1!')

        error_messages = self.get_errors()

        self.assertIn(
            'Por favor, aumente este texto para 8 caracteres ou mais '
            '(você está usando atualmente 3 caracteres).', error_messages
        )

    def test_password_symbols_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'abcd1234'
        self.fill_credentials(id_password1='abcd1234')

        error_messages = self.get_errors()

        self.assertIn('A senha deve conter símbolos.', error_messages)

    def test_password_numbers_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'abcd!@#$'
        self.fill_credentials(id_password1='abcd!@#$')

        error_messages = self.get_errors()

        self.assertIn('A senha deve conter números.', error_messages)

    def test_password_is_equal_error_message_portuguese_translations(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled the fields
        self.fill_credentials(id_password1='abcd12!@#$')
        self.fill_credentials(id_password2='adbc')

        error_messages = self.get_errors()

        self.assertIn('As senhas não coincidem.', error_messages)
