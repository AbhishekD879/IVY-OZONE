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
class Test_C58694810_Verify_Betslip_behavior_for_user_with_without_Overask_available(Common):
    """
    TR_ID: C58694810
    NAME: Verify Betslip behavior for user with/without  Overask available
    DESCRIPTION: This test case verifies Betslip behavior for user with/without  Overask available
    PRECONDITIONS: Overask functionality is enabled for Event Type and User:
    PRECONDITIONS: Confluence Instruction - https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: User #1 - Overask enabled for user
    PRECONDITIONS: User #2 - Overask disabled for user
    PRECONDITIONS: 1. Open the app
    PRECONDITIONS: 2. Log in to application with User #1
    PRECONDITIONS: 3. Add selection available for Overask to Betslip
    PRECONDITIONS: 4. Enter stake value which is higher than maximum bet limit for added selection
    """
    keep_browser_open = True

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Overask review process is started
        EXPECTED: - Bet trigger OA is displayed in TI (Bet -&gt; BI Requests)
        """
        pass

    def test_002_log_out_from_the_application_with_user_1for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out from the application with User #1:
        DESCRIPTION: For Desktop: Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: For Web Mobile: Refresh the page
        DESCRIPTION: For Wrappers: Kill the app
        EXPECTED: - User is logged out
        EXPECTED: - Betslip is Empty
        """
        pass

    def test_003_log_in_to_application_with_user_2_wo_overask_available(self):
        """
        DESCRIPTION: Log in to application with User #2 (w/o Overask available)
        EXPECTED: - User is logged in
        """
        pass

    def test_004_add_the_selection_from_preconditions_to_betslip_with_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection(self):
        """
        DESCRIPTION: Add the selection from preconditions to Betslip with stake value which is higher than maximum bet limit for added selection
        EXPECTED: - Selection is successfully added
        """
        pass

    def test_005_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - 'Maximum stake of &lt;currency&gt;&lt;amount&gt;' ( **Coral** ) /'Sorry, the maximum stake for this bet is &lt;currency&gt;&lt;amount&gt;' ( **Ladbrokes** ) error message is displayed above stake section
        """
        pass

    def test_006_log_out_from_the_application_with_user_2for_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out from the application with User #2:
        DESCRIPTION: For Desktop: Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: For Web Mobile: Refresh the page
        DESCRIPTION: For Wrappers: Kill the app
        EXPECTED: - User is logged out
        EXPECTED: - Selection is shown in Betslip
        """
        pass
