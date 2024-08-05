import pytest
import tests
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.critical
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1621')
@vtest
class Test_C16673861_Vanilla_Change_My_Password(Common):
    """
    TR_ID: C16673861
    NAME: [Vanilla] Change My Password
    DESCRIPTION: This test case verifies 'Change Password' functionality
    PRECONDITIONS: Choosing the password should include following rules:
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True
    password = tests.settings.default_password
    new_pswd = 'Qwerty123'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register user
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username

    def test_001_load_home_page(self):
        """
        DESCRIPTION: Load Home page
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=self.username)

    def test_003_click_tap_on_my_account_menu_on_the_upper_right_side_of_the_page(self):
        """
        DESCRIPTION: Click/Tap on "My Account" Menu on the upper right side of the page
        EXPECTED: "My Account" menu is displayed
        """
        if self.device_type == 'desktop':
            self.site.header.user_panel.my_account_button.click()
        else:
            self.site.header.right_menu_button.click()

    def test_004_click_tap_on_settings_change_password_menu_on_the_item(self):
        """
        DESCRIPTION: Click/Tap on **'Settings'** --> "**'Change Password'**" menu on the item
        EXPECTED: "**'Change Password'**" page is opened
        """
        settings_title = self.site.window_client_config.settings_menu_title
        settings = self.site.right_menu.items_as_ordered_dict.get(settings_title)
        self.assertTrue(settings.is_displayed(), msg='Settings link is not displayed')
        settings.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='Right menu is not displayed')
        result = wait_for_result(lambda: self.site.right_menu.header.title == settings_title,
                                 name='Wait for header title to change',
                                 timeout=3)
        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                        f'expected "{settings_title}"')
        self.__class__.change_password_link = self.site.right_menu.items_as_ordered_dict.get(self.site.window_client_config.change_password_menu_title)
        self.assertTrue(self.change_password_link.is_displayed(), msg='Change password link is not displayed')
        self.change_password_link.click()
        self.__class__.change_password = self.site.change_password
        self.assertTrue(self.change_password.is_displayed(), msg='Change password page is not displayed')

    def test_005_verify_change_password_page(self):
        """
        DESCRIPTION: Verify 'Change Password' page
        EXPECTED: 'Change password' page consists of the following:
        EXPECTED: 1.  Page title is **'CHANGE PASSWORD'**
        EXPECTED: 2.  Back button near title (left side)
        EXPECTED: 3.  Close button in the upper right corner
        EXPECTED: 4.  **'Old Password', 'New Password' fields
        EXPECTED: 5.  Show Password icon for each field
        """
        if self.device_type == 'mobile':
            title = self.change_password.header.title.name
            self.assertEqual(title, self.site.window_client_config.change_password_menu_title,
                             msg=f'Title expected: "{self.site.window_client_config.change_password_menu_title}", but was: "{title}"')
            self.assertTrue(self.change_password.header.back_button.is_displayed(),
                            msg='Back button is not displayed')
            self.assertTrue(self.change_password.header.close_button.is_displayed(),
                            msg='Close button is not displayed')
        self.assertTrue(self.change_password.old_password.is_displayed(),
                        msg='Old password field is not displayed')
        self.assertTrue(self.change_password.new_password.is_displayed(),
                        msg='New password field is not displayed')
        self.assertTrue(self.change_password.new_password.toggle_icon_button.is_displayed(),
                        msg='Show new password icon is not displayed')
        self.assertTrue(self.change_password.old_password.toggle_icon_button.is_displayed(),
                        msg='Show old password icon is not displayed')

    def test_006_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User gets back to previous page ("Settings" page )
        """
        if self.device_type == 'mobile':
            self.change_password.header.back_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='Right menu is not displayed')

    def test_007_click_on_change_password_again_enter_valid_data_in_old_password_new_password_tap_on_submit_button(self):
        """
        DESCRIPTION: Click on 'Change Password' again
        DESCRIPTION: Enter valid data in 'Old Password', 'New Password' -> tap on 'Submit' button
        EXPECTED: 1.  Field validation message should appear while entering NewPassword
        EXPECTED: 2.  Password changed successfully! message appears
        EXPECTED: 3.  'Change Password' form remains opened
        EXPECTED: 4.  All fields are cleared
        """
        if self.device_type == 'mobile':
            self.__class__.change_password_link = self.site.right_menu.items_as_ordered_dict.get(self.site.window_client_config.change_password_menu_title)
            self.change_password_link.click()
        self.__class__.change_password = self.site.change_password
        self.change_password.old_password.input.value = self.password
        self.change_password.new_password.input.value = self.new_pswd
        self.assertTrue(self.change_password.submit_button.is_enabled(), msg='Submit button is not enabled.')
        self.change_password.submit_button.click()
        result = wait_for_result(
            lambda: self.change_password.confirm_password_changed_message == vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG,
            timeout=20)
        self.assertTrue(result, msg=f'"{vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG}" is not displayed')
        self.assertTrue(self.change_password.is_displayed(), msg='Change password page is not displayed')
        self.assertFalse(self.change_password.old_password.input.value,
                         msg=f'Old password field value expected to be empty but it was: '
                             f'"{self.change_password.old_password.input.value}"')
        self.assertFalse(self.change_password.new_password.input.value,
                         msg=f'New password field value expected to be empty but it was: '
                             f'"{self.change_password.new_password.input.value}"')

    def test_008_log_out_try_to_log_in_with_old_password(self):
        """
        DESCRIPTION: Log out -> try to log in with old password
        EXPECTED: It is impossible to login with old password
        """
        self.navigate_to_page('logout')
        self.site.wait_content_state(state_name='HomePage')
        self.site.header.sign_in.click()
        login_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(login_dialog, msg='Login dialog is not displayed')
        login_dialog.username = self.username
        login_dialog.password = self.password
        login_dialog.login_button.click()
        login_dialog.wait_error_message()
        error_msg = login_dialog.error_message
        self.assertEqual(error_msg, vec.gvc.INCORRECT_PASSWORD_ERROR,
                         msg=f'Error message expected: "{vec.gvc.INCORRECT_PASSWORD_ERROR}", but was: "{error_msg}"')

    def test_009_log_in_with_new_password(self):
        """
        DESCRIPTION: Log in with new password
        EXPECTED: User is logged in successfully with new password
        """
        self.site.login(username=self.username, password=self.new_pswd, timeout_wait_for_dialog=2)
