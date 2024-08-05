import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
import voltron.environments.constants as vec


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_journey_promo_1
@pytest.mark.user_journey_promo_2
@pytest.mark.user_account
@pytest.mark.user_password
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.pipelines
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C28220_C16268954_Successful_Log_In_with_Username_and_Password(BaseUserAccountTest):
    """
    TR_ID: C28220
    TR_ID: C16268954
    NAME: Successful Log In with Username and Password
    DESCRIPTION: This test case verifies successful Log In with existing credentials
    """
    keep_browser_open = True
    dialog = None
    password_type = 'password'

    def test_001_log_in_pop_up_is_displayed(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log In' pop-up is displayed
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')

    def test_002_username_is_displayed(self):
        """
        DESCRIPTION: Enter existing correct 'Username'
        EXPECTED: Username is displayed
        """
        self.dialog.username = self.username
        username = self.dialog.username
        self.assertEqual(username, self.username,
                         msg=f'Actual username "{username}" is not the same as expected "{self.username}"')

    def test_003_password_is_displayed_correctly(self):
        """
        DESCRIPTION: Enter correct corresponding 'Password'
        EXPECTED: Entered password is displayed as ******
        """
        self.dialog.password = tests.settings.default_password
        password_type = self.dialog.password.input_type
        self.assertEqual(password_type, self.password_type, msg='Password is not displayed in "*****" format')

    def test_004_user_is_logged_in_successfully(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: Log in popup is closed
        EXPECTED: User is logged in successfully
        EXPECTED: User Balance is displayed
        EXPECTED: Page from which user made log in is still shown
        """
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        try:
            self.site.close_all_dialogs(async_close=False)
        except Exception as e:
            # for some reasons exception occurs on closing one of dialogs
            self._logger.warning(e)
        self.site.wait_content_state('Homepage')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
