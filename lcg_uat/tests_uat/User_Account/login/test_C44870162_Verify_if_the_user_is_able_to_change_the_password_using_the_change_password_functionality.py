import re
import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from time import sleep
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.p2
@pytest.mark.user_account
@vtest
class Test_C44870162_Verify_if_the_user_is_able_to_change_the_password_using_the_change_password_functionality(Common):
    """
    TR_ID: C44870162
    NAME: Verify if the user is able to change the password using the 'change password'  functionality
    """
    keep_browser_open = True
    old_password = tests.settings.default_password
    new_password = 'Vikas123'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register user
        DESCRIPTION: User is logged into an app
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('HomePage')

    def test_001_load_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Load https://beta-sports.coral.co.uk/
        """
        # covered in next step

    def test_002_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
        EXPECTED: User is successfully logged in
        EXPECTED: Home page is opened in case if user has positive amount of his/her balance
        EXPECTED: Low Balance message is shown to the user if balance is equal to 0 (Not Applicable for Ladbrokes)
        """
        self.site.header.sign_in.click()
        self.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        self.dialog.username = self.username
        self.dialog.password = self.old_password
        self.dialog.click_login()
        if self.brand == 'bma':
            self.assertTrue(self.site.has_low_balance(), msg='low balance msg is not shown')
        sleep(5)
        try:
            self.site.close_all_dialogs(timeout=5)
            dialog_appeared = True
        except Exception:
            dialog_appeared = False
        if self.device_type == 'mobile' and self.site.root_app.has_timeline_overlay_tutorial():
            self.site.timeline_tutorial_overlay.close_icon.click()
        if not dialog_appeared:
            self.site.close_all_dialogs(timeout=5)

    def test_003_click_on_the_avatar__settings__change_password(self):
        """
        DESCRIPTION: Click on the Avatar > Settings > Change password
        EXPECTED: 'Change Password' page is opened
        """
        wait_for_result(lambda: self.site.header.right_menu_button.is_displayed(),
                        name='right_menu_button button to appear',
                        timeout=3)
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right-Menu')
        self.site.right_menu.click_item('Settings')
        if self.device_type == 'mobile':
            self.site.wait_splash_to_hide(7)
            sleep(2)
            self.site.right_menu.click_item(item_name='Change Password')
        sleep(7)
        actual_url = self.device.get_current_url()
        expected_url = re.sub(r"beta2|beta3", "beta", ("https://" + tests.HOSTNAME + "/en/mobileportal/changepassword"))
        expected_url_beta2 = re.sub(r"beta2|beta3", "beta2", ("https://" + tests.HOSTNAME + "/en/mobileportal/changepassword"))
        expected_url_beta3 = re.sub(r"beta2|beta3", "beta3", ("https://" + tests.HOSTNAME + "/en/mobileportal/changepassword"))
        if 'beta2' in tests.HOSTNAME:
            self.assertIn(actual_url, [expected_url, expected_url_beta2],
                          msg=f'Actual url: "{actual_url}" is not same as Expected url: "{[expected_url, expected_url_beta2]}"')
        elif 'beta3' in tests.HOSTNAME:
            self.assertIn(actual_url, [expected_url, expected_url_beta3],
                          msg=f'Actual url: "{actual_url}" is not same as Expected url: "{[expected_url, expected_url_beta3]}"')
        else:
            self.assertEqual(actual_url, expected_url,
                             msg=f'Actual url: "{actual_url}" is not same as Expected url: "{expected_url}"')

    def test_004_enter_valid_data_in_old_password_new_password_and_tapclick_on_submit_button(self):
        """
        DESCRIPTION: Enter valid data in 'Old Password', 'New Password' and tap/click on 'Submit' button
        EXPECTED: Confirmation message appears under the header ("Password changed successfully!!")
        EXPECTED: Password is changed
        EXPECTED: User is still logged in
        """
        self.change_pass = self.site.change_password
        self.change_pass.old_password.input.value = self.old_password
        self.change_pass.new_password.input.value = self.new_password
        self.change_pass.submit_button.click()
        sleep(5)
        successful_msg = self.change_pass.confirm_password_changed_message
        self.assertEqual(successful_msg, vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG,
                         msg=f'successful message "{successful_msg}"is not the same as '
                             f'expected "{vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG}"')

    def test_005_log_out_and_login_again_with_new_password(self):
        """
        DESCRIPTION: Log out and login again with new password
        EXPECTED: User is logged in with new password
        """
        self.navigate_to_page('HomePage')
        self.site.wait_content_state('homepage')
        self.site.logout()
        self.site.login(self.username, self.new_password)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')

    def test_006_log_out_and_try_to_log_in_with_old_password(self):
        """
        DESCRIPTION: Log out and try to log in with old password
        EXPECTED: It is impossible to login with old password
        """
        self.site.logout()
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        self.site.wait_splash_to_hide(5)
        self.dialog.username = self.username
        self.dialog.password = self.old_password
        self.dialog.click_login()
        self.site.wait_splash_to_hide(3)
        error_message = self.dialog.error_message
        self.assertEqual(error_message, vec.gvc.INCORRECT_PASSWORD_ERROR,
                         msg=f'Error message "{error_message}" is not the same as expected "{vec.gvc.INCORRECT_PASSWORD_ERROR}"')

    def test_007_log_in_with_new_password(self):
        """
        DESCRIPTION: Log in with new password
        EXPECTED: User is logged in
        """
        self.dialog.password = self.new_password
        self.dialog.click_login()
        self.site.wait_content_state('HomePage')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
