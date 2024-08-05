import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.user_account
@pytest.mark.login
@pytest.mark.desktop
@vtest
class Test_C15785353_Vanilla_User_is_logged_out_in_case_of_error_happening(Common):
    """
    TR_ID: C15785353
    NAME: [Vanilla] User is logged out in case of error happening
    DESCRIPTION: This test case verifies that user is logged out by the server automatically in case of error happening
    PRECONDITIONS: User is logged out in case:
    PRECONDITIONS: - **this.authService.isAuthenticated** is failed
    PRECONDITIONS: - **this.api.get('temporarytoken')** is failed
    """
    keep_browser_open = True
    cookie_name = 'OX.USER'
    cookie_parameter = 'bppToken'

    def verify_logged_out_state(self, timeout=90):
        """
        For tests that are verifying app behaviour after logout in separate tab
        Means that user's session is over on the server.
        """
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=timeout)
        self.assertTrue(dialog, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog is not shown')
        actual_error = dialog.error_message
        self.assertEqual(actual_error, vec.gvc.SESSION_EXPIRED_DIALOG_TITLE,
                         msg=f'Actual error "{actual_error}" != Expected "{vec.gvc.SESSION_EXPIRED_DIALOG_TITLE}"')
        dialog.close_dialog()
        dialog_closed = dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg=f'{vec.dialogs.DIALOG_MANAGER_LOG_IN} dialog was not closed')

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is successfully logged in
        """
        self.site.login()

    def test_002_open_separate_tab_in_the_browser_load_oxygen_app_and_log_in_there_with_the_same_credentials(self):
        """
        DESCRIPTION: Open separate tab in the browser, load oxygen app and log in there with the same credentials
        EXPECTED: User is already logged in
        """
        self.device.open_new_tab()
        self.device.switch_to_new_tab()
        self.device.navigate_to(tests.HOSTNAME)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')

    def test_003_log_out_from_one_of_opened_tabs(self):
        """
        DESCRIPTION: Log out from one of opened tabs
        EXPECTED: Session is over on the server side
        """
        self.site.logout(timeout=20)

    def test_004_go_to_another_tab(self):
        """
        DESCRIPTION: Go to another tab
        EXPECTED: Ladbrokes:
        EXPECTED: - User is logged out after page refresh
        EXPECTED: - 'Log out' pop-up shouldn't be displayed
        EXPECTED: Coral:
        EXPECTED: - User is logged out after page refresh
        EXPECTED: - 'Log out' pop-up is displayed
        """
        self.device.open_tab(tab_index=0)
        self.verify_logged_out_state()

    def test_005_log_in_again(self):
        """
        DESCRIPTION: Log in again
        EXPECTED: User is successfully logged in
        """
        self.site.login()

    def test_006_open_application_tab___cookies___delete_vauthnetwork_tab___offline___online(self):
        """
        DESCRIPTION: Open Application tab -> Cookies -> delete 'vauth'
        DESCRIPTION: Network tab -> Offline -> Online
        EXPECTED: - User is logged out
        EXPECTED: - 'Log out' pop-up is displayed
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.refresh_page()
        self.site.wait_content_state('homepage')

    def test_007_log_in_again(self):
        """
        DESCRIPTION: Log in again
        EXPECTED: User is successfully logged in
        """
        self.site.login()

    def test_008_in_dev_tools___application___local_storage_select_app_url(self):
        """
        DESCRIPTION: In Dev Tools -> Application -> Local Storage select app url
        """
        # Covered into step 9

    def test_009_for_oxuser_parameter_change_bpptoken_value_and_save_changes(self):
        """
        DESCRIPTION: For OX.USER parameter change bppToken": value and save changes
        """
        cookie_value = self.get_local_storage_cookie_value_as_dict(cookie_name=self.cookie_name)
        self._logger.debug(f'OX.USER cookie value before change "{cookie_value}"')
        self.assertTrue(cookie_value, msg='Error retrieving cookie value')

        cookie_value[self.cookie_parameter] = '123'
        self.device.set_local_storage_cookies(ls_cookies_dict={self.cookie_name: cookie_value})

        cookie_value = self.get_local_storage_cookie_value(cookie_name=self.cookie_name)
        self._logger.debug(f'OX.USER cookie value after change "{cookie_value}"')
        self.assertTrue(cookie_value, msg='Error retrieving cookie value')

    def test_010_in_application_refresh_the_page_and_verify_that_user_is_still_logged_in(self):
        """
        DESCRIPTION: In application refresh the page and verify that user is still logged in
        EXPECTED: User is still logged in to application
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_logged_in()
