import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
import voltron.environments.constants as vec


@pytest.mark.prod
@pytest.mark.tst
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.user_account
@pytest.mark.remember_me
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C16852869_Vanilla_Login_with_Checked_Remember_me_Option(BaseUserAccountTest):
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
    dialog = None

    def test_001_tap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on the "Log In" button
        EXPECTED: *   "Log In" pop-up is opened
        EXPECTED: *   Username and Password fields are available
        EXPECTED: *   "Remember me" checkbox is placed under Username field and unchecked by default
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='No login dialog present on page')
        self.assertFalse(self.dialog.remember_me.is_checked(expected_result=False), msg='Remember Me is not unchecked by default')

    def test_002_enter_valid_login_and_password_and_check_remember_me_option(self):
        """
        DESCRIPTION: Enter valid Login and Password and Check 'Remember me' option
        EXPECTED: - User is successfully logged in;
        EXPECTED: - the user must be given an extended session of <timePeriod> (c
        EXPECTED: onfigurable value which is set to <timePeriod=365 days> by default);
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        remember_me = self.dialog.remember_me
        remember_me.click()
        self.assertTrue(remember_me.is_checked(), msg='Remember Me is not selected after click')
        self.dialog.click_login()
        self.dialog.wait_dialog_closed()
        self.site.close_all_dialogs(async_close=False)

    def test_003_kill_an_app_relaunch(self):
        """
        DESCRIPTION: Kill an app/relaunch
        DESCRIPTION: or wait 2 h
        DESCRIPTION: (or another period of time according to http://qa2.sports.coral.co.uk/mocks/config [VanillaFramework.Web.Authentication Timeout])
        EXPECTED: - user should be logged IN
        """
        self.device.open_new_tab()
        self.device.switch_to_new_tab()
        self.device.close_current_tab()
        tabs = self.device.driver.window_handles
        self.device.driver.switch_to.window(tabs[0])
        self.device.navigate_to(tests.HOSTNAME)
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
