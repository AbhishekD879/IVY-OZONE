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
class Test_C18249843_Vanilla_Verify_User_Session_termination_message(Common):
    """
    TR_ID: C18249843
    NAME: [Vanilla] Verify User Session termination message
    DESCRIPTION: This test case verifies user session termination message
    PRECONDITIONS: Private mode is switched off on device browser
    """
    keep_browser_open = True

    def test_001_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: The main page should be displayed
        """
        pass

    def test_002_specify__valid_login__valid_password__tick_remember_me_checkbox(self):
        """
        DESCRIPTION: Specify:
        DESCRIPTION: - valid Login
        DESCRIPTION: - valid Password
        DESCRIPTION: - tick "Remember me" checkbox
        EXPECTED: All fields /UI controls fulfilled
        EXPECTED: ![](index.php?/attachments/get/35829)
        """
        pass

    def test_003_clock_on_login(self):
        """
        DESCRIPTION: Clock on Login
        EXPECTED: User Should be successfully logged in
        """
        pass

    def test_004_open_new_window_and_go_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Open new window and go to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: The main page should be displayed
        EXPECTED: User should be logged in
        """
        pass

    def test_005_click_on_myaccount____logout(self):
        """
        DESCRIPTION: Click on MyAccount --> Logout
        EXPECTED: User should be logged out
        """
        pass

    def test_006_close_window_and_back_to_previous_one_step_3(self):
        """
        DESCRIPTION: Close window and Back to previous one (Step 3)
        EXPECTED: user session should be terminated
        EXPECTED: user  should NOT be Logged in
        """
        pass
