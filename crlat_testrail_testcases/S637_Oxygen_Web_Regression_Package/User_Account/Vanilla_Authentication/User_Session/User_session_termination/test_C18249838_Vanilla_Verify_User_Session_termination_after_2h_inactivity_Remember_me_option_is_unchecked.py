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
class Test_C18249838_Vanilla_Verify_User_Session_termination_after_2h_inactivity_Remember_me_option_is_unchecked(Common):
    """
    TR_ID: C18249838
    NAME: [Vanilla] Verify User Session termination after 2h inactivity ("Remember me" option is unchecked)
    DESCRIPTION: This test case verifies user session termination for predefine time of user inactivity. ("Remember me" option is unchecked)
    PRECONDITIONS: Private mode is switched off on device browser
    """
    keep_browser_open = True

    def test_001_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: The main page should be displayed
        """
        pass

    def test_002_specify__valid_login__valid_passwordnote_remember_me_option_should_be_unchecked(self):
        """
        DESCRIPTION: Specify:
        DESCRIPTION: - valid Login
        DESCRIPTION: - valid Password
        DESCRIPTION: Note: "Remember me" option should be unchecked
        EXPECTED: All fields fulfilled
        """
        pass

    def test_003_click_on_login(self):
        """
        DESCRIPTION: Click on Login
        EXPECTED: User Should be successfully logged in
        """
        pass

    def test_004_wait_for_idle_2h_or_another_predefined_session_termination_timecan_be_checked_here_envmocksconfigeg_httpqa2sportscoralcoukmocksconfig_as_vanillaframeworkwebauthentication____timeoutindexphpattachmentsget35830(self):
        """
        DESCRIPTION: Wait for idle 2h (or another predefined session termination time)
        DESCRIPTION: Can be checked here env/mocks/config
        DESCRIPTION: (e.g. http://qa2.sports.coral.co.uk/mocks/config as VanillaFramework.Web.Authentication --> timeout)
        DESCRIPTION: ![](index.php?/attachments/get/35830)
        EXPECTED: n/a
        """
        pass

    def test_005_go_to_another_page_eg_my_account_icon____settings__change_password(self):
        """
        DESCRIPTION: Go to another page (e.g "My Account" icon --> "Settings"--"Change Password")
        EXPECTED: user session should be terminated
        EXPECTED: user  should be Logged out
        EXPECTED: Login page with "Please log in" message should be displayed.
        EXPECTED: ![](index.php?/attachments/get/35958)
        """
        pass
