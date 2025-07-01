from django.urls import reverse
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests


class TestAuthorCreate(BaseWebDriverForFunctionalTests):
    def setUp(self):
        super().setUp()
        self.wait = self.delay()

    def get_all_placeholders(self, inputs):
        inputs_information = []

        for input in inputs:
            placeholder = input.get_attribute('placeholder')
            name = input.get_attribute('name')
            inputs_information.append((name, placeholder))

        return inputs_information

    def validate_placeholders(self, inputs_information):
        correct_inputs = {
            'username': 'Ex: Gabriel Rodrigues',
            'email': 'Ex: gabrielrodrigues@example.com',
            'password1': 'Ex 23#$1fsgKDL!',
            'password2': 'Repeat your password'
        }

        for name, placeholder in inputs_information:
            input = correct_inputs[name]

            if placeholder == input:
                pass
            else:
                self.fail((placeholder, input))

    def validate_errors(self, errors, expected_errors):
        commum_errors = {
            'username': [
                'Size less than 4 characters.', 'Username already in use.'
            ],
            'email': ['Email already used.'],
            'password': [
                'Size smaller than 8 characters.', 'Without the use of symbols.',
                'Without the use of numbers.', 'Passwords are not the same.'
            ]
        }

        self.fail('finish the test!')

        # O erro vai vim tipo: Password: 'Without the use of symbols'
        # dai pego o commum_error que tenha a mesma chave que o erro
        # e verifico se o erro foi validado

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # # He sees the Login button and presses it.
        # wait.until(EC.visibility_of_element_located((
        #     By.CLASS_NAME, 'login-button'
        # ))).click()

        # He realizes that he doesn't have an account
        # and clicks the Sign up button.
        # self.browser.find_element(By.CLASS_NAME, 'sign-up-button')

        # See the registration screen
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))
        self.assertEqual(self.browser.title, 'Sign Up')

        # Check that all inputs have placeholders.
        inputs = form.find_elements(By.CLASS_NAME, 'form-control')
        inputs_information = self.get_all_placeholders(inputs)
        self.validate_placeholders(inputs_information)

    def test_registration_invalid_fields_and_success_redirect(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + reverse('authors:signup'))

        # Ele viu os campos e enviou sem completar nada
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))

        form.submit()

        # Viu que apareceu erros em sua tela
        errors = self.browser.find_elements(By.CLASS_NAME, 'errors')

        self.fail('finish the test!')

        self.validate_errors(errors, 'Campo vazio')

        # Decidiu arrumar o username
        username = form.find_element(By.CLASS_NAME, 'username_field')
        username.send_keys('abc')

        # Viu que isso resultou em um erro
        form.submit()

        # Decidiu arrumar
        username.clear()
        username.send_keys('Test')

        # Mas percebeu que esse nome já existia e recebeu outro erro

        #### abrir outro navegador e criar uma conta com o mesmo nome
        form.submit()

        # Colocou outro nome e viu que não deu mais erro
        username.clear()
        username.send_keys('Testing')
        form.submit()

        # agora tentou arrumar o e-mail
        email = form.find_element(By.CLASS_NAME, 'email_field')
        email.send_keys('test@gmail.com')

        # Mas percebeu também que alguém já usou este email
        # Ele decidiu tentar outro, e deu certo
        email.clear()
        email.send_keys('testing@gmail.com')

        # Agora ele foi tentar colocar uma senha
        password1 = form.find_element(By.CLASS_NAME, 'password1_field')
        password2 = form.find_element(By.CLASS_NAME, 'password2_field')

        password1.send_keys('abc')
        password2.send_keys('abc')

        # Percebeu que ele recebeu um erro que o tamanho
        # é menor que 5 caracteres
        form.submit()

        # Ele então mudou de senha
        password1.clear()
        password2.clear()

        password1.send_keys('abcdef')
        password2.send_keys('abcdef')

        # Mas agora deu um erro que não há numeros, então ele deciciu arrumar
        password1.clear()
        password2.clear()

        password1.send_keys('abcdef1')
        password2.send_keys('abcdef1')

        # Mas viu que não há símbolos e então arrumou novamente, mas esqueceu
        # de arrumar a password2 e recebeu o erro que as senhas não são iguais
        password1.clear()
        password2.clear()

        password1.send_keys('abcdef1!')
        password2.send_keys('abcdef1')

        # Então por fim ele arrumou a password2 e conseguiu entrar
        # na página principal
        password1.clear()
        password2.clear()

        password1.send_keys('abcdef1!')
        password2.send_keys('abcdef1!')

        # foi redirecionado já logado para a home
        self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'home'
        )))
        self.assertEqual(self.browser.title, 'Home')
