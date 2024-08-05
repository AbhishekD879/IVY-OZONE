import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.bet_history_open_bets
@vtest
class Test_C28153_Verify_Settled_Bets_tab_after_Logout(Common):
    """
    TR_ID: C28153
    NAME: Verify 'Settled Bets' tab after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger an event when the session is over on the server please perform the following steps:
    PRECONDITIONS: * Login to Oxygen in one browser tab, open 'My Bets' page
    PRECONDITIONS: * Login to Oxygen in second browser tab, logout -> session is over on the server
    PRECONDITIONS: * Navigate back to the first browser tab where user is still logged in, however, there is no active session already
    """
    keep_browser_open = True

    def test_001_verify_settled_bets_tab(self):
        """
        DESCRIPTION: Verify 'Settled Bets' tab
        EXPECTED: * User is logged out from the application without performing any action
        EXPECTED: * User is not able to see the content of 'Settled Bets' tab
        EXPECTED: * User is redirected to the Homepage
        EXPECTED: * **"You Are Logged Out"** pop-up appears
        """
        pass

    def test_002_log_in_from_settled_bets_tab(self):
        """
        DESCRIPTION: Log in from 'Settled Bets' tab
        EXPECTED: User is logged in and can see the page content
        """
        pass

    def test_003_repeat_steps_1_3_on_settled_bets_tab_of_account_history_page(self):
        """
        DESCRIPTION: Repeat steps 1-3 on "Settled Bets" tab of 'Account History' page
        EXPECTED: 
        """
        pass
