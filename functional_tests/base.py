from time import sleep

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.utils.translation import activate
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.browser import get_chrome_driver

User = get_user_model()


class BaseWebDriverForFunctionalTests(StaticLiveServerTestCase):
    language = 'en-US,en'
    locale = 'en'

    def setUp(self):
        self.browser = get_chrome_driver(self.language)
        activate(self.locale)

        super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def delay(self, time=5):
        return WebDriverWait(self.browser, time)

    def wait_for_element(self, by, element, all_element=False):
        if all_element:
            return self.wait.until(EC.visibility_of_all_elements_located((
                by, element
            )))

        return self.wait.until(EC.visibility_of_element_located((
            by, element
        )))

    def find_element(self, by, element, all_element=False):
        if all_element:
            return self.browser.find_elements(by, element)

        return self.browser.find_element(by, element)

    def go_to_url(self, reverse_url=None):
        self.browser.get(
            self.live_server_url + (
                reverse(reverse_url)
                if reverse_url else ''
            )
        )

    def click_when_visible(
            self, by, element, all_element=False, wait_for_element=False
    ):

        if wait_for_element:
            return self.wait_for_element(by, element, all_element).click()

        return self.find_element(by, element, all_element).click()

    def get_text(self, by, element, all_element=False, wait_for_element=True):
        if wait_for_element:
            return self.wait_for_element(by, element, all_element).text

        return self.find_element(by, element, all_element).text

    def fill_field(self): ...

    def is_element_present(self): ...

    def login_user(self, username='testing', password='testing12!@1dsFG'):
        self.client.login(username=username, password=password)

        cookie = self.client.cookies['sessionid']
        self.browser.add_cookie({
            'name': 'sessionid',
            'value': cookie.value,
            'secure': False,
            'path': '/'
        })

        self.browser.refresh()

    def logout_user(self):
        self.client.logout()
        self.browser.delete_all_cookies()
        self.browser.refresh()

    def create_valid_user(
            self,
            username='testing',
            email='testing@example.com',
            password='testing12!@1dsFG',
            auto_login=False
    ):

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        if auto_login:
            self.login_user()

        return user

    def create_invalid_user(self): ...

    def fill_credentials(self): ...

    @staticmethod
    def sleep(time=5):
        sleep(time)


# fill_credentials(username, password) (pode interagir com SeleniumHelpers)
