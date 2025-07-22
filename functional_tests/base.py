from time import sleep

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.translation import activate
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

    def logout_user(self):
        self.client.logout()
        self.browser.delete_all_cookies()
        self.browser.refresh()

    @staticmethod
    def sleep(time=5):
        sleep(time)
