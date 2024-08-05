import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C29177_TO_EDITCash_Out_after_Logout(Common):
    """
    TR_ID: C29177
    NAME: [TO EDIT]Cash Out after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: **Jira tickets:** BMA-5678 (Handle HTTP Error 401)
    DESCRIPTION: The TC should be edited according to Vanilla designs as well
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: User has placed a bet on Pre Match or In-Play match (Singles and Multiple bets) where Cash Out and Partial Cash Out offers are available (on SS see cashoutAvail="Y" on Event and Market level to be sure whether COMB option is available).
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen in one browser tab, open 'Cash Out' tab
    PRECONDITIONS: *   Login to Oxygen in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_002_refresh_cash_out_page(self):
        """
        DESCRIPTION: Refresh 'Cash Out' page
        EXPECTED: * User is logged out from the application automatically without performing any actions
        EXPECTED: * User is not able to see Cash Out bet lines and to perform Cash Out operations
        EXPECTED: *  User is redirected to the Homepage*
        EXPECTED: * "You Are Logged Out" pop up is displayed in the center of the page
        """
        pass

    def test_003_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_004_try_to_tap_partial_cash_out_button(self):
        """
        DESCRIPTION: Try to tap 'PARTIAL CASH OUT' button
        EXPECTED: * Popup message about logging out appears.
        EXPECTED: * User is logged out from the application performing any actions
        EXPECTED: * User is not able to see Cash Out bet lines and to perform Cash Out operations
        EXPECTED: * He/she is redirected to the Homepage
        """
        pass

    def test_005_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_006_try_to_tap_cash_out_button(self):
        """
        DESCRIPTION: Try to tap 'CASH OUT' button
        EXPECTED: * Popup message about logging out appears.
        EXPECTED: * User is logged out from the application without performing any actions
        EXPECTED: * User is not able to see Cash Out bet lines and to perform Cash Out operations
        EXPECTED: * He/she is redirected to the Homepage
        EXPECTED: * User balance is not changed
        """
        pass
