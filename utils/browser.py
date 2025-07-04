import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver(language):
    options = Options()

    if os.environ.get('FAST_FUNCTIONAL_TESTS') == '1':
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

    options.add_experimental_option('prefs', {
        'intl.accept_languages': language
    })

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
