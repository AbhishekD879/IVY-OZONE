import os
from time import sleep

from appium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException

import tests_ios_fully_native_regression as tests_native
from voltron.pages.shared import get_driver
from voltron.pages.shared import set_driver
from voltron.utils import mixins


class IosLocalEmulator(mixins.LoggingMixin):
    platform = None
    platform_version = None

    def __init__(self):
        super(IosLocalEmulator, self).__init__()
        self.platform_version = tests_native.ios_platform_version
        self.device_type = tests_native.device_name
        self.uuid = None
        self.ios_app_path = tests_native.ios_app_path

    def get_desired_caps(self, version=''):
        ios_version = version if version else 12.1
        desired_caps = {'platformName': 'iOS',
                        'platformVersion': ios_version,
                        'deviceName': self.device_type,
                        'automationName': 'XCUITest',
                        'noReset': 'false'}
        if self.uuid:
            desired_caps['uuid'] = self.uuid
        desired_caps['app'] = self.get_app_path()
        self.__class__.version = version
        return desired_caps

    def get_app_path(self):
        path_to_app = f'{self.ios_app_path}/Debug-iphonesimulator/' \
            f'{"Coral" if tests_native.settings.brand == "bma" else tests_native.settings.brand.title()} Sports Betting.app'
        return os.path.abspath(os.path.join(os.path.dirname(__file__), path_to_app))

    def start_application(self):
        set_driver(webdriver.Remote('http://localhost:4723/wd/hub', self.get_desired_caps()))

    def swipe(self, start_x, start_y, end_x, end_y):
        get_driver().swipe(start_x, start_y, end_x, end_y)

    def turn_connection_on(self):
        get_driver().set_network_connection(4)

    def turn_connection_off(self):
        get_driver().set_network_connection(1)

    def accept_allert(cls, timeout=5):
        waiting_time = 0
        time_to_stop = timeout
        while waiting_time < time_to_stop:
            try:
                get_driver().switch_to.alert.accept()
                return
            except (NoAlertPresentException, WebDriverException):
                pass
            waiting_time += 0.5
            sleep(0.5)

    def dismiss_allert(cls, timeout=5):
        waiting_time = 0
        time_to_stop = timeout
        while waiting_time < time_to_stop:
            try:
                get_driver().switch_to.alert.dismiss()
                return
            except (NoAlertPresentException, WebDriverException):
                pass
            waiting_time += 0.5
            sleep(0.5)

    @staticmethod
    def put_app_in_background(seconds=5):
        get_driver().background_app(seconds)

    def close_app(self):
        get_driver().close_app()

    def quit(self):
        get_driver().quit()

    def launch_app(self):
        get_driver().launch_app()
