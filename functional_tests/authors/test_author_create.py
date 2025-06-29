from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests

# from selenium.webdriver.common.keys import Keys


class TestAuthorCreate(BaseWebDriverForFunctionalTests):
    def get_all_placeholders(self, inputs):
        inputs_information = []

        for input in inputs:
            placeholder = input.get_attribute('placeholder')
            name = input.get_attribute('name')
            inputs_information.append((name, placeholder))

        return inputs_information

    def validates_placeholders(self, inputs_information):
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

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.browser.get(self.live_server_url + '/signup/')

        # # He sees the Login button and presses it.
        wait = self.delay()
        # wait.until(EC.visibility_of_element_located((
        #     By.CLASS_NAME, 'login-button'
        # ))).click()

        # He realizes that he doesn't have an account
        # and clicks the Sign up button.
        # self.browser.find_element(By.CLASS_NAME, 'sign-up-button')

        # See the registration screen
        form = wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'sign-up-form'
        )))
        self.assertEqual(self.browser.title, 'Sign Up')

        # Check that all inputs have placeholders.
        inputs = form.find_elements(By.TAG_NAME, 'input')
        inputs_information = self.get_all_placeholders(inputs)
        self.validates_placeholders(inputs_information)
