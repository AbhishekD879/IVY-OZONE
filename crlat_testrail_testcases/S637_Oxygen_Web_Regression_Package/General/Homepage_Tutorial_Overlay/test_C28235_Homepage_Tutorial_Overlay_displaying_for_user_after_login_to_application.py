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
class Test_C28235_Homepage_Tutorial_Overlay_displaying_for_user_after_login_to_application(Common):
    """
    TR_ID: C28235
    NAME: Homepage Tutorial Overlay displaying for user after login to application
    DESCRIPTION: This test case verifies Homepage Tutorial Overlay displaying after user's login to application
    DESCRIPTION: AUTOTEST [C2593985]
    PRECONDITIONS: **JIRA tickets:**
    PRECONDITIONS: - BMA-7029 Homepage Tutorial Overlay
    PRECONDITIONS: - BMA-16264 Cookie Banner :- Football tutorial displaying when cookie banner message is shown
    PRECONDITIONS: Information that Homepage Tutorial Overlay was shown is saved in Local Storage: name - OX.tutorial, value - true. Cookie is added after Overlay closing via 'Close' or My Bets/Betslip/Balance buttons
    PRECONDITIONS: ![](index.php?/attachments/get/1227)
    """
    keep_browser_open = True

    def test_001_clear_browser_cookies_and_load_oxygen_application(self):
        """
        DESCRIPTION: Clear browser cookies and load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_do_not_login_to_application_and_go_to_the_homepage(self):
        """
        DESCRIPTION: Do not login to application and go to the Homepage
        EXPECTED: Homepage is displayed without Homepage Tutorial Overlay
        """
        pass

    def test_003_login_to_application_with_already_existing_user(self):
        """
        DESCRIPTION: Login to application with already existing user
        EXPECTED: - Homepage is displayed with Homepage Tutorial Overlay
        EXPECTED: - Homepage Tutorial Overlay is displayed under Cookie Banner if its present
        EXPECTED: - Homepage Tutorial Overlay is scrollable on devices with small screen resolution when Cookie Banner is present
        """
        pass

    def test_004_tap_close_button(self):
        """
        DESCRIPTION: Tap 'Close' button
        EXPECTED: *   Homepage Tutorial Overlay is closed
        EXPECTED: *   User stays on the Homepage
        EXPECTED: *   'OX.tutorial: True' cookie is added to Local Storage
        """
        pass

    def test_005_repeat_steps_1_and_3tap_my_betsbalancemy_accountbetslip_button(self):
        """
        DESCRIPTION: Repeat steps 1 and 3
        DESCRIPTION: Tap 'My Bets'/Balance/'My Account'/'Betslip' button
        EXPECTED: *   Homepage Tutorial Overlay is closed
        EXPECTED: *   Appropriate page is opened e.g. My Bets/Balance/Betslip
        EXPECTED: *   'OX.tutorial: True' cookie is added to Local Storage
        """
        pass

    def test_006_repeat_steps_1_and_3and_change_url_eg_football(self):
        """
        DESCRIPTION: Repeat steps 1 and 3
        DESCRIPTION: and change URL e.g. football
        EXPECTED: *   Homepage Tutorial Overlay is closed
        EXPECTED: *   User is navigated to appropriate page
        """
        pass

    def test_007_clear_browser_cookies_and_login_with_any_user_that_will_have_to_interact_with_pop_up_after_successful_logineg_user_with_000_balance_user_that_increased_deposit_limits_and_has_to_confirm_this_action__user_that_needs_to_pass_netverify_procedure_user_with_freebets_etc(self):
        """
        DESCRIPTION: Clear browser cookies and login with any user that will have to interact with Pop-up after successful login
        DESCRIPTION: (e.g. user with '0.00' balance, user that increased deposit limits and has to confirm this action,  user that needs to pass NetVerify procedure, user with freebets, etc.)
        EXPECTED: *   User is redirected to the Homepage
        EXPECTED: *   Homepage Tutorial Overlay is displayed
        """
        pass

    def test_008_close_homepage_tutorial_overlay(self):
        """
        DESCRIPTION: Close Homepage Tutorial Overlay
        EXPECTED: *   Homepage Tutorial Overlay is closed
        EXPECTED: *   Appropriate Pop-up messages are displayed one by one after closing the Overlay
        EXPECTED: *   User stays on the Homepage
        EXPECTED: *   'OX.tutorial: True' cookie is added to Local Storage
        """
        pass
