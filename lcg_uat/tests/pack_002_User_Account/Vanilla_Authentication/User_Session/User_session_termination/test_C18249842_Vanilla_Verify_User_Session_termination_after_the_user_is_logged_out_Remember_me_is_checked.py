import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C18249842_Vanilla_Verify_User_Session_termination_after_the_user_is_logged_out_Remember_me_is_checked(BaseUserAccountTest):
    """
    TR_ID: C18249842
    NAME: [Vanilla] Verify User Session termination after the user is logged out ("Remember me" is checked)
    DESCRIPTION: This test case verifies user session  "Remember me" option is invalid after user is logged out
    PRECONDITIONS: Private mode is switched off on device browser
    """
    keep_browser_open = True
    username = tests.settings.betplacement_user
    password = tests.settings.default_password

    def test_001_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: The main page should be displayed
        """
        self.site.wait_content_state("Home")

    def test_002_specify__valid_login__valid_password__tick_remember_me_checkbox(self):
        """
        DESCRIPTION: Specify:
        DESCRIPTION: - valid Login
        DESCRIPTION: - valid Password
        DESCRIPTION: - tick "Remember me" checkbox
        EXPECTED: All fields /UI controls fulfilled
        EXPECTED: ![](index.php?/attachments/get/35829)
        """
        self.site.login(username=self.username, password=self.password, remember_me=True)

    def test_003_clock_on_login(self):
        """
        DESCRIPTION: Clock on Login
        EXPECTED: User Should be successfully logged in
        """
        # Covered in Step 2

    def test_004_close_browser(self):
        """
        DESCRIPTION: Close browser
        EXPECTED: n/a
        """
        self.device.open_new_tab()
        self.device.open_tab(tab_index=0)
        self.device.close_current_tab()
        self.device.switch_to_new_tab()

    def test_005_open_browser_and_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Open browser and load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: user should be already logged in
        """
        self.device.navigate_to(tests.HOSTNAME)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')

    def test_006_click_on_log_out(self):
        """
        DESCRIPTION: Click on Log Out
        EXPECTED: user should be successfully logged out
        """
        self.site.logout()

    def test_007_close_browser(self):
        """
        DESCRIPTION: Close browser
        EXPECTED: n/a
        """
        self.test_004_close_browser()

    def test_008_open_browser_and_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Open browser and load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: user is NOT logged in
        EXPECTED: Log In button is displayed
        """
        self.device.navigate_to(tests.HOSTNAME)
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='User is logged in')
