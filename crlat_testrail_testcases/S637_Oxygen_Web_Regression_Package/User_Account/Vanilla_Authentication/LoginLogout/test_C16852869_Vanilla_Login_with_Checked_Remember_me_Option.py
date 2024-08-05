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
class Test_C16852869_Vanilla_Login_with_Checked_Remember_me_Option(Common):
    """
    TR_ID: C16852869
    NAME: [Vanilla] Login with Checked "Remember me" Option
    DESCRIPTION: This Test Case verify "Remember" me Option (trChecked)
    DESCRIPTION: Update:
    DESCRIPTION: Note according to new logic from GVC:
    DESCRIPTION: 1. User will still be logged-out due to inactivity, but transparently logged-in using the remember me token.
    DESCRIPTION: 2. If the user is actively using or does something before the 2 hour window, the session will be extended.
    DESCRIPTION: 3. Remember me is valid for a year/12 months (can be configured to whatever is required), however, customer needs to be active every two hours.
    PRECONDITIONS: User should not be logged in
    """
    keep_browser_open = True

    def test_001_clicktap_on_the_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on the "Log In" button
        EXPECTED: *   "Log In" pop-up is opened
        EXPECTED: *   Username and Password fields are available
        EXPECTED: *   "Remember me" checkbox is placed under Username field and unchecked by default
        """
        pass

    def test_002_enter_valid_login_and_password_and_check_remember_me_option(self):
        """
        DESCRIPTION: Enter valid Login and Password and Check 'Remember me' option
        EXPECTED: - User is successfully logged in;
        EXPECTED: - the user must be given an extended session of <timePeriod> (c
        EXPECTED: onfigurable value which is set to <timePeriod=365 days> by default);
        """
        pass

    def test_003_kill_an_apprelaunchor_wait_2_h(self):
        """
        DESCRIPTION: Kill an app/relaunch
        DESCRIPTION: or wait 2 h
        EXPECTED: - user should be logged IN
        """
        pass
