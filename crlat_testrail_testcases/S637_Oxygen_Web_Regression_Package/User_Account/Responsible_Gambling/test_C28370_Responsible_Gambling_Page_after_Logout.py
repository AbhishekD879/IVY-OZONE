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
class Test_C28370_Responsible_Gambling_Page_after_Logout(Common):
    """
    TR_ID: C28370
    NAME: 'Responsible Gambling' Page after Logout
    DESCRIPTION: This test case verifies that user is logged out by server automatically when his/her session is over on the server.
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen in one browser tab -> open 'Responsible Gambling' page
    PRECONDITIONS: *   Login to Oxygen in second browser tab, log out -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_002_verify_responsible_gambling_page(self):
        """
        DESCRIPTION: Verify 'Responsible Gambling' page
        EXPECTED: * Popup message about logging out appears.
        EXPECTED: * User is logged out from the application automatically without performing any actions
        EXPECTED: * User is not able to see the content of 'Responsible Gambling' page
        EXPECTED: * User is redirected to the Homepage
        """
        pass
