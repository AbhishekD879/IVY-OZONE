import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.login
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@pytest.mark.safari
@vtest
class Test_C28230_C16268960_Show_Password_Option(Common):
    """
    TR_ID: C28230
    TR_ID: C16268960
    NAME: Show Password Option
    DESCRIPTION: This test case verifies 'Show password' option
    """
    keep_browser_open = True
    password = tests.settings.default_password

    def test_001_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log in' button
        EXPECTED: *   'Log In' pop-up appears
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)

        self.assertTrue(self.dialog, msg='"Log In" dialog is not shown')

    def test_002_verify_show_button_icon(self):
        """
        DESCRIPTION: Verify 'Show' button/icon
        EXPECTED: 'Show' button is shown on the right side after the 'Password' field for **Mobile/Tablet**
        EXPECTED: 'Show' icon is shown within Password input field for **Desktop**
        """
        self.assertTrue(self.dialog.password.show_button.is_displayed(), msg='"Show" button is not shown')

    def test_003_fill_in_username_and_password_fields_with_valid_login_and_password(self):
        """
        DESCRIPTION: Fill in 'Username' and 'Password' fields with valid login and password
        EXPECTED: *   Valid login and password are entered
        EXPECTED: *   Password is hidden from user, displaying dots
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = self.password

        self.assertEqual(self.dialog.password.input_type, 'password', msg='Password is not hidden from user')

    def test_004_tap_on_show_button_icon(self):
        """
        DESCRIPTION: Tap on 'Show' button/icon
        EXPECTED: *   'Show' inscription changes by 'Hide' on button/icon
        EXPECTED: *   Password is not hidden anymore
        EXPECTED: *   User is able to see characters typed in 'Password' field
        """
        self.dialog.password.show_button.click()
        self.assertTrue(self.dialog.password.hide_button.is_displayed(), msg='"Hide" button is not shown')

        self.assertEqual(self.dialog.password.input_type, 'text', msg='Password still hidden from user')

    def test_005_verify_correctness_of_password(self):
        """
        DESCRIPTION: Verify correctness of password
        EXPECTED: Displayed password corresponds to password entered on step #4
        """
        self.assertEqual(self.dialog.password.input_value, self.password,
                         msg='Displayed password "%s" is not the same as expected "%s"' %
                             (self.dialog.password.input_value, self.password))

    def test_006_click_tap_on_hide_button_icon(self):
        """
        DESCRIPTION: Click/Tap on 'Hide' button/icon
        EXPECTED: *   'Hide' inscription changes by 'Show' on button/icon
        EXPECTED: *   Password is hidden from user again
        """
        self.dialog.password.hide_button.click()
        self.assertTrue(self.dialog.password.show_button.is_displayed(), msg='"Show" button is not shown')

        self.assertEqual(self.dialog.password.input_type, 'password', msg='Password is not hidden from user')
