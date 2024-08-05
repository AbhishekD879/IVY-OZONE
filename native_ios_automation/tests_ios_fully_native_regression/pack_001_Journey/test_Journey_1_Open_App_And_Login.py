import pytest
import tests_ios_fully_native_regression as tests
from time import sleep
from tests_ios_fully_native_regression.base_test import BaseTest


@pytest.mark.native
class Test_Journey_1_Open_App_And_Login(BaseTest):
    """
    NAME: Open App And Login
    DESCRIPTION: This test case verifies Login Journey
    """
    def test_001_open_app(self):
        """
        Open The Native App
        """
        homepage = self.native_app.home_page
        self.assertTrue(homepage, msg="App Not Opened")

    def test_002_click_on_login(self):
        """
        Click on Login CTA
        """
        self.native_app.home_page.login_button.click()
        login_popup = self.native_app.home_page.login_popup
        self.assertTrue(login_popup, msg="Login Popup Not Opened even After Login Cta Clicked")

    def test_003_enter_username_and_password(self):
        """
        Enter Credentials
        """
        username = "testgvcld_RT2JIW" if tests.settings.brand != 'bma' else "testgvccl-U3AW6E"
        login_popup = self.native_app.home_page.login_popup
        login_popup.username = username
        login_popup.password = tests.settings.default_password

    def test_004_click_on_login_CTA(self):
        """
        Click On Login Button to Confirm Login
        """
        self.__class__.login_popup = self.native_app.home_page.login_popup
        self.login_popup.login_button.click()

    def test_005_check_login(self):
        self.assertTrue(self.native_app.home_page.module_ribbon.is_displayed(), msg='login is failed')
        # sleep(2)
        # self.login_popup.odds_boost.click()
        # try:
        #     self.login_popup.odds_boost.click()
        # except Exception:
        #     self._logger.info('Odds boost/Super boost popup not displayed')


