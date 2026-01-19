from selenium.webdriver.common.by import By

from functional_tests.base import BaseWebDriverForFunctionalTests


class TestClassesFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

    def test_start_class_redirect_to_the_correct_page(self):
        # Enters to home page
        self.go_to_url()

        self.click_when_visible(By.CLASS_NAME, 'testing-classes')

        self.assertEqual(self.browser.title, 'Classes')
