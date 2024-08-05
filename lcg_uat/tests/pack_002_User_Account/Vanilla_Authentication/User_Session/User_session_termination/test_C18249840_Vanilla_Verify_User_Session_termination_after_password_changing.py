import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C18249840_Vanilla_Verify_User_Session_termination_after_password_changing(BaseUserAccountTest):
    """
    TR_ID: C18249840
    NAME: [Vanilla] Verify User Session termination after password changing
    DESCRIPTION: This test case verifies user session termination after password changing
    PRECONDITIONS: Private mode is switched off on device browser
    """
    keep_browser_open = True
    password = tests.settings.default_password
    new_pswd = "Qwerty20"

    def test_001_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: The main page should be displayed
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username, remember_me=True, async_close_dialogs=False)

    def test_002_specify__valid_login__valid_password__tick_remember_me_checkbox(self):
        """
        DESCRIPTION: Specify:
        DESCRIPTION: - valid Login
        DESCRIPTION: - valid Password
        DESCRIPTION: - tick "Remember me" checkbox
        EXPECTED: All fields /UI controls fulfilled
        EXPECTED: ![](index.php?/attachments/get/35829)
        """
        # covered in step 1

    def test_003_click_on_login(self):
        """
        DESCRIPTION: Click on Login
        EXPECTED: User Should be successfully logged in
        """
        # covered in step 1

    def test_004_click_on_my_account_icon____settings__change_password(self):
        """
        DESCRIPTION: Click on "My Account" icon --> "Settings"--"Change Password"
        EXPECTED: Change Password Page should be opened
        EXPECTED: ![](index.php?/attachments/get/35959)
        """
        if self.device_type == 'desktop':
            self.site.header.user_panel.my_account_button.click()
        else:
            self.site.header.right_menu_button.click()
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
        change_password_link = self.site.right_menu.items_as_ordered_dict.get(
            self.site.window_client_config.change_password_menu_title)
        self.assertTrue(change_password_link.is_displayed(), msg='Change password link is not displayed')
        change_password_link.click()
        result = wait_for_result(lambda: self.site.change_password.is_displayed(),
                                 name='Wait for header title to change',
                                 timeout=30)
        self.assertTrue(result, msg='Change password page is not displayed')

    def test_005_specify_old_and_new_password_and_click_on_submit_button(self):
        """
        DESCRIPTION: Specify Old and New password and click on "Submit" button
        EXPECTED: "Password changed successfully!" message should appear
        """
        change_password = self.site.change_password
        change_password.old_password.input.value = self.password
        change_password.new_password.input.value = self.new_pswd
        self.assertTrue(change_password.submit_button.is_enabled(), msg='Submit button is not enabled.')
        change_password.submit_button.click()
        result = wait_for_result(
            lambda: change_password.confirm_password_changed_message == vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG,
            timeout=20)
        self.assertTrue(result, msg=f'"{vec.gvc.CHANGE_PASSWORD_SUCCESS_MSG}" is not displayed')

    def test_006_close_browser(self):
        """
        DESCRIPTION: Close browser
        EXPECTED: n/a
        """
        self.device.close_current_tab()

    def test_007_open_browser_and_load_to_vanilla_evn_eg_httpqa2sportscoralcouk(self):
        """
        DESCRIPTION: Open browser and load to Vanilla evn (e.g. http://qa2.sports.coral.co.uk)
        EXPECTED: According to VANO-1078:
        EXPECTED: user session should be terminated
        EXPECTED: user should NOT be Logged in
        EXPECTED: Login button should be displayed
        """
        self.create_new_browser_instance()
        self.site.wait_content_state("Home")
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='User is logged in')
