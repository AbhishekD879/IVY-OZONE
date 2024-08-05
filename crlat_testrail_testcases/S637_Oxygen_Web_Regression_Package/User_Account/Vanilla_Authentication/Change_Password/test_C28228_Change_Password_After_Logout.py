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
class Test_C28228_Change_Password_After_Logout(Common):
    """
    TR_ID: C28228
    NAME: Change Password After Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: User is still able to navigate between pages and to see the content, however he is not able to do actions which are related to his/her account
    PRECONDITIONS: **Choosing the password should include following rules:**
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to Oxygen app in one browser tab -> open 'Change password' via 'My Account'
    PRECONDITIONS: *   Login to Oxygen app in second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_repeat_steps_from_preconditions(self):
        """
        DESCRIPTION: Repeat steps from Preconditions
        EXPECTED: 
        """
        pass

    def test_002_verify_change_password_page(self):
        """
        DESCRIPTION: Verify 'Change Password' page
        EXPECTED: Popup message appears **"You have been logged out."**
        EXPECTED: User is logged out from the application automatically without performing any actions
        EXPECTED: User is not able to see the content of '**Change Password**' page
        EXPECTED: User is redirected to the Homepage
        """
        pass
