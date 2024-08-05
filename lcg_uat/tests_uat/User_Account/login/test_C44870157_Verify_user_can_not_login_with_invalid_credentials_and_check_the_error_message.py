import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C44870157_Verify_user_can_not_login_with_invalid_credentials_and_check_the_error_message(BaseUserAccountTest):
    """
    TR_ID: C44870157
    NAME: Verify user can not login with invalid credentials and check the error message.
    PRECONDITIONS: Launch the app
    PRECONDITIONS: Login with the invalid credentials
    """
    keep_browser_open = True
    invalid_username = 'Te$t3R'
    invalid_password = 'testing123'

    def test_001_try_to_login_with_a_wrong_username_eg_try_a_weird_combination_of_characters_so_the_username_does_not_exist(self):
        """
        DESCRIPTION: Try to login with a wrong username (e.g. try a weird combination of characters so the username does not exist)
        EXPECTED: Error message is displayed
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        self.dialog.username = self.invalid_username
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        self.assertTrue(self.dialog.wait_error_message(),
                        msg='Error message did not appear!')
        self.assertEqual(self.dialog.error_message, vec.gvc.INCORRECT_PASSWORD_ERROR,
                         msg=f'Error message "{self.dialog.error_message}" is not the same as expected "{vec.gvc.INCORRECT_PASSWORD_ERROR}"')

    def test_002_try_to_login_with_a_correct_username_but_wrong_password(self):
        """
        DESCRIPTION: Try to login with a correct username but wrong password
        EXPECTED: Error message is displayed
        """
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        self.dialog.username = tests.settings.default_username
        self.dialog.password = self.invalid_password
        self.dialog.click_login()
        self.assertTrue(self.dialog.wait_error_message(),
                        msg='Error message did not appear!')
        self.assertEqual(self.dialog.error_message, vec.gvc.INCORRECT_PASSWORD_ERROR,
                         msg=f'Error message "{self.dialog.error_message}" is not the same as expected "{vec.gvc.INCORRECT_PASSWORD_ERROR}"')
