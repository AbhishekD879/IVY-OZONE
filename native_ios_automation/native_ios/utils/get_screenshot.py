import logging

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from native_ios.pages.shared import get_driver

_logger = logging.getLogger('native_ios_logger')
SCREENSHOTS = []


def screenshot():

    driver = get_driver()
    if driver:
        try:
            SCREENSHOTS.clear()
            SCREENSHOTS.append(driver.get_screenshot_as_base64())
        except (WebDriverException, TimeoutException) as e:
            _logger.info(f'Bypassing exception: {str(e)}')
