from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import authors.constants as const
from functional_tests.base import BaseWebDriverForFunctionalTests


class GetErrorsMixin:
    def get_errors(self):
        error_messages = self.wait_for_element(
            By.CLASS_NAME, 'error-span', all_element=True
        )

        return [error_message.text for error_message in error_messages]


class CreateAuthorJSTest(BaseWebDriverForFunctionalTests, GetErrorsMixin):
    def setUp(self):
        super().setUp()

        self.wait = self.delay()

        self.create_valid_user()

    def test_username_already_registred(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'testing'
        self.fill_credentials(id_username='testing')

        error_messages = self.get_errors()

        self.assertIn(const.USERNAME_TAKEN_ALREADY_ERROR, error_messages)

    def test_username_not_already_registred(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'abc'
        self.fill_credentials(id_username='abc')

        error_messages = self.get_errors()

        self.assertNotIn(const.USERNAME_TAKEN_ALREADY_ERROR, error_messages)


class CreateAuthorMessagesJSTest(
    BaseWebDriverForFunctionalTests, GetErrorsMixin
):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_username_length_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'ab'
        self.fill_credentials(id_username='ab')

        error_messages = self.get_errors()

        self.assertIn(
            'Por favor, insira pelo menos 4 caracteres '
            '(você está usando atualmente 2 caracteres).',
            error_messages
        )

    def test_username_already_registred_error_message_portuguese(self):
        self.create_valid_user()

        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'testing'
        self.fill_credentials(id_username='testing')

        error_messages = self.get_errors()

        self.assertIn('Este nome de usuário já está em uso.', error_messages)

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
