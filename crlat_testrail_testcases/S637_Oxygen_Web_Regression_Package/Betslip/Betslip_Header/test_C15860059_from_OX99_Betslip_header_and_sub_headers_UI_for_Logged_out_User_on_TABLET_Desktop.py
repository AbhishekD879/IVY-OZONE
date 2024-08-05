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
class Test_C15860059_from_OX99_Betslip_header_and_sub_headers_UI_for_Logged_out_User_on_TABLET_Desktop(Common):
    """
    TR_ID: C15860059
    NAME: [from OX99] Betslip: header and sub-headers UI for Logged out User on TABLET/Desktop
    DESCRIPTION: This test case verifies betslip header and sub-headers UI for Logged out User
    PRECONDITIONS: You should be logged out and have no selections added to betslip
    """
    keep_browser_open = True

    def test_001_load_oxygen_on_tabletdesktop(self):
        """
        DESCRIPTION: Load Oxygen on Tablet/Desktop
        EXPECTED: 
        """
        pass

    def test_002_verify_betslip_header_ui(self):
        """
        DESCRIPTION: Verify betslip header UI
        EXPECTED: Betslip header area is displayed and it includes:
        EXPECTED: * Betslip tab
        EXPECTED: * My Bets tab
        EXPECTED: Betslip tab is selected by default and "**Your betslip is empty** Please add one or more selections to place a bet" message is displayed below the betslip header
        EXPECTED: **[For Ladbrokes on Tablet]**: Button 'Go Betting' is present
        """
        pass

    def test_003_navigate_to_my_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'My Bets' tab
        EXPECTED: My Bets tab is displayed and sub-headers are displayed including:
        EXPECTED: Cash Out
        EXPECTED: Open Bets
        EXPECTED: Settled Bets
        EXPECTED: Shop Bets
        EXPECTED: Cash Out sub-tab is selected by default and "Please log in to see your Cash Out bets" message is displayed below the Cash Out sub-header
        EXPECTED: **Coral:** 'Log In' button is present.
        EXPECTED: **Ladbrokes**: 'Log In' button is NOT present.
        """
        pass

    def test_004_navigate_to_open_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'Open Bets' tab
        EXPECTED: Open Bets sub-tab is selected and "Please log in to see your Open Bets" message is displayed below the Open Bets sub-header
        EXPECTED: **Coral:** 'Log In' button is present.
        EXPECTED: **Ladbrokes**: 'Log In' button is NOT present.
        """
        pass

    def test_005_navigate_to_settled_bets_tab(self):
        """
        DESCRIPTION: Navigate to 'Settled Bets' tab
        EXPECTED: Settled Bets sub-tab is selected and "Please log in to see your Settled Bets" message is displayed below the Settled Bets sub-header
        EXPECTED: **Coral:** 'Log In' button is present.
        EXPECTED: **Ladbrokes**: 'Log In' button is NOT present.
        """
        pass

    def test_006_add_some_selections_to_betslip_and_verify_betslip_tab(self):
        """
        DESCRIPTION: Add some selections to betslip and verify 'Betslip' tab
        EXPECTED: Added selection is displayed in the Betslip content area
        """
        pass
