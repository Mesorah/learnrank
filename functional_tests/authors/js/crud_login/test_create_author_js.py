from selenium.webdriver.common.by import By

import authors.constants as const
import utils.constants_informations as const_informations
from functional_tests.base import BaseWebDriverForFunctionalTests


class GetErrorsMixin:
    def get_errors(self, input_id):
        input_el = self.find_element(By.ID, input_id)
        parent = input_el.find_element(By.XPATH, "..")

        error_messages = parent.find_elements(By.CLASS_NAME, 'error-span')

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
        self.fill_credentials(id_username=const_informations.TEST_USERNAME)

        error_messages = self.get_errors('id_username')

        self.assertIn(const.USERNAME_ALREADY_TAKEN_ERROR, error_messages)

    def test_username_not_already_registred(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'abc'
        self.fill_credentials(id_username='abc')

        error_messages = self.get_errors('id_username')

        self.assertNotIn(const.USERNAME_ALREADY_TAKEN_ERROR, error_messages)

    def test_email_already_registred(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'testing@example.com'
        self.fill_credentials(id_email=const_informations.TEST_EMAIL)

        error_messages = self.get_errors('id_email')

        self.assertIn(const.EMAIL_ALREADY_REGISTERED_ERROR, error_messages)

    def test_email_not_already_registred(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'testing2@example.com'
        self.fill_credentials(id_email='testing2@example.com')

        # uses a fail username for error_messages get a error
        self.fill_credentials(id_username='abc')

        error_messages = self.get_errors('id_email')

        self.assertNotIn(const.EMAIL_ALREADY_REGISTERED_ERROR, error_messages)


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

        # filled in the field with 'abc'
        self.fill_credentials(id_username='abc')

        error_messages = self.get_errors('id_username')

        self.assertIn(
            'Por favor, insira pelo menos 4 caracteres '
            '(você está usando atualmente 3 caracteres).',
            error_messages
        )

    def test_username_already_registred_error_message_portuguese(self):
        self.create_valid_user(username=const_informations.TEST_USERNAME)

        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'testing'
        self.fill_credentials(id_username=const_informations.TEST_USERNAME)

        error_messages = self.get_errors('id_username')

        self.assertIn('Este nome de usuário já está em uso.', error_messages)

    def test_password_length_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'a1!'
        self.fill_credentials(id_password1='a1!')

        error_messages = self.get_errors('id_password1')

        self.assertIn(
            'Por favor, aumente este texto para 8 caracteres ou mais '
            '(você está usando atualmente 3 caracteres).', error_messages
        )

    def test_password_letters_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        self.fill_credentials(id_password1='!@#$1234')

        error_messages = self.get_errors('id_password1')

        self.assertIn('A senha deve conter letras.', error_messages)

    def test_password_symbols_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'abcd1234'
        self.fill_credentials(id_password1='abcd1234')

        error_messages = self.get_errors('id_password1')

        self.assertIn('A senha deve conter símbolos.', error_messages)

    def test_password_numbers_error_message_portuguese_translation(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'abcd!@#$'
        self.fill_credentials(id_password1='abcd!@#$')

        error_messages = self.get_errors('id_password1')

        self.assertIn('A senha deve conter números.', error_messages)

    def test_password_is_equal_error_message_portuguese_translations(self):
        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled the fields
        self.fill_credentials(id_password1='abcd12!@#$')
        self.fill_credentials(id_password2='adbc')

        error_messages = self.get_errors('id_password1')

        self.assertIn('As senhas não coincidem.', error_messages)

    def test_email_already_registred_error_message_portuguese_translate(self):
        # Create a new account for test duplicated email
        self.create_valid_user()

        # Enter to signup page
        self.go_to_url('authors:signup')

        # filled in the field with 'testing@example.com'
        self.fill_credentials(id_email=const_informations.TEST_EMAIL)

        error_messages = self.get_errors('id_email')

        self.assertIn('Este e-mail já está registrado.', error_messages)
