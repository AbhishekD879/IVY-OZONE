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
class Test_C2807969_Verify_login_reactivation_pop_up(Common):
    """
    TR_ID: C2807969
    NAME: Verify login reactivation pop up
    DESCRIPTION: This test case verifies on login Reactivation pop up
    DESCRIPTION: AUTOTEST [C9240749]
    PRECONDITIONS: * User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item -> Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: * Player Tag 'Account_Closed_By_Player' is set to 'True' in IMS
    PRECONDITIONS: * Player Tag 'On_login_Account_Closed_Message' is set in IMS
    PRECONDITIONS: * 'Reactivation' Log in message is created with the tag 'On_login_Account_Closed_Message' in IMS
    PRECONDITIONS: * The login pop up is set within IMS - configuration instructions can be found here https://drive.google.com/drive/u/2/folders/1pkGIbDBUp2rU_iWXh1ve18W0mwK71VMU
    """
    keep_browser_open = True

    def test_001__log_in_verify_availability_of_on_log_reactivation_pop_up(self):
        """
        DESCRIPTION: * Log in
        DESCRIPTION: * Verify availability of on log ‘Reactivation’ pop up
        EXPECTED: * Property 'Get Player Tags'= name: 'On_login_Account_Closed_Message' is available in openApi WS response with ID: 35548
        EXPECTED: * On login Reactivation pop up consist of:
        EXPECTED: **Reactivation text:**
        EXPECTED: 'Your account is closed therefore you will not be able to deposit funds or place bets.
        EXPECTED: If you wish to reactivate your account, go to Reactivation page and follow the instructions.'
        EXPECTED: **Reactivation url**
        """
        pass

    def test_002_close_the_pop_up(self):
        """
        DESCRIPTION: Close the pop up
        EXPECTED: * Pop up is closed
        EXPECTED: * User is logged in remaining on home page
        """
        pass

    def test_003_log_out_then_log_in_with_the_same_user(self):
        """
        DESCRIPTION: Log out then log in with the same user
        EXPECTED: Reactivation pop up is displayed
        """
        pass

    def test_004_log_out_then_log_in_with_an_active_user(self):
        """
        DESCRIPTION: Log out then log in with an active user
        EXPECTED: Reactivation pop up is not displayed
        """
        pass
