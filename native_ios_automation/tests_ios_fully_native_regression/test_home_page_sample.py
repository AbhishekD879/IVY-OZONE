from time import sleep

import pytest
from tests_ios_fully_native_regression.base_test import BaseTest


@pytest.mark.ios
class Test_Home_Page_Sample(BaseTest):
    """
    NAME: Test home page components
    DESCRIPTION: This test case verifies home page components
    """

    def test_001_home_page(self):
        """
        Home Page
        """
        sleep(5)
        # self.native_app.home_page.login_button.click()
        self.native_app.login()
        # self.assertTrue(self.native_app.home_page.home_button.is_enabled(), msg='Home button is not enabled')
        # self.assertTrue(self.native_app.home_page.logo.is_enabled(), msg='Logo is not displayed')
        # self.assertTrue(self.native_app.home_page.login_button.is_enabled(), msg='Login button is not displayed')
