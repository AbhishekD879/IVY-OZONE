import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod - commented for prod now, as there's not good to register so many prod users
# @pytest.mark.crl_hl
@pytest.mark.mobile_only
@pytest.mark.popup
@pytest.mark.tutorial_overlay
@pytest.mark.user_account
@pytest.mark.cookies
@pytest.mark.medium
@pytest.mark.local_storage
@pytest.mark.navigation
@vtest
class Test_C28236_Homepage_Tutorial_Overlay_Displaying_After_New_User_Registration(BaseUserAccountTest):
    """
    TR_ID: C28236
    VOL_ID: C9697663
    NAME: Homepage Tutorial Overlay displaying after new user registration
    DESCRIPTION: This test case verifies Homepage Tutorial Overlay displaying after new user registration
    PRECONDITIONS: **JIRA tickets:**
    PRECONDITIONS: - BMA-7029 Homepage Tutorial Overlay
    PRECONDITIONS: Information that Homepage Tutorial Overlay was shown is saved in Local Storage: name - OX.tutorial, value - true.
    PRECONDITIONS: Cookie is added after Overlay closing via 'Close' or My Bets/Betslip/Balance buttons
    """
    keep_browser_open = True
    cookie_name = 'OX.tutorial'
    _ls_cookies = {'OX.footballTutorial': 'true', 'OX.cookieBanner': 'true',
                   'OX.oddsBoostSeen': 'true', 'OX.cookieBannerVersion': 12347}

    def verify_tutorial_overlay_not_displayed(self):
        """
        Verifies that Tutorial overlay is not displayed  and 'OX.tutorial: True' cookie is added to Local Storage
        """
        self.assertFalse(self.site.wait_for_tutorial_overlay(expected_result=False),
                         msg='Tutorial overlay is still displayed')

        cookie = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self.assertTrue(cookie, msg="'OX.tutorial: True' cookie is not added to Local Storage")

    def test_001_clear_browser_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Clear browser cookies and load Oxygen application
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.navigate_to(url=tests.HOSTNAME)
        self.site.wait_splash_to_hide()

    def test_002_register_new_user_successfully(self):
        """
        DESCRIPTION: Register new user successfully
        EXPECTED: 'GDPR' splash screen is displayed
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_003_click_coral_logo(self):
        """
        DESCRIPTION: Click on Coral logo
        EXPECTED: User is navigated to Homepage
        EXPECTED: Homepage Tutorial Overlay is displayed
        """
        self.assertTrue(self.site.wait_for_tutorial_overlay(), msg='Tutorial overlay is not displayed')

    def test_004_tap_overlay_close_button(self):
        """
        DESCRIPTION: Tap overlay 'Close' button
        EXPECTED: Homepage Tutorial Overlay is closed
        EXPECTED: User stays on the Homepage
        EXPECTED: 'OX.tutorial: True' cookie is added to Local Storage
        """
        self.site.tutorial_overlay.text_panel.close_button.click()

        self.site.wait_content_state('HomePage')
        self.verify_tutorial_overlay_not_displayed()

    def test_005_repeat_steps_1_3_tap_my_bets_button(self):
        """
        DESCRIPTION: Repeat steps 1 - 3
        DESCRIPTION: Tap 'My Bets' button
        EXPECTED: Homepage Tutorial Overlay is closed
        EXPECTED: User is navigated to My Bets page
        EXPECTED: 'OX.tutorial: True' cookie is added to Local Storage
        """
        self.test_001_clear_browser_cookies_and_load_oxygen_application()
        self.test_002_register_new_user_successfully()
        self.test_003_click_coral_logo()
        self.site.open_my_bets_cashout()
        self.verify_tutorial_overlay_not_displayed()

    def test_006_repeat_steps_1_3_tap_betslip_button(self):
        """
        DESCRIPTION: Repeat steps 1 - 3
        DESCRIPTION: Tap 'Betslip' button
        EXPECTED: Homepage Tutorial Overlay is closed
        EXPECTED: User is navigated to Betslip page
        EXPECTED: 'OX.tutorial: True' cookie is added to Local Storage
        """
        self.test_001_clear_browser_cookies_and_load_oxygen_application()
        self.test_002_register_new_user_successfully()
        self.test_003_click_coral_logo()

        self.site.open_betslip()
        self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open Betslip')
        self.verify_tutorial_overlay_not_displayed()

    def test_007_repeat_steps_1_3_tap_balance_button(self):
        """
        DESCRIPTION: Repeat steps 1 - 3
        DESCRIPTION: Tap 'Balance' button
        EXPECTED: Homepage Tutorial Overlay is closed
        EXPECTED: User is navigated to Betslip page
        EXPECTED: 'OX.tutorial: True' cookie is added to Local Storage
        """
        self.test_001_clear_browser_cookies_and_load_oxygen_application()
        self.test_002_register_new_user_successfully()
        self.test_003_click_coral_logo()

        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        self.verify_tutorial_overlay_not_displayed()

    def test_008_register_new_user_successfully_without_clearing_cookies(self):
        """
        DESCRIPTION: Do not clear cookies and successfully register new user
        DESCRIPTION: Go to the Homepage
        EXPECTED: User is redirected to the Homepage
        EXPECTED: Homepage Tutorial Overlay is not displayed
        """
        self.site.right_menu.logout()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('HomePage')
        self.test_002_register_new_user_successfully()
        self.site.wait_content_state('HomePage')
        self.verify_tutorial_overlay_not_displayed()
