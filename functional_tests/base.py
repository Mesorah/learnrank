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

    def login_user(self):
        user = User.objects.create(username='test')
        self.client.force_login(user=user)

        # Used to login user
        cookie = self.client.cookies['sessionid']
        self.browser.add_cookie({
            'name': 'sessionid',
            'value': cookie.value,
            'secure': False,
            'path': '/'
        })

        self.browser.refresh()

    def wait_until_element(self, by, element, all_element=False):
        if all_element:
            return self.wait.until(EC.visibility_of_all_elements_located((
                by, element
            )))

        return self.wait.until(EC.visibility_of_element_located((
            by, element
        )))

    def go_to_url(self, reverse_url=None):
        self.browser.get(
            self.live_server_url + (
                reverse(reverse_url)
                if reverse_url else '')
        )

    def logout_user(self):
        self.client.logout()
        self.browser.delete_all_cookies()
        self.browser.refresh()

    @staticmethod
    def sleep(time=5):
        sleep(time)
