import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C35326493_Change_Password(Common):
    """
    TR_ID: C35326493
    NAME: Change Password
    DESCRIPTION: This test case verifies 'Change Password' functionality
    PRECONDITIONS: Choosing the password should include following rules:
    PRECONDITIONS: At least 8 characters;
    PRECONDITIONS: Uppercase and lowercase letters;
    PRECONDITIONS: Numbers and symbols
    """
    keep_browser_open = True
    blocked_hosts = ['*.google.*']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register user
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: * User is successfully logged in
        """
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_003_click_tap_on_my_account_menu_on_the_header(self):
        """
        DESCRIPTION: Click/Tap on 'My Account' Menu on the Header
        EXPECTED: 'My Account' menu is displayed
        """
        if self.device_type == 'desktop':
            self.site.header.user_panel.my_account_button.click()
        else:
            self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"My Account" menu is not displayed')

    def test_004_click_tap_on_settings_change_password_menu_item(self):
        """
        DESCRIPTION: Click/Tap on 'Settings' --> 'Change Password' menu item
        EXPECTED: 'Change Password' page is opened
        """
        settings_title = self.site.window_client_config.settings_menu_title
        settings = self.site.right_menu.items_as_ordered_dict.get(settings_title)
        self.assertTrue(settings.is_displayed(), msg='Settings link is not displayed')
        settings.click()
        result = wait_for_result(lambda: self.site.right_menu.header.title == settings_title,
                                 name='Wait for header title to change',
                                 timeout=3)
        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                        f'expected "{settings_title}"')

        change_password_link = self.site.right_menu.items_as_ordered_dict.get(self.site.window_client_config.change_password_menu_title)
        self.assertTrue(change_password_link.is_displayed(), msg='Change password link is not displayed')
        change_password_link.click()
        self.__class__.change_password = self.site.change_password
        self.assertTrue(self.change_password.is_displayed(), msg='Change password page is not displayed')

    def test_005_enter_valid_data_in_old_password_new_password_tap_on_submit_button(self):
        """
        DESCRIPTION: Enter valid data in 'Old Password', 'New Password' -> tap on 'Submit' button
        EXPECTED: Password changed successfully! message appears
        """
        self.__class__.new_pswd = 'Qwerty123'
        self.__class__.password = tests.settings.default_password
        self.change_password.old_password.input.value = self.password
        self.change_password.new_password.input.value = self.new_pswd
        self.change_password.submit_button.click()

        result = wait_for_result(lambda: self.change_password.confirm_password_changed_message == vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG,
                                 name=f'Message to appear {vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG}',
                                 timeout=2)

        self.assertTrue(result, msg=f'Actual message: "{self.change_password.confirm_password_changed_message}" '
                        f'is not "{vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG}"')

    def test_006_log_out_and_try_to_log_in_with_old_password(self):
        """
        DESCRIPTION: Log out and try to log in with old password
        EXPECTED: It is impossible to login with old password
        """
        if self.device_type == 'mobile':
            self.change_password.header.close_button.click()
        self.site.logout()
        self.site.wait_logged_out()
        self.navigate_to_page(name='/')  # for tst endpoints
        self.site.wait_content_state('HomePage')
        self.site.header.sign_in.click()
        self.site.login_dialog.username = self.username
        self.site.login_dialog.password = self.password
        self.site.login_dialog.login_button.click()
        # failure on tst2 env due to redirect to the page with capture
        self.site.login_dialog.wait_error_message()
        error_msg = self.site.login_dialog.error_message
        self.assertEqual(error_msg, vec.gvc.INCORRECT_PASSWORD_ERROR,
                         msg=f'*** Error message expected: "{vec.gvc.INCORRECT_PASSWORD_ERROR}", but was: "{error_msg}"')

    def test_007_log_in_with_new_password(self):
        """
        DESCRIPTION: Log in with new password
        EXPECTED: User is logged in
        """
        self.site.login(username=self.username, password=self.new_pswd)
