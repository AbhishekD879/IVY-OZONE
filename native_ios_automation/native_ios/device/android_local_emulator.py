import os
from time import sleep

from appium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException
import tests_ios_fully_native_regression as tests_native
from native_ios.pages.shared import get_driver
from native_ios.pages.shared import set_driver
from native_ios.utils import mixins


class AndroidLocalEmulator(mixins.LoggingMixin):
    platform = tests_native.platform

    def __init__(self):
        super(AndroidLocalEmulator, self).__init__()
        self.device_type = tests_native.device_name
        self.uuid = None
        self.ios_app_path = tests_native.ios_app_path

    def get_desired_caps(self, version=''):
        desired_caps = {
            'platformName': self.platform,
            # 'deviceName': 'Pixel_3_XL_API_29',
            'appium:automationName': 'uiautomator2',
            'noReset': False,
            'uiautomator2ServerInstallTimeout': 1000000,
            'appium:autoGrantPermissions': True,
            # 'appium:appPackage': "com.mobenga.ladbrokes",
            'appium:appActivity': 'com.galacoral.android.Splash',
            'appium:appWaitActivity': "com.galacoral.android.MainActivity",
            # "appPackage": "com.mobenga.ladbrokes",
            # "appActivity": "com.galacoral.android.MainActivity",
            "appium:dontStopAppOnReset": True
        }
        if self.uuid:
            desired_caps['uuid'] = self.uuid
        if tests_native.settings.brand == "bma":
            desired_caps['appium:app'] = \
                '/Users/abhishek.diwate/Desktop/native_automation/native_ios_automation/apps/android/coral.7.0.1-debug.apk'
        else:
            desired_caps['appium:app'] = \
                '/Users/abhishek.diwate/Desktop/native_automation/native_ios_automation/apps/android/ladbrokes.7.0.1-debug.apk'
        # desired_caps['app'] = self.get_app_path()
        self.__class__.version = version
        return desired_caps

    def get_app_path(self):
        path_to_app = f'{self.ios_app_path}/Debug-iphonesimulator/' \
                      f'{"Coral" if tests_native.settings.brand == "bma" else tests_native.settings.brand.title()} Sports Betting.app'
        return os.path.abspath(os.path.join(os.path.dirname(__file__), path_to_app))

    def start_application(self):
        set_driver(webdriver.Remote('http://127.0.0.1:4723', self.get_desired_caps()))

    @staticmethod
    def swipe(start_x, start_y, end_x, end_y):
        get_driver().swipe(start_x, start_y, end_x, end_y)

    @staticmethod
    def turn_connection_on():
        get_driver().set_network_connection(4)

    @staticmethod
    def turn_connection_off():
        get_driver().set_network_connection(1)

    @staticmethod
    def accept_alert(timeout=5):
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

    @staticmethod
    def dismiss_alert(timeout=5):
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
        # todo: recheck in VOL-6205
        get_driver().background_app(seconds)

    @staticmethod
    def close_app():
        # todo: recheck in VOL-6205
        driver = get_driver()
        if driver:
            driver.close_app()

    @staticmethod
    def quit():
        # todo: recheck in VOL-6205
        driver = get_driver()
        if driver:
            driver.quit()

    @staticmethod
    def launch_app():
        # todo: recheck in VOL-6205
        get_driver().launch_app()
