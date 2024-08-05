import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C2745941_STG2HLVerify_Login_functionality_during_Time_Out_period_set_by_User(Common):
    """
    TR_ID: C2745941
    NAME: [STG2][HL]Verify 'Login' functionality during Time-Out period set by User
    DESCRIPTION: This test case verifies 'Login' functionality during Time-Out period set by User
    PRECONDITIONS: * Oxygen app is loaded
    PRECONDITIONS: * The user is logged out
    PRECONDITIONS: * User account has set Time-Out period
    PRECONDITIONS: * Click/Tap on 'Log In' button for opening 'Login' pop-up
    PRECONDITIONS: *Note:*
    PRECONDITIONS: Execute the next test case https://ladbrokescoral.testrail.com/index.php?/cases/view/2696885 for triggering Time-Out for User account.
    """
    keep_browser_open = True

    def test_001_enter_username_and_password_for_user_from_preconditions(self):
        """
        DESCRIPTION: Enter username and password for user from preconditions
        EXPECTED: * Entered characters are displayed inside fields
        EXPECTED: * 'Log In' button becomes active
        """
        pass

    def test_002_clicktap_log_in_button(self):
        """
        DESCRIPTION: Click/Tap 'Log In' button
        EXPECTED: The error message "Sorry, the action cannot be performed because you have asked to be timed-out from playing. You can come back and play after yyyy-mm-dd hh:mm:ss" appears at the top of pop-up
        EXPECTED: * yyyy-mm-dd hh:mm:ss - time-out expiration date
        """
        pass

    def test_003_compare_time_out_expiration_date_on_login_pop_up_and_during_setting_it_by_the_user_in_time_out_journey(self):
        """
        DESCRIPTION: Compare time-out expiration date on 'Login' pop up and during setting it by the user in time-out journey
        EXPECTED: The time-out expiration date is equal to date and time that were chosen by the user during time-out journey
        """
        pass
