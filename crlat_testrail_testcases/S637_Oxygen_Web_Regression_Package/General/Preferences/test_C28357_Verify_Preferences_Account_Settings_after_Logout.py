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
class Test_C28357_Verify_Preferences_Account_Settings_after_Logout(Common):
    """
    TR_ID: C28357
    NAME: Verify Preferences/Account Settings after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: **Jira tickets:** BMA-5678 (Handle HTTP Error 401)
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to one browser tab and open 'Bet History' page
    PRECONDITIONS: *   Login to second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_verify_settings_page(self):
        """
        DESCRIPTION: Verify 'Settings' page
        EXPECTED: - User is logged out from the application automatically without performing any actions
        EXPECTED: - Log in pop-up message  about logging out 'Your session expired. Please log in again.' appears
        EXPECTED: **CORAL**
        EXPECTED: ![](index.php?/attachments/get/115467297)
        EXPECTED: **LADBROKES**
        EXPECTED: ![](index.php?/attachments/get/115467298)
        EXPECTED: - User is not able to see the content of '**Settings**' page
        """
        pass
