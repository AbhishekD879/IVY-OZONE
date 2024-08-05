from abc import ABCMeta
from time import sleep
import tests_ios_fully_native_regression as tests
from native_ios.utils import mixins
from native_ios.pages.shared.components.home_page import NativeHomePage


class NativeApp(mixins.LoggingMixin, metaclass=ABCMeta):

    def __init__(self):
        super().__init__()
        self.close_cookie()

    @property
    def home_page(self):
        return NativeHomePage()

    def close_cookie(self):
        if tests.settings.brand == 'bma':
            return
        try:
            #sleep(15)
            self.home_page.cookie_pop_up_close_icon.click()
        except Exception as e:
            self._logger.info('Cookie popup is not displayed')

    def login(self, username=None, password=None):
        home_page: NativeHomePage = self.home_page
        home_page.login_button.click()
        username = username if username else tests.settings.betplacement_user
        password = password if password else tests.settings.default_password
        login_popup = home_page.login_popup
        login_popup.username = username
        login_popup.password = password
        login_popup.login_button.click()
        sleep(15)
        try:
            login_popup.odds_boost.click()
        except Exception:
            self._logger.info('Odds boost/Super boost popup is not displayed')
        sleep(3)
        try:
            self.home_page.timeline_tutorial_overlay.click()
        except Exception as e:
            self._logger.info('Timeline tutorial overlay is not displayed')

    def open_sport(self):
        pass
