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
class Test_C1377332_Verify_Settled_Bets_tab_when_user_is_logged_out(Common):
    """
    TR_ID: C1377332
    NAME: Verify 'Settled Bets' tab when user is logged out
    DESCRIPTION: This test case verifies login from 'Settled Bets' tab
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_open_settled_bets_tabmobile_my_bets_page___settled_betstabletdesktop_bet_slip_widget___settled_betsuse_direct_url_bet_history(self):
        """
        DESCRIPTION: Open 'Settled Bets' tab
        DESCRIPTION: Mobile: 'My Bets' page -> 'Settled Bets'
        DESCRIPTION: Tablet/Desktop: 'Bet Slip' widget -> 'Settled Bets'
        DESCRIPTION: (Use direct URL: .../Bet-history)
        EXPECTED: * 'Settled Bets' tab is opened
        EXPECTED: * "Please log in to see your Settled Bets." message is displayed
        EXPECTED: * "Log In" button is shown below the message
        """
        pass

    def test_002_log_in_from_settled_bets_tab(self):
        """
        DESCRIPTION: Log in from 'Settled Bets' tab
        EXPECTED: *   User is logged in
        EXPECTED: *   Content of page is visible
        """
        pass
