from time import sleep

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class BaseWebDriverForFunctionalTests(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        return super().setUp()

    def tearDown(self):
        self.driver.quit()
        return super().tearDown()

    @staticmethod
    def sleep(time=5):
        sleep(time)
