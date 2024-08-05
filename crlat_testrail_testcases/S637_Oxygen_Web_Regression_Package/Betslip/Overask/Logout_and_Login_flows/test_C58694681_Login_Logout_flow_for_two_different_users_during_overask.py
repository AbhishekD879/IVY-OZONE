import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C58694681_Login_Logout_flow_for_two_different_users_during_overask(Common):
    """
    TR_ID: C58694681
    NAME: Login/Logout flow for two different users  during overask
    DESCRIPTION: This test case verifies Overask process when different users logged in/logged out
    PRECONDITIONS: Overask functionality is enabled for Event Type and User:
    PRECONDITIONS: Confluence Instruction - https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: User #1 - has Overask enabled
    PRECONDITIONS: User #2 - has Overask enabled
    PRECONDITIONS: - Open the app
    PRECONDITIONS: - Log in to application with User #1
    """
    keep_browser_open = True

    def test_001_add_selection_available_for_overask_to_betslip(self):
        """
        DESCRIPTION: Add selection available for Overask to Betslip
        EXPECTED: - Selection is successfully added
        """
        pass

    def test_002_open_betslip__gt_enter_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection(self):
        """
        DESCRIPTION: Open Betslip -&gt; Enter stake value which is higher than maximum bet limit for added selection
        EXPECTED: - Betslip is opened
        EXPECTED: - Stake value is entered
        """
        pass

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Overask review process is started
        EXPECTED: - Bet trigger OA is displayed in TI (Bet -&gt; BI Requests)
        """
        pass

    def test_004_log_out_with_user_1for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out with User #1:
        DESCRIPTION: **For Desktop:** Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: **For Web Mobile:** Refresh the page
        DESCRIPTION: **For Wrappers:** Kill the app
        EXPECTED: - User #1 is logged out
        EXPECTED: - Added selection from step#1 is cleared
        EXPECTED: - Betslip is empty
        """
        pass

    def test_005_log_in_with_user_2_to_application(self):
        """
        DESCRIPTION: Log in with User #2 to application
        EXPECTED: - User #2 is logged in
        """
        pass

    def test_006_repeat_steps_1_3(self):
        """
        DESCRIPTION: Repeat steps 1-3
        EXPECTED: - Overask review process is started for User #2
        EXPECTED: - Bet trigger OA is displayed in TI (Bet -&gt; BI Requests)
        """
        pass

    def test_007_log_out_with_user_2for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out with User #2:
        DESCRIPTION: **For Desktop:** Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: **For Web Mobile:** Refresh the page
        DESCRIPTION: **For Wrappers:** Kill the app
        EXPECTED: - User #2 is logged out
        EXPECTED: - Overask selection from step#8 is cleared
        EXPECTED: - Betslip is empty
        """
        pass

    def test_008_login_to_application_with_user_1_again_and_go_to_the_betslip(self):
        """
        DESCRIPTION: Login to application with User #1 again and go to the Betslip
        EXPECTED: - Betslip is empty
        """
        pass
