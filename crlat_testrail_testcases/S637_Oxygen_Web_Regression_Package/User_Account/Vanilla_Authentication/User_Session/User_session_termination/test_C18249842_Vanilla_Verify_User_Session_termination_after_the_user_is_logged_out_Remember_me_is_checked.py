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
class Test_C18249842_Vanilla_Verify_User_Session_termination_after_the_user_is_logged_out_Remember_me_is_checked(Common):
    """
    TR_ID: C18249842
    NAME: [Vanilla] Verify User Session termination after the user is logged out ("Remember me" is checked)
    DESCRIPTION: This test case verifies user session  "Remember me" option is invalid after user is logged out
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

    def test_004_close_browser(self):
        """
        DESCRIPTION: Close browser
        EXPECTED: n/a
        """
        pass

    def test_005_open_browser_and_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Open browser and load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: user should be already logged in
        """
        pass

    def test_006_click_on_log_out(self):
        """
        DESCRIPTION: Click on Log Out
        EXPECTED: user should be successfully logged out
        """
        pass

    def test_007_close_browser(self):
        """
        DESCRIPTION: Close browser
        EXPECTED: n/a
        """
        pass

    def test_008_open_browser_and_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Open browser and load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: user is NOT logged in
        EXPECTED: Log In button is displayed
        """
        pass
