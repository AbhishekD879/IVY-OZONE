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
class Test_C15860060_from_OX99_Betslip_header_and_sub_headers_UI_for_Logged_in_User_on_TABLET_Desktop(Common):
    """
    TR_ID: C15860060
    NAME: [from OX99] Betslip: header and sub headers UI for Logged in User on TABLET/Desktop
    DESCRIPTION: This test case verifies betslip header and sub-headers UI for Logged in User
    PRECONDITIONS: User account with a positive balance
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_user_account__from_preconditions(self):
        """
        DESCRIPTION: Log in User account ( from Preconditions)
        EXPECTED: User is logged in
        """
        pass

    def test_003_verify_betslip_header_ui(self):
        """
        DESCRIPTION: Verify betslip header UI
        EXPECTED: Betslip header area is displayed and it includes:
        EXPECTED: * Betslip tab
        EXPECTED: * My Bets tab
        EXPECTED: Betslip tab is selected by default and "*Your betslip is empty* Please add one or more selections to place a bet" message is displayed below the betslip header
        EXPECTED: **[For Ladbrokes on Tablet]**: Button 'Go Betting' is present
        """
        pass

    def test_004_navigate_to_my_bets_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'My Bets' sub-tab
        EXPECTED: My Bets tab is displayed and sub-headers are displayed including:
        EXPECTED: Cash Out
        EXPECTED: Open Bets
        EXPECTED: Settled Bets
        EXPECTED: Shop Bets
        EXPECTED: Cash Out sub-tab is selected by default and List of available not resulted bets is present
        """
        pass

    def test_005_navigate_to_open_bets_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' sub-tab
        EXPECTED: Sub-tab is opened with filter 'Regular'
        """
        pass

    def test_006_navigate_to_settled_bets_sub_tab(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' sub-tab
        EXPECTED: Calendar icons 'From' and 'To' are present
        """
        pass

    def test_007_add_some_selections_to_betslip_and_verify_betslip_tab(self):
        """
        DESCRIPTION: Add some selections to betslip and verify 'Betslip' tab
        EXPECTED: Added selection is displayed in the Betslip content area
        """
        pass
