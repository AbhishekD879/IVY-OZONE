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
class Test_C29220_Verify_Open_Bets_tab_after_Logout(Common):
    """
    TR_ID: C29220
    NAME: Verify 'Open Bets' tab after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: AUTOTEST [C527737]
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger an event when the session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen in one browser tab, open 'My Bets' page
    PRECONDITIONS: *   Login to Oxygen in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however, there is no active session already
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 'My Bets' page is opened
        """
        pass

    def test_002_verify_open_bets_tab(self):
        """
        DESCRIPTION: Verify 'Open Bets' tab
        EXPECTED: **Coral**
        EXPECTED: * Popup message about logging out appears.
        EXPECTED: * User is logged out from the application automatically without performing any actions
        EXPECTED: * User is not able to see 'My Bets' page
        EXPECTED: * User is redirected to the Homepage
        EXPECTED: **Ladbrokes**
        EXPECTED: * User is logged out from the application automatically without performing any actions
        EXPECTED: * User is not able to see 'My Bets' page
        EXPECTED: * User is redirected to the Homepage
        """
        pass
