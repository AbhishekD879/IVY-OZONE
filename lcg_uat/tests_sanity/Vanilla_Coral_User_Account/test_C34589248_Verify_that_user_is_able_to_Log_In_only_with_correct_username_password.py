import pytest
import voltron.environments.constants as vec
import tests
from time import sleep
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C34589248_Verify_that_user_is_able_to_Log_In_only_with_correct_username_password(Common):
    """
    TR_ID: C34589248
    NAME: Verify that user is able to Log In only with correct username/password
    DESCRIPTION: Verify that customers can successfully log in / log out (also check negative scenarios)
    """
    keep_browser_open = True

    def test_001_try_to_login_with_a_wrong_username(self):
        """
        DESCRIPTION: Try to login with a wrong username (e.g. try a weird combination of characters so the username does not exist)
        EXPECTED: Error 'The credentials entered are incorrect' is displayed
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" pop up is not displayed')

        self.dialog.username = 'wrong1234'
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()

        self.assertTrue(self.dialog.wait_error_message(),
                        msg='Error message did not appear!')
        expected_error_message = vec.gvc.INCORRECT_USER_ERROR
        error_message = self.dialog.error_message
        self.assertEqual(error_message, expected_error_message,
                         msg=f'Error message "{error_message}" is not the same as expected "{expected_error_message}"')

    def test_002_try_to_login_with_a_correct_username_but_wrong_password(self):
        """
        DESCRIPTION: Try to login with a correct username but wrong password
        EXPECTED: Error 'The credentials entered are incorrect' is displayed
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = 'wrong'
        self.dialog.click_login()
        self.assertTrue(self.dialog.wait_error_message(),
                        msg='Error message did not appear!')
        expected_error_message = vec.gvc.INCORRECT_PASSWORD_ERROR
        error_message_status = wait_for_result(lambda: self.dialog.error_message == expected_error_message, name = "waiting for the error message on login dialoge to match the expected error message", timeout=10)
        self.assertTrue(error_message_status, msg=f'Error message "{self.dialog.error_message}" is not the same as expected "{expected_error_message}"')

    def test_003_try_to_login_with_correct_username_and_password(self):
        """
        DESCRIPTION: Try to login with correct username and password
        EXPECTED: The customer is successfully logged in. Balance is displayed
        """
        self.assertTrue(self.dialog.username_field.is_enabled(timeout=5),
                        msg='Username field is not enabled!')
        sleep(3)
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        self.assertTrue(self.dialog.wait_dialog_closed(), msg='Login dialog is not closed.')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in.')
        self.assertNotEquals(self.site.header.user_balance, '',
                             msg='User balance is not displayed.')
        self.site.close_all_dialogs(async_close=False)

    def test_004_click_on_menu___logout(self):
        """
        DESCRIPTION: Click on Menu -> Logout
        EXPECTED: The customer is logged out
        """
        if self.site.root_app.has_timeline_overlay_tutorial(timeout=2, expected_result=True):
            self.site.timeline_tutorial_overlay.close_icon.click()
        self.site.header.user_panel.my_account_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Account menu is not opened.')
        self.site.right_menu.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out.')
