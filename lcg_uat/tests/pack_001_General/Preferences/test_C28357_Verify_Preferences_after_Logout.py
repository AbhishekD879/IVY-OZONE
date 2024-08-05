import pytest

from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.portal_only_test
@pytest.mark.user_account
@pytest.mark.preferences
@pytest.mark.low
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28357_Verify_Preferences_after_Logout(BaseUserAccountTest):
    """
    TR_ID: C28357
    NAME: Verify Preferences/Account Settings after Logout
    DESCRIPTION: This test scenario verifies that user is logged out by server automatically when his/her session is over on the server.
    DESCRIPTION: **Jira tickets:** BMA-5678 (Handle HTTP Error 401)
    PRECONDITIONS: User should be logged in, but session should be OVER on the server
    PRECONDITIONS: To trigger event when session is over on the server please perform the following steps:
    PRECONDITIONS: *   Login to one browser tab and open 'Bet History' page
    PRECONDITIONS: *   Login to second browser tab, logout -> session is over on the server
    PRECONDITIONS: *   Navigate back to the first browser tab where user is still logged in, however there is no active session already
    """
    keep_browser_open = True

    def test_001_open_right_menu_and_tap_settings(self):
        """
        DESCRIPTION: Open Right Menu and tap 'Settings'
        EXPECTED: Popup message about logging out appears.
        EXPECTED: User is logged out from the application
        EXPECTED: User is not able to see the content of '**Settings**' page
        EXPECTED: User is redirected to the Homepage
        """
        self.site.login(async_close_dialogs=False)
        self.site.navigate_to_my_account_page(name='Settings')
        self.logout_in_new_tab()
        self.verify_logged_out_state()

    def test_002_make_steps_from_preconditions(self):
        """
        DESCRIPTION: Make steps from Preconditions
        """
        self.site.login()
        self.navigate_to_page(name='bet-history')
        self.site.wait_content_state('BetHistory')
        self.logout_in_new_tab()

    def test_003_verify_settings_page(self):
        """
        DESCRIPTION: Verify 'Settings' page
        EXPECTED: User is logged out from the application automatically without performing any actions
        EXPECTED: User is not able to see the content of '**Settings**' page
        EXPECTED: User is redirected to the Homepage
        """
        self.verify_logged_out_state()
