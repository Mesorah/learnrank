from selenium.webdriver.common.by import By

import authors.constants as const
from functional_tests.base import BaseWebDriverForFunctionalTests


class TestChangeInformationFT(BaseWebDriverForFunctionalTests):
    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_user_can_change_username(self):
        # User enters the website
        self.go_to_url()

        # Log into your profile
        # TODO leave it to log in through the dashboard

        # Click on change username
        self.click_when_visible(By.CLASS_NAME, 'change-information')

        # Receives the error message
        # error_message = self.get_text(By.CLASS_NAME, 'alert-error')

        # self.assertEqual(error_message, const.CANNOT_ACCESS_NOT_LOGGED_ERROR)
        # TODO When transforming into a class-based view,
        # include the login error

        # He realized that he was redirected to the login
        # page and needs to be logged in.
        self.assertEqual(self.browser.title, 'Login')

        # He realizes that he needs to be logged in.
        self.create_valid_user(auto_login=True)

        # Click on change the username again
        self.click_when_visible(By.CLASS_NAME, 'change-information')

        # It is redirected to the opening page
        # TODO make the extra URL stay on the same page
        self.assertEqual(self.browser.title, 'Change username')

        # He saw that his name was in the current username.
        current_username = self.find_element(By.ID, 'id_current_username')
        current_username_value = current_username.get_attribute('value')

        self.assertEqual(current_username_value, 'testing')

        # He changes the username
        self.fill_credentials(id_new_username='new_username', submit=True)

        # He saw your new username
        username = self.get_text(By.CLASS_NAME, 'username')
        self.assertEqual(username, 'new_username')

        # Decide to try the username again
        self.click_when_visible(By.CLASS_NAME, 'change-information')

        # Sees that now you need to wait 7 days
        error_message = self.get_text(By.CLASS_NAME, 'alert-error')

        self.assertEqual(error_message, 'FAIL')

    def test_user_can_not_change_username(self):
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
        self.assertEqual(error_message, const.USERNAME_TAKEN_ALREADY_ERROR)
