import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C29210_Verify_Open_Bets_tab_when_user_is_logged_out(Common):
    """
    TR_ID: C29210
    NAME: Verify 'Open Bets' tab when user is logged out
    DESCRIPTION: This test case verifies login from 'Open Bets' tab
    DESCRIPTION: AUTOTEST [C9698233]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_open_bets_tabmobile_my_bets_page___open_bets_open_betstabletdesktop_bet_slip_widget___open_bets(self):
        """
        DESCRIPTION: Open 'Open Bets' tab
        DESCRIPTION: Mobile: 'My Bets' page -> 'Open Bets' (.../open-bets)
        DESCRIPTION: Tablet/Desktop: 'Bet Slip' widget -> 'Open Bets'
        EXPECTED: * 'Open Bets' tab is opened
        EXPECTED: * "Please log in to see your Open Bets." message is displayed
        EXPECTED: * "Log In" button is shown below the message
        """
        pass

    def test_002_log_in_from_open_bets_tab(self):
        """
        DESCRIPTION: Log in from 'Open Bets' tab
        EXPECTED: *   User is logged in
        EXPECTED: *   Content of page is visible
        """
        pass
