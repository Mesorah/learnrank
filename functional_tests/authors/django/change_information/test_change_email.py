import pytest
from selenium.webdriver.common.by import By

from functional_tests.base import BaseWebDriverForFunctionalTests


@pytest.mark.skip(reason="Work in progress")
class TestChangeEmailFT(BaseWebDriverForFunctionalTests):
    def test_user_can_change_email_sucess(self):
        # Ele acessa a página
        self.go_to_url()

        # Log into your profile
        # TODO leave it to log in through the dashboard

        # Aperta no botão de trocar de email
        self.click_when_visible(By.CLASS_NAME, 'change-email')

        # Vê que entrou no site de trocar o email
        self.assertEqual(self.browser.title, 'Change email')

        # Preenche o campo para trocar de email corretamente
        pass
