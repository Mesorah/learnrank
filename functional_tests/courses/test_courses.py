from selenium.webdriver.common.by import By

from functional_tests.base import BaseWebDriverForFunctionalTests


class TestClassesFT(BaseWebDriverForFunctionalTests):
    language_header = "en-US,en"
    locale = "en"

    def setUp(self):
        super().setUp()

        self.wait = self.delay()

        # Enters to home page
        self.go_to_url()

        self.create_valid_user(auto_login=True)

    def test_start_class_redirect_to_the_correct_page(self):
        # Clicks to course page
        self.click_when_visible(By.CLASS_NAME, 'testing-courses')

        # Verify the page title
        self.assertEqual(self.browser.title, 'Courses')

    def test_card_when_press_no__it_will_disappear(self):
        # Clicks to course page
        self.click_when_visible(By.CLASS_NAME, 'testing-courses')

        # View the card and click
        self.click_when_visible(By.XPATH, '//button[@data-choice="no"]')

        # The card disappeared from the screen.
        overlay = self.find_element(By.CLASS_NAME, 'overlay')
        self.assertEqual(overlay.is_displayed(), False)

    def test_card_when_press_no__it_is_redirected(self):
        # Clicks to course page
        self.click_when_visible(By.CLASS_NAME, 'testing-courses')

        # View the card and click
        self.click_when_visible(By.XPATH, '//button[@data-choice="yes"]')

        self.assertIn('Aulas', self.browser.page_source)
