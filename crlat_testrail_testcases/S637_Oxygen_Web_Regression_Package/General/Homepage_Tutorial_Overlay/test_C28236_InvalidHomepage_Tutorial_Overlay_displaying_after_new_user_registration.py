import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C28236_InvalidHomepage_Tutorial_Overlay_displaying_after_new_user_registration(Common):
    """
    TR_ID: C28236
    NAME: [Invalid]Homepage Tutorial Overlay displaying after new user registration
    DESCRIPTION: This test case verifies Homepage Tutorial Overlay displaying after new user registration
    PRECONDITIONS: JIRA tickets:
    PRECONDITIONS: BMA-7029 Homepage Tutorial Overlay
    PRECONDITIONS: Information that Homepage Tutorial Overlay was shown is saved in Cookies: name - Tutorial, value - True. Cookie is added after Overlay closing via 'Close' or My Bets/Betslip/Balance buttons
    """
    keep_browser_open = True

    def test_001_clear_browser_cookies_and_load_invictus_application(self):
        """
        DESCRIPTION: Clear browser cookies and load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_register_new_user_successfully(self):
        """
        DESCRIPTION: Register new user successfully
        EXPECTED: * User is navigated to 'Add Debit/Credit Card' tab on Deposit page
        EXPECTED: * Homepage Tutorial Overlay is NOT displayed
        """
        pass

    def test_003_click_coral_logo(self):
        """
        DESCRIPTION: Click Coral logo
        EXPECTED: * User is navigated to Homepage
        EXPECTED: * Homepage Tutorial Overlay is displayed
        """
        pass

    def test_004_tap_overlay_close_button(self):
        """
        DESCRIPTION: Tap overlay 'Close' button
        EXPECTED: * Homepage Tutorial Overlay is closed
        EXPECTED: * User stays on the Homepage
        EXPECTED: * 'Tutorial: True' cookie is added
        """
        pass

    def test_005_repeat_steps_1___3tap__my_bets_button(self):
        """
        DESCRIPTION: Repeat steps 1 - 3
        DESCRIPTION: Tap ' My Bets' button
        EXPECTED: * Homepage Tutorial Overlay is closed
        EXPECTED: * User is navigated to My Bets page
        EXPECTED: * 'Tutorial: True' cookie is added
        """
        pass

    def test_006_repeat_steps_1_3tap_betslip_button(self):
        """
        DESCRIPTION: Repeat steps 1-3
        DESCRIPTION: Tap 'Betslip' button
        EXPECTED: * Homepage Tutorial Overlay is closed
        EXPECTED: * User is navigated to Betslip page
        EXPECTED: * 'Tutorial: True' cookie is added
        """
        pass

    def test_007_repeat_steps_1_3tap_balance_button(self):
        """
        DESCRIPTION: Repeat steps 1-3
        DESCRIPTION: Tap Balance button
        EXPECTED: * Homepage Tutorial Overlay is closed
        EXPECTED: * Right menu is opened after tapping Balance button
        EXPECTED: * 'Tutorial: True' cookie is added
        """
        pass

    def test_008_repeat_steps_1_3tap_my_account_button(self):
        """
        DESCRIPTION: Repeat steps 1-3
        DESCRIPTION: Tap My Account button
        EXPECTED: * Homepage Tutorial Overlay is closed
        EXPECTED: * Right menu is opened after tapping My Account button
        EXPECTED: * 'Tutorial: True' cookie is added
        """
        pass

    def test_009_do_not_clear_cookies_and_successfully_register_new_usergo_to_the_homepage(self):
        """
        DESCRIPTION: Do not clear cookies and successfully register new user
        DESCRIPTION: Go to the Homepage
        EXPECTED: *   User is redirected to the Homepage
        EXPECTED: *   Homepage Tutorial Overlay is not displayed
        """
        pass
