from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests

# from selenium.webdriver.common.keys import Keys


class TestAuthorCreate(BaseWebDriverForFunctionalTests):
    def get_all_placeholders(self):
        pass

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + '/signup/')

        # He sees the Login button and presses it.
        wait = self.delay()
        wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'login-button'
        ))).click()

        # He realizes that he doesn't have an account
        # and clicks the Sign up button.
        # self.browser.find_element(By.CLASS_NAME, 'sign-up-button')

        # # See the registration screen
        # wait.until(EC.visibility_of_element_located((
        #     By.CLASS_NAME, 'sign-up-form'
        # )))
        # self.assertEqual(self.browser.title, 'Sign up')

        # Check that all inputs have placeholders.
