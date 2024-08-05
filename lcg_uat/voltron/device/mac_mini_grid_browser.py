import os
from time import sleep

from selenium.webdriver import Remote

from voltron.device.local_browser import LocalBrowser


class MacMiniGridBrowser(LocalBrowser):
    """
    For running on Jenkins on Safari on Mac Mini
    """
    record_video = False
    _safari_driver = {'type': Remote, 'command_executor': 'http://127.0.0.1:4444/wd/hub'}

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
