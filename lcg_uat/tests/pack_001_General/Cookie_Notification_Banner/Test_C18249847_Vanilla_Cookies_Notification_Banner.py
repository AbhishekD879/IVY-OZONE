import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.gvc_exeption import GVCException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # TODO
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C18249847_Vanilla_Cookies_Notification_Banner(Common):
    """
    TR_ID: C18249847
    NAME: [Vanilla] Cookies Notification Banner
    DESCRIPTION: Cookie banner is managed by GVC marketing team.
    PRECONDITIONS: Browser/device with no Coral related Cookies.
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

    def test_001_open_the_application(self):
        """
        DESCRIPTION: Open the application.
        EXPECTED: Cookies banner is displayed.
        """
        self.site.wait_content_state(state_name='HomePage')
        url = self.device.get_current_url()
        self.__class__.url = url.replace('?automationtest=true', "") if 'automationtest=true' not in url else url
        self.device.navigate_to(url=self.url)
        self.assertTrue(wait_for_result(lambda: self.site.is_cookie_banner_shown(), timeout=30),
                        msg='Cookies Notification Banner is not shown')
        self.assertTrue(self.site.is_cookie_banner_shown(), msg='Cookies Notification Banner is not shown')

    def test_002_verify_cookies_banner_content(self):
        """
        DESCRIPTION: Verify cookies banner content.
        EXPECTED: - "We use cookies to provide you with a great user experience. By using Coral, you agree to our use of cookies." text
        EXPECTED: - "cookies" word is also a link to coral cookies policy
        EXPECTED: - Green 'OK' button
        """
        actual_description = self.site.cookie_banner.description.text
        actual_description = actual_description.replace(",", "")
        expected_description = vec.bma.COOKIES_DESCRIPTION.split(",")[1] + vec.bma.COOKIES_DESCRIPTION.split(",")[2] + vec.bma.COOKIES_DESCRIPTION.split(",")[3]
        self.assertIn(expected_description, actual_description,
                      msg=f'Expected cookies description: {expected_description} not not found in expected: {actual_description} ')
        self.assertTrue(self.site.cookie_banner.ok_button.is_displayed(), msg=' Green OK button is not shown')

    def test_003_click_ok_button(self):
        """
        DESCRIPTION: Click 'OK' button.
        EXPECTED: Cookies banner is closed.
        """
        self.site.cookie_banner.ok_button.click()
        self.assertTrue(self.site.is_cookie_banner_shown(), msg='Cookies Notification Banner is shown')

    def test_004_open_the_application_in_the_same_browser_again(self):
        """
        DESCRIPTION: Open the application in the same browser again.
        EXPECTED: Cookies banner is not displayed.
        """
        self.device.open_new_tab()
        self.device.open_tab(tab_index=0)
        self.device.close_current_tab()
        self.device.switch_to_new_tab()
        self.device.navigate_to(url=self.url)
        self.assertFalse(self.site.is_cookie_banner_shown(), msg='Cookies Notification Banner is shown')
