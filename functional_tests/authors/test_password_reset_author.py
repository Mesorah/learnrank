from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from functional_tests.base import BaseWebDriverForFunctionalTests


class TestPasswordResetAuthorFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

        self.form_data = {
            'username': 'testing',
            'email': 'testing@example.com',
            'password1': 'testing12!@1dsFG',
            'password2': 'testing12!@1dsFG',
        }

    def send_input_keys(self, username, email, password1, password2):
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))

        username_field = form.find_element(By.ID, 'id_username')
        email_field = form.find_element(By.ID, 'id_email')
        password1_field = form.find_element(By.ID, 'id_password1')
        password2_field = form.find_element(By.ID, 'id_password2')

        username_field.clear()
        email_field.clear()
        password1_field.clear()
        password2_field.clear()

        username_field.send_keys(username)
        email_field.send_keys(email)
        password1_field.send_keys(password1)
        password2_field.send_keys(password2)

        form.submit()

        return form

    def test_user_can_see_all_the_placeholders(self):
        # User enters the home screen
        self.browser.get(self.live_server_url)

        self.login_user()

        self.browser.get(
            self.live_server_url + reverse('authors:password_reset')
        )

        # See the password reset page
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))
        self.assertEqual(self.browser.title, 'Password reset')

        # Check that all inputs have placeholders.
        input = form.find_element(By.ID, 'id_email')

        placeholder = input.get_attribute('placeholder')
        name = input.get_attribute('name')

        correct_input = {'email': 'Write your email here.'}

        if placeholder == correct_input[name]:
            pass
        else:
            self.fail((placeholder, correct_input[name]))

    def test_not_logged_user_cannot_access_registration_page(self):
        # User enters the home screen
        self.browser.get(
            self.live_server_url + reverse('authors:password_reset')
        )

        # He noticed that he couldn't enter there
        # and received an error notifying him.
        error_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-error'
        ))).text

        self.assertEqual(
            error_message, 'You cannot access this while not logged in.'
        )

    def test_user_can_see_the_page_styling_and_layout(self):
        # User enters the home screen
        self.browser.get(self.live_server_url)

        self.login_user()

        # User enters the password reset page
        self.browser.get(
            self.live_server_url + reverse('authors:password_reset')
        )

        # His browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # He notices the Submit button color
        submit_button = self.browser.find_element(
            By.XPATH, '//button[text()="Submit"]'
        )
        self.assertEqual(
            submit_button.value_of_css_property('background-color'),
            'rgba(38, 198, 218, 1)'
        )


class TestCreateAuthorPtBRFT(BaseWebDriverForFunctionalTests):
    language = 'pt-BR,pt'
    locale = 'pt-br'

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_user_can_see_portuguese_translation(self):
        # User tried to reset the password without being logged in
        self.browser.get(
            self.live_server_url + reverse('authors:password_reset')
        )

        # Saw the error alerting him
        error_message = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'alert-error'
        ))).text

        self.assertEqual(
            error_message,
            'Você não pode acessar esta página sem estar logado.'
        )

        # So he logged into his account.
        self.login_user()

        # And decided to change his password
        self.browser.get(
            self.live_server_url + reverse('authors:password_reset')
        )

        # He found the form in portuguese
        form = self.wait.until(EC.visibility_of_element_located((
            By.CLASS_NAME, 'author-form'
        )))

        email_input = form.find_element(By.ID, 'id_email')

        email_placeholder = email_input.get_attribute('placeholder')

        self.assertEqual(email_placeholder, 'Escreva seu e-mail aqui.')
        self.assertEqual(self.browser.title, 'Recuperar senha')
