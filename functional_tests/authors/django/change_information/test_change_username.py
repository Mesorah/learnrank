from selenium.webdriver.common.by import By

import authors.constants as const
from authors.utils import is_wait_time_done
from functional_tests.base import BaseWebDriverForFunctionalTests


class TestChangeUsernameFT(BaseWebDriverForFunctionalTests):
    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_user_can_change_username_success(self):
        # User enters the website
        self.go_to_url()

        # Log into your profile
        # TODO leave it to log in through the dashboard

        # He realizes that he needs to be logged in.
        self.go_to_url()

        user = self.create_valid_user(auto_login=True)

        # Click on change the username
        self.click_when_visible(By.CLASS_NAME, 'change-information')

        # It is redirected to the opening page
        # TODO make the extra URL stay on the same page
        self.assertEqual(self.browser.title, 'Change information')

        # He saw that his name was in the current username.
        current_username = self.find_element(By.ID, 'id_current_username')
        current_username_value = current_username.get_attribute('value')

        self.assertEqual(current_username_value, 'testing')

        # He changes the username
        self.fill_credentials(id_new_username='new_username', submit=True)
        success_message = self.get_text(By.CLASS_NAME, 'alert-success')
        self.assertEqual(success_message, const.USERNAMED_CHANGED_SUCCESS)

        # He saw your new username
        username = self.get_text(By.CLASS_NAME, 'username')
        self.assertEqual(username, 'new_username')

        # He decides to wait 7 days to change his name again
        new_data = is_wait_time_done()

        user.change_username_data = new_data
        user.save()

        # Clicks to change your username
        self.click_when_visible(By.CLASS_NAME, 'change-information')
        self.fill_credentials(id_new_username='new_username2', submit=True)

        # He received the success message
        success_message = self.get_text(By.CLASS_NAME, 'alert-success')
        self.assertEqual(success_message, const.USERNAMED_CHANGED_SUCCESS)

        # He saw that he changed his username again.
        username = self.get_text(By.CLASS_NAME, 'username')
        self.assertEqual(username, 'new_username2')

    def test_user_can_not_change_username_error(self):
        # User enters the website
        self.go_to_url()

        # Log into your profile
        # TODO leave it to log in through the dashboard

        # Click on change username
        self.click_when_visible(By.CLASS_NAME, 'change-information')

        # Receives the error message
        error_message = self.get_text(By.CLASS_NAME, 'alert-error')

        self.assertEqual(error_message, const.CANNOT_ACCESS_NOT_LOGGED_ERROR)

        # He realized that he was redirected to the login
        # page and needs to be logged in.
        self.assertEqual(self.browser.title, 'Login')

        # He realizes that he needs to be logged in.
        self.go_to_url()

        user = self.create_valid_user(auto_login=True)

        # Clicks to change your username
        self.click_when_visible(By.CLASS_NAME, 'change-information')
        self.fill_credentials(id_new_username='new_username2', submit=True)

        # Decide to try the username again
        self.click_when_visible(By.CLASS_NAME, 'change-information')

        # Sees that you need to wait 7 days
        self.fill_credentials(id_new_username='new_username3', submit=True)
        error_message = self.get_text(By.ID, 'id_new_username_error')

        self.assertEqual(
            error_message, const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 7}
        )

        # He decides to wait 1 days to change his name again.
        new_data = is_wait_time_done(wait_days=1)

        user.change_username_data = new_data
        user.save()

        self.browser.refresh()

        # Decide to try the username again
        self.fill_credentials(id_new_username='new_username3', submit=True)
        error_message = self.get_text(By.ID, 'id_new_username_error')

        # And then noticed that now you need to wait 6 days
        self.assertEqual(
            error_message, const.CANNOT_CHANGE_USERNAME_ERROR % {'days': 6}
        )

    def test_username_exists_can_not_change_username(self):
        # User enters the website
        self.go_to_url()

        # Log into your profile
        # TODO leave it to log in through the dashboard

        self.create_valid_user()

        # He logged in
        self.create_valid_user(username='testing2', auto_login=True)

        # Click on change the username
        self.click_when_visible(By.CLASS_NAME, 'change-information')

        # He try change the username
        self.fill_credentials(id_new_username='testing', submit=True)

        # He saw a form error
        error_message = self.get_text(By.CLASS_NAME, 'errorlist')
        self.assertEqual(error_message, const.USERNAME_ALREADY_TAKEN_ERROR)

    def test_user_can_see_the_page_styling_and_layout(self):
        self.go_to_url()
        self.create_valid_user(auto_login=True)

        # User enters the home screen
        self.go_to_url('authors:change_username')

        # His browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # He notices the Submit button color
        submit_button = self.find_element(
            By.XPATH, '//button[text()="Submit"]'
        )
        self.assertEqual(
            submit_button.value_of_css_property('background-color'),
            'rgba(38, 198, 218, 1)'
        )


class TestChangeUsernamePtBRFT(BaseWebDriverForFunctionalTests):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

        self.go_to_url()
        self.create_valid_user(auto_login=True)

    def test_user_can_see_portuguese_translation(self):
        # User enters the home screen
        self.go_to_url('authors:change_username')

        # And he found the form in portuguese
        current_username_label = self.get_text(
            By.XPATH, '//label[@for="id_current_username"]',
            wait_for_element=False
        )

        new_username_label = self.get_text(
            By.XPATH, '//label[@for="id_new_username"]',
            wait_for_element=False
        )

        new_username_input = self.find_element(
            By.XPATH, '//input[@id="id_new_username"]',
        )

        new_username_placeholder = new_username_input.get_attribute(
            'placeholder'
        )

        self.assertEqual(current_username_label, 'Seu nome de usuário atual:')
        self.assertEqual(new_username_label, 'Novo nome de usuário:')

        self.assertEqual(
            new_username_placeholder, const.NEW_USERNAME_PLACEHOLDER
        )

        self.assertEqual(self.browser.title, 'Mudar informações')

    def test_user_can_see_portuguese_translation_error(self):
        # create another user
        self.create_valid_user(username='testing2')

        # User enters the home screen
        self.click_when_visible(By.CLASS_NAME, 'change-information')

        self.fill_credentials(id_new_username='testing2', submit=True)

        error_message = self.get_text(By.CLASS_NAME, 'errorlist')
        self.assertEqual(error_message, 'Este nome de usuário já está em uso.')

        self.browser.refresh()

        self.fill_credentials(id_new_username='testing3', submit=True)

        self.click_when_visible(By.CLASS_NAME, 'change-information')
        self.fill_credentials(id_new_username='testing4', submit=True)
        error_message = self.get_text(By.ID, 'id_new_username_error')
        self.assertEqual(
            error_message,
            'Você precisa esperar 7 dias antes de poder '
            'alterar seu nome de usuário novamente.'
        )

    def test_user_can_see_portuguese_translation_sucess(self):
        # User enters the home screen
        self.go_to_url('authors:change_username')

        self.fill_credentials(id_new_username='new_username', submit=True)

        success_message = self.get_text(By.CLASS_NAME, 'alert-success')
        self.assertEqual(
            success_message, 'Seu nome de usuário foi alterado com sucesso!'
        )
