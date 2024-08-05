import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C631550_Login_with_unfrozen_account(Common):
    """
    TR_ID: C631550
    NAME: Login with unfrozen account
    DESCRIPTION: This test case verifies login with user with unfrozen account
    PRECONDITIONS: * Oxygen application is loaded
    PRECONDITIONS: * User has account that was unfrozen
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To freeze (self-exclude) account navigate to My Account -> Responsible Gambling -> Self Exclusion
    PRECONDITIONS: * To unfreeze account contact UAT
    """
    keep_browser_open = True

    def test_001_click_log_in_button(self):
        """
        DESCRIPTION: Click 'LOG IN' button
        EXPECTED: 'Log In' pop up is shown
        """
        pass

    def test_002_enter_credentials_of_unfrozen_account_and_click_log_in_button(self):
        """
        DESCRIPTION: Enter credentials of unfrozen account and click 'Log In' button
        EXPECTED: * User is logged in
        EXPECTED: * Self Exclusion pop up is NOT shown
        """
        pass
