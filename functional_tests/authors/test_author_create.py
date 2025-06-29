from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests

# from selenium.webdriver.common.keys import Keys


class TestAuthorCreate(BaseWebDriverForFunctionalTests):
    def get_all_placeholders(self):
        pass

    def test_user_can_see_all_the_placeholders(self):
        # Usuário entra na tela inicial
        self.browser.get(self.live_server_url + '/signup/')

        # Ele visualiza o botão de Login e aperta nela
        wait = self.delay()
        wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'login-button'
        )))

        # Ele percebe que não tem uma conta e aperta no botão de Sign up
        self.browser.find_element(By.CLASS_NAME, 'sign-up-button')

        # Vê a tela de se cadastrar
        wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))
        self.assertEqual(self.browser.title, 'Sign up')

        # Verifica que todos os inputs tem placeholders
