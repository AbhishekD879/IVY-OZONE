import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.Common import Common


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C16425274_Vanilla_Log_in_with_new_created_user(Common):
    """
    TR_ID: C16425274
    NAME: [Vanilla] Log in with new created user
    DESCRIPTION: This test case verifies that it is possible to log in using new registered user's data
    PRECONDITIONS: Register new user. Make sure you remembered entered username and password.
    PRECONDITIONS: Choosing the password should include following rules:
    PRECONDITIONS: - A letter
    PRECONDITIONS: - A number
    PRECONDITIONS: - 6 to 20 characters
    PRECONDITIONS: - Must not contain parts of your name or e-mail
    PRECONDITIONS: - Must not contain any of these special characters (‘ “ < > & % )
    PRECONDITIONS: Do not make deposit on the last step of registration.
    """
    keep_browser_open = True

    def test_001_load_vanilla_application(self):
        """
        DESCRIPTION: Load Vanilla application
        EXPECTED:
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('HomePage')

    def test_002_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' button
        EXPECTED: Log In pop-up opens
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.navigate_to(url=tests.HOSTNAME)
        self.device.driver.implicitly_wait(5)
        self.site.header.sign_in.click()
        self.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        self.dialog.username = self.username
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()

    def test_003_fill_in_username_and_password_fields_with_data_of_just_registered_user___tap_login_button(self):
        """
        DESCRIPTION: Fill in 'Username' and 'Password' fields with data of just registered user -> Tap 'Login' button
        EXPECTED: - Logging in passed successfully.
        EXPECTED: - "Low balance
        EXPECTED: Your account balance is £0.00. Would you like to deposit?"
        EXPECTED: message is displayed at the bottom.
        """
        self.assertTrue(self.site.has_low_balance(), msg='low balance msg is not shown')
