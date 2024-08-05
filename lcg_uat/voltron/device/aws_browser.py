import os
from time import sleep

from selenium.webdriver import Chrome as ChromeDriver

from voltron.device.local_browser import LocalBrowser


class AwsBrowser(LocalBrowser):
    """
    For running on GoCD on Chrome
    """
    _chrome_driver = {'type': ChromeDriver, 'service_args': ['--verbose', '--log-path=./chromedriver.log']}

    @property
    def resolution(self):
        return '%sx%s' % (self.width, self.height)

    @resolution.setter
    def resolution(self, value):
        width, height = value.split('x')
        if (self.width, self.height) != (width, height):
            os.system('xrandr -s %s' % value)
            sleep(1.5)
            self._driver.set_window_size(width=width, height=height)
            self.width, self.height = width, height
            sleep(1.5)
