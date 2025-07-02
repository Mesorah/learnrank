from time import sleep

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import WebDriverWait

from utils.browser import get_chrome_driver


class BaseWebDriverForFunctionalTests(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = get_chrome_driver()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def delay(self, time=5):
        return WebDriverWait(self.browser, time)

    @staticmethod
    def sleep(time=5):
        sleep(time)
