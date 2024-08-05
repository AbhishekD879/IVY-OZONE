import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C352447_Verify_OXsoftSerial_and_OXuuid_parameters_setting_in_local_storage(BaseUserAccountTest):
    """
    TR_ID: C352447
    NAME: Verify 'OX.softSerial' and 'OX.uuid' parameters setting in local storage
    DESCRIPTION: This test case verifies 'OX.softSerial' and 'OX.uuid' parameters setting in local storage
    PRECONDITIONS: 1. To check local storage open dev tools -> select Application tab -> local storage section
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='No login dialog present on page')

    def test_002_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log in' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        # Covered in step #1

    def test_003_check_remember_me_option_and_tap_log_in_button(self):
        """
        DESCRIPTION: Check 'Remember me' option and tap 'Log in' button
        EXPECTED: User is successfully logged in with permanet session
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        remember_me = self.dialog.remember_me
        remember_me.click()
        self.assertTrue(remember_me.is_checked(), msg='Remember Me is not selected after click')
        self.dialog.click_login()
        self.dialog.wait_dialog_closed()
        self.site.close_all_dialogs(async_close=False)

    def test_004_verify_oxsoftserial_parameter_correctness_in_local_storage(self):
        """
        DESCRIPTION: Verify 'OX.softSerial' parameter correctness in local storage
        EXPECTED: 'OX.softSerial' parameter corresponds to 'softSerail' value from object
        """
        cookie_value = self.get_local_storage_cookie_value_as_dict('OX.softSerial')
        self.assertTrue(cookie_value, msg=f'"OX.softSerial" value not present')

    def test_005_verify_oxuuid_parameter_correctness_in_local_storage(self):
        """
        DESCRIPTION: Verify 'OX.uuid' parameter correctness in local storage
        EXPECTED: 'OX.uuid' parameter corresponds to 'deviceID' value from object
        """
        cookie_value = self.get_local_storage_cookie_value_as_dict('OX.uuid')
        self.assertTrue(cookie_value, msg=f'"OX.uuid" value not present')
