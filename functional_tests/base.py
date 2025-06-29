from time import sleep

from django.test import LiveServerTestCase

from utils.browser import get_chrome_driver


class BaseWebDriverForFunctionalTests(LiveServerTestCase):
    def setUp(self):
        self.driver = get_chrome_driver()
        return super().setUp()

    def tearDown(self):
        self.driver.quit()
        return super().tearDown()

    @staticmethod
    def sleep(time=5):
        sleep(time)
