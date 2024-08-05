import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C28360_Verify_My_Account_menu_after_Logout(Common):
    """
    TR_ID: C28360
    NAME: Verify 'My Account' menu after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by the server automatically when his/her session is over on the server.
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. User should be logged in, but session should be OVER on the server
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To trigger an event when the session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to the app in the first browser tab and open 'My account' page
    PRECONDITIONS: *   Login to the app in the second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where the user is still logged in, however, there is no active session already
    """
    keep_browser_open = True

    def test_001_verify_my_account_page(self):
        """
        DESCRIPTION: Verify 'My Account' page
        EXPECTED: * User is logged out from the application automatically without performing any actions
        EXPECTED: * User is not able to see the content of 'My Account' menu
        EXPECTED: * User is redirected to the 'Login' page
        """
        pass
