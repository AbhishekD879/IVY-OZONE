import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C58694749_Verify_triggering_new_OA_bet_request_with_LOGIN_PLACE_BET(Common):
    """
    TR_ID: C58694749
    NAME: Verify triggering new OA bet request with 'LOGIN & PLACE BET'
    DESCRIPTION: This test case verifies Overask functionality when user adds a selection and uses 'LOGIN & PLACE BET' option.
    PRECONDITIONS: Overask functionality is enabled for Event Type and User:
    PRECONDITIONS: Confluence Instruction - https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
    PRECONDITIONS: - Open the app
    PRECONDITIONS: - Log in to the application
    PRECONDITIONS: - Add selection available for Overask to Betslip
    PRECONDITIONS: - Enter stake value which is higher than maximum bet limit for added selection
    PRECONDITIONS: Check parameters in Local Storage:
    PRECONDITIONS: OX.BetSelections
    PRECONDITIONS: OX.overaskPlaceBetsData
    PRECONDITIONS: OX.overaskIsInProgress
    PRECONDITIONS: OX.overaskUsername
    PRECONDITIONS: ![](index.php?/attachments/get/106947951)
    """
    keep_browser_open = True

    def test_001_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        EXPECTED: - Overask review process is started
        EXPECTED: - Bet trigger OA is displayed in TI (Bet -> BI Requests)
        """
        pass

    def test_002_log_out_from_the_applicationfor_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out from the application:
        DESCRIPTION: **For Desktop:** Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: **For Web Mobile:** Refresh the page
        DESCRIPTION: **For Wrappers:** Kill the app
        EXPECTED: - User is logged out
        EXPECTED: - Betslip is Empty
        """
        pass

    def test_003_add_the_same_selection_from_preconditions_to_betslip_with_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection(self):
        """
        DESCRIPTION: Add the same selection from preconditions to Betslip with stake value which is higher than maximum bet limit for added selection
        EXPECTED: - The same selection is added to Beslip
        """
        pass

    def test_004_tap_login__place_betlogin_and_place_bet_buttoncoralladbrokes(self):
        """
        DESCRIPTION: Tap 'LOGIN & PLACE BET'/'LOGIN AND PLACE BET' button
        DESCRIPTION: (Coral/Ladbrokes)
        EXPECTED: - New Overask review process is started
        EXPECTED: - New Bet trigger OA is displayed in TI (Bet -> BI Requests)
        EXPECTED: - New placeBet request is sent
        """
        pass

    def test_005_log_out_from_the_applicationfor_desktop_click_log_out_item_in_my_account_menufor_web_mobile_refresh_the_pagefor_wrappers_kill_the_app(self):
        """
        DESCRIPTION: Log Out from the application:
        DESCRIPTION: **For Desktop:** Click 'Log Out' item in 'My Account' Menu
        DESCRIPTION: **For Web Mobile:** Refresh the page
        DESCRIPTION: **For Wrappers:** Kill the app
        EXPECTED: - User is logged out
        EXPECTED: - Betslip is Empty
        """
        pass

    def test_006_add_new_selection_another_than_was_used_in_preconditions_to_betslip_with_stake_value_which_is_higher_than_maximum_bet_limit_for_added_selection(self):
        """
        DESCRIPTION: Add new selection another than was used in preconditions to Betslip with stake value which is higher than maximum bet limit for added selection
        EXPECTED: - Selection is added to Beslip
        """
        pass

    def test_007_tap_login__place_betlogin_and_place_bet_buttoncoralladbrokes(self):
        """
        DESCRIPTION: Tap 'LOGIN & PLACE BET'/'LOGIN AND PLACE BET' button
        DESCRIPTION: (Coral/Ladbrokes)
        EXPECTED: - New Overask review process is started
        EXPECTED: - New Bet trigger OA is displayed in TI (Bet -> BI Requests)
        EXPECTED: - New placeBet request is sent
        """
        pass
