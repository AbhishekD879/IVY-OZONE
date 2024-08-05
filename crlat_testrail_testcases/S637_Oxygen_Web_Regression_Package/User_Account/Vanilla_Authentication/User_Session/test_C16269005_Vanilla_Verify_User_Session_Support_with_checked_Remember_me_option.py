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
class Test_C16269005_Vanilla_Verify_User_Session_Support_with_checked_Remember_me_option(Common):
    """
    TR_ID: C16269005
    NAME: [Vanilla] Verify User Session Support with checked "Remember me" option
    DESCRIPTION: This test case verifies user session support for logged-in user with enabled "Remember me" option
    PRECONDITIONS: Private mode is switched off on device browser
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: The main page should be displayed
        """
        pass

    def test_002_click_login_on_the_header(self):
        """
        DESCRIPTION: Click Login on the header
        EXPECTED: 
        """
        pass

    def test_003_specify__valid_login__valid_password__tick_remember_me_checkbox(self):
        """
        DESCRIPTION: Specify:
        DESCRIPTION: - valid Login
        DESCRIPTION: - valid Password
        DESCRIPTION: - tick "Remember me" checkbox
        EXPECTED: All fields /UI controls fulfilled
        EXPECTED: ![](index.php?/attachments/get/35829)
        """
        pass

    def test_004_click_login_button(self):
        """
        DESCRIPTION: Click Login button
        EXPECTED: User Should be successfully logged in
        """
        pass

    def test_005_close_browser(self):
        """
        DESCRIPTION: Close browser
        EXPECTED: n/a
        """
        pass

    def test_006_open_browser_and_load_app_again(self):
        """
        DESCRIPTION: Open browser and load app again
        EXPECTED: user should be already logged in
        """
        pass

    def test_007_wait_for_idle_2h_or_another_predefined_session_termination_timecan_be_checked_here_envmocksconfigeg_httpqa2sportscoralcoukmocksconfig_as_vanillaframeworkwebauthentication____timeoutindexphpattachmentsget35830(self):
        """
        DESCRIPTION: Wait for idle 2h (or another predefined session termination time)
        DESCRIPTION: Can be checked here env/mocks/config
        DESCRIPTION: (e.g. http://qa2.sports.coral.co.uk/mocks/config as VanillaFramework.Web.Authentication --> timeout)
        DESCRIPTION: ![](index.php?/attachments/get/35830)
        EXPECTED: n/a
        """
        pass

    def test_008_navigate_around_the_app_after_idle_time(self):
        """
        DESCRIPTION: Navigate around the app after idle time
        EXPECTED: User session should NOT be terminated
        EXPECTED: User should be still logged in
        """
        pass
