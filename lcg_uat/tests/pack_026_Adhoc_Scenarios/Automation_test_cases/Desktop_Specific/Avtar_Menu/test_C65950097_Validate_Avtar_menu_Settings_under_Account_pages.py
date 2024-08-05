import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.avtar_menu
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65950097_Validate_Avtar_menu_Settings_under_Account_pages(Common):
    """
    TR_ID: C65950097
    NAME: Validate Avtar menu Settings under Account pages
    DESCRIPTION: This test case is to verify the Avtar menu Settings under Account pages
    PRECONDITIONS: 1.User should have vaild login credentials to log into the application
    """
    keep_browser_open = True
    old_password = tests.settings.default_password
    new_password = 'Qwerty20'

    def try_login(self, username, password, successful=True) -> bool:
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN, timeout=10)
        dialog.username = username
        dialog.password = password
        dialog.click_login()
        if not successful:
            not_login = dialog.error_message
            self.assertTrue(not_login, msg="Login successful Even After Wrong Password")
            dialog.header_object.close_button.click()
            return False
        return True

    def test_001_launch_the_ladscoral_application(self):
        """
        DESCRIPTION: Launch the lads/coral application
        EXPECTED: Home page should loaded succesfully
        """
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)

    def test_002_verify_settings_page(self):
        """
        DESCRIPTION: verify settings page
        EXPECTED: page consists of
        EXPECTED: 1.change password
        EXPECTED: 2.communication prefrennces
        EXPECTED: 3.Betting settings
        EXPECTED: 4.security
        """
        wait_for_result(
            lambda: self.site.header.has_right_menu() and self.site.header.right_menu_button.is_displayed(timeout=1),
            timeout=2,
            name='Right Menu button to be displayed')
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        right_menu_items = self.site.right_menu.section_wise_items
        setting = right_menu_items.get(vec.bma.V2_HEADER.account.upper()).get(vec.bma.EXPECTED_RIGHT_MENU.settings.upper())
        setting.click()
        wait_for_haul(20)
        setting_page_items = self.site.account_settings.items_as_ordered_dict
        setting_page_items_names = setting_page_items.keys()
        expected_setting_items = vec.bma.SETTINGS_MENU_ITEMS
        for setting_item in expected_setting_items:
            self.assertIn(setting_item, setting_page_items_names,
                          msg=f"Setting item {setting_item} is not present in Settings items {setting_page_items_names}")

    def test_003_verify_by_clicking_on_change_password(self):
        """
        DESCRIPTION: Verify by clicking on change password
        EXPECTED: change passowod page is opened
        """
        setting_page_items = self.site.account_settings.items_as_ordered_dict
        setting_page_items.get(vec.bma.CHANGE_PASSWORD).click()

    def test_004_verify_change_password_page(self):
        """
        DESCRIPTION: verify change password page
        EXPECTED: Change password' page consists of the following:
        EXPECTED: Page title is 'CHANGE PASSWORD'
        EXPECTED: Back button near title (left side)
        EXPECTED: Close button in the upper right corner
        EXPECTED: **'Old Password', 'New Password' fields
        EXPECTED: Show Password icon for each field
        EXPECTED: 'SUBMIT' button, enabled by default
        """
        wait_for_haul(10)
        page_title = self.site.change_password.header.title
        text = self.device.driver.execute_script('return arguments[0].innerText;', page_title._we)
        expected_header_title = vec.bma.CHANGE_PASSWORD
        self.assertEqual(text.upper(), expected_header_title.upper(), msg=f"{vec.bma.CHANGE_PASSWORD} page title:{page_title}"
                                                                          f"Expected {vec.bma.CHANGE_PASSWORD}")
        back_button = self.site.change_password.header.close_button
        self.assertTrue(back_button, msg="Back button Not Found On Change password Page")

        old_password = self.site.change_password.old_password.input
        self.assertTrue(old_password, msg="Old Password Not Found On Change password Page")

        new_password = self.site.change_password.new_password.input
        self.assertTrue(new_password, msg="New Password Not Found On Change password Page")

        sumbit_btn = self.site.change_password.submit_button
        self.assertTrue(sumbit_btn, msg="Sumbit Button not found Change Password Page")

        self.assertFalse(sumbit_btn.is_enabled(), msg="Sumbit is Not Disabled By Default")

    def test_005_verify_by_clicking_on_submit(self):
        """
        DESCRIPTION: verify by clicking on submit
        EXPECTED: password changed succesfully
        """
        old_password = self.site.change_password.old_password.input
        self.assertTrue(old_password, msg="Old Password Not Found On Change password Page")
        old_password.value = self.old_password

        new_password = self.site.change_password.new_password.input
        self.assertTrue(new_password, msg="New Password Not Found On Change password Page")
        new_password.value = self.new_password

        submit_btn = self.site.change_password.submit_button
        self.assertTrue(submit_btn, msg="Submit Button not found Change Password Page")

        self.assertTrue(submit_btn.is_enabled(), msg="Submit is Not Disabled By Default")

        submit_btn.click()
        wait_for_haul(10)
        successful_message = self.site.change_password.confirm_password_changed_message

        self.assertTrue(successful_message, msg="Successful Message Did not Appear")

        self.site.change_password.header.close_button.click()

        self.site.wait_content_state(state_name="Home")

    def test_006_log_out_and_try_to_login_with_old_passoword(self):
        """
        DESCRIPTION: log out and try to login with old passoword
        EXPECTED: user unable to login
        """
        self.site.logout()

        able_to_login = self.try_login(username=self.username, password=self.old_password, successful=False)
        self.assertFalse(able_to_login, msg="Login successful Even After Wrong Password")

    def test_007_log_out_and_try_to_login_with_new_passoword(self):
        """
        DESCRIPTION: log out and try to login with new passoword
        EXPECTED: user should be able to login
        """
        able_to_login = self.try_login(username=self.username, password=self.new_password, successful=True)
        self.assertTrue(able_to_login, msg="Login not successful Even After Correct Password")
        self.site.wait_logged_in()

    def test_008_mobileverify_by_clicking_on_the_backward_chevron_beside_account_details_header(self):
        """
        DESCRIPTION: Mobile
        DESCRIPTION: Verify by clicking on the backward chevron beside Account details header
        EXPECTED: User should be navigate to avatar menu page  successfully
        """
        # Covered in Step 2
        pass

    def test_009_desktopverify_the_username_with_avatar_beside_account_details_header(self):
        """
        DESCRIPTION: Desktop
        DESCRIPTION: Verify the username with avatar beside Account details header
        EXPECTED: User should able to see the username with avatar icon
        """
        # Covered in Step 2
        pass
