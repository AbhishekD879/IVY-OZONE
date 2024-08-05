import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.mobile
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870155_Verify_user_journey_with_valid_credentials(BaseUserAccountTest):
    """
    TR_ID: C44870155
    NAME: Verify user journey with valid credentials
    """
    keep_browser_open = True

    def test_001_clicktap_log_in_button(self):
        """
        DESCRIPTION: Click/Tap 'Log in' button
        EXPECTED: 'Log in' pop-up is present
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')

    def test_002_enter_valid_credentials__and_tap_log_in_button(self):
        """
        DESCRIPTION: Enter valid credentials  and tap 'Log in' button
        EXPECTED: User is logged in with permanent session
        """
        self.dialog.username = tests.settings.default_username
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed(timeout=20)
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        try:
            self.site.close_all_dialogs(async_close=False)
        except Exception as e:
            self._logger.warning(e)
        self.site.wait_content_state('Homepage')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
