import pytest

import tests
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.gvc_exeption import GVCException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.cookies
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C36494633_Cookies_Notification_Banner(Common):
    """
    TR_ID: C36494633
    NAME: Cookies Notification Banner
    DESCRIPTION: This test case verifies Cookies Notification Banner functionality
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: **Cookie Banner is handled on GVC side (Enabling/Disabling, Text configuration, URL navigation )**
        DESCRIPTION: 1. All cookies and cache are cleared
        DESCRIPTION: 2. User is logged out
        """
        if not self.site.window_client_config.cookie_enabled:
            raise GVCException('Cookie Banner is not enabled on GVC side')
        self.delete_cookies()

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: - Homepage is opened
        EXPECTED: - Cookies Notification Banner is displayed at the Bottom
        EXPECTED: ![](index.php?/attachments/get/17649891)
        """
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        self.site.wait_content_state(state_name='HomePage')
        self.assertTrue(self.site.is_cookie_banner_shown(), msg='Cookies Notification Banner is not shown')

    def test_002_navigate_through_app(self):
        """
        DESCRIPTION: Navigate through app
        EXPECTED: Cookies Notification Banner is displayed within app
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        self.assertTrue(self.site.is_cookie_banner_shown(), msg='"Cookie Banner" is not shown on Horseracing page')
        self.site.back_button_click()
        self.site.wait_content_state('Homepage')
        self.navigate_to_page(name='sport/football')
        self.assertTrue(self.site.is_cookie_banner_shown(), msg='"Cookie Banner" is not shown on Football page')
        self.site.open_betslip()
        self.assertTrue(self.site.is_cookie_banner_shown(), msg='"Cookie Banner" is not shown on Betslip')
        self.site.close_betslip()

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Cookies Notification Banner is still displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.is_cookie_banner_shown(),
                        msg='Cookies Notification Banner is not shown')

    def test_004_click__tap_ok_button_on_cookies_notification_banner(self):
        """
        DESCRIPTION: Click / tap 'OK' button on Cookies Notification Banner
        EXPECTED: - Cookies Notification Banner is closed and no more displayed
        EXPECTED: (Note: 'euconsent' parameter is set with value 'a' and expiry date for a year in future)
        EXPECTED: ![](index.php?/attachments/get/17649960)
        """
        self.site.cookie_banner.ok_button.click()
        cookies = self.device.driver.get_cookies()
        cookie_value = [i['value'] for i in cookies if i['name'] == 'euconsent']
        self.assertEqual(''.join(cookie_value), 'a', msg=f'Euconsent value = {"".join(cookie_value)}, not "a"')
        self.assertFalse(self.site.is_cookie_banner_shown(expected_result=False),
                         msg='Cookies Notification Banner is shown')

    def test_005_navigate_through_app(self):
        """
        DESCRIPTION: Navigate through app
        EXPECTED: Cookies Notification Banner is NOT displayed
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        self.assertFalse(self.site.is_cookie_banner_shown(expected_result=False),
                         msg='"Cookie Banner" is present on "Horseracing" page after accepting the cookie usage policy')
        self.site.back_button.click()
        self.site.wait_content_state('Homepage')
        self.navigate_to_page(name='sport/football')
        self.assertFalse(self.site.is_cookie_banner_shown(expected_result=False),
                         msg='"Cookie Banner" is present on "Football" page after accepting the cookie usage policy')
        self.site.open_betslip()
        self.assertFalse(self.site.is_cookie_banner_shown(expected_result=False),
                         msg='"Cookie Banner" is present on "Betslip" after accepting the cookie usage policy')
        self.site.close_betslip()

    def test_006_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: Cookies Notification Banner is NOT displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertFalse(self.site.is_cookie_banner_shown(expected_result=False),
                         msg='Cookies Notification Banner is shown')

    def test_007_clear_cookies_and_refresh_the_page(self):
        """
        DESCRIPTION: Clear Cookies and refresh the page
        EXPECTED: Cookies Notification Banner is again displayed at the Bottom of page
        """
        self.delete_cookies()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.is_cookie_banner_shown(), msg='Cookies Notification Banner is not shown')
