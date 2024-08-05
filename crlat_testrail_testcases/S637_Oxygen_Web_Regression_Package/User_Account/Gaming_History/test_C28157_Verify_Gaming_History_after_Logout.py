import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C28157_Verify_Gaming_History_after_Logout(Common):
    """
    TR_ID: C28157
    NAME: Verify Gaming History after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by the server automatically when his/her session is over on the server.
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: * [BMA-24547 RTS: Account history tabs > General view (Bet History / Transactions / Gaming History)] [1]
    DESCRIPTION: * [BMA-23956 RTS: Account History > Gaming History] [2]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-24547
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-23956
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger an event when the session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen in one browser tab and open 'Gaming History' tab on 'Account History' page
    PRECONDITIONS: *   Login to Oxygen in second browser tab, log out -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however, there is no active session already
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_002_verify_gaming_history_tab_on_account_history_page(self):
        """
        DESCRIPTION: Verify 'Gaming History' tab on 'Account History' page
        EXPECTED: * User is logged out from the application automatically without performing any actions
        EXPECTED: * User is not able to see the content of 'Gaming History' tab on 'Account History' page
        EXPECTED: * He/she is redirected to the Homepage
        EXPECTED: * Pop-up is shown that session expired
        """
        pass

    def test_003_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_004_try_to_scroll_down_gaming_history_tab_on_account_history_page(self):
        """
        DESCRIPTION: Try to scroll down 'Gaming History' tab on 'Account History' page
        EXPECTED: * Lazy loading is not working and user is not able to see gaming history records
        EXPECTED: * User is logged out from the application automatically without performing any actions
        EXPECTED: * He/she is redirected to the Homepage
        EXPECTED: * Pop-up is shown that session expired
        """
        pass
