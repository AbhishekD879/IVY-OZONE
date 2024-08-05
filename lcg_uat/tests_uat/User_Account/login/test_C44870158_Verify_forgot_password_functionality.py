import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from random import randint


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@pytest.mark.user_password
@vtest
class Test_C44870158_Verify_forgot_password_functionality(Common):
    """
    TR_ID: C44870158
    NAME: Verify forgot password functionality
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Tap on 'Join' button
        EXPECTED: All mandatory fields are filled.
        EXPECTED: User is registered successfully
        """
        self.__class__.username = self.generate_user()
        self.__class__.email = f'test{randint(0, 10000000)}@internalgvc.com'
        self.__class__.birth_date = '1-06-1977'
        self.site.register_new_user(username=self.username, email=self.email, birth_date=self.birth_date)
        self.site.wait_content_state("HomePage")
        self.site.logout()
        self.site.wait_content_state_changed()

    def test_001_load_application__tap_on_log_in(self):
        """
        DESCRIPTION: Load Application & Tap on 'Log in'
        EXPECTED: Login overlay is loaded with
        EXPECTED: I forgot my username & I forgot my Password options available along with Registration tab.
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.Dialogs.DIALOG_MANAGER_LOG_IN)
        try:
            self.assertTrue(self.dialog, msg=f'"{vec.Dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        except Exception:
            self.site.header.sign_in.click()
            self.__class__.dialog = self.site.wait_for_dialog(vec.Dialogs.DIALOG_MANAGER_LOG_IN)
            self.assertTrue(self.dialog, msg=f'"{vec.Dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
        self.assertEqual(self.dialog.forgot_password_text.text, vec.bma.FORGOT_PASSWORD,
                         msg=f'Actual text:"{self.dialog.forgot_password_text.text}" is not same as'
                             f'Expected text:"{vec.bma.FORGOT_PASSWORD}"')
        # self.assertTrue(self.dialog.join_us.is_displayed(), msg=' "Register" button is not available')

    def test_002_tab_on_i_forgot_my_password(self):
        """
        DESCRIPTION: Tab on 'I forgot my Password'
        EXPECTED: Forgot password page is opened & the user is asked to enter the "username" and Submit
        EXPECTED: 'Live chat' & 'Contact us' is present just below submit tab.
        """
        self.dialog.forgot_password.password.click()
        self.site.wait_content_state_changed()
        self.__class__.password = self.site.forgot_password
        if self.brand == 'ladbrokes':
            expected_title = vec.bma.FORGOTTEN_PASSWORD_TEXT.title()
        else:
            expected_title = vec.bma.FORGOTTEN_PASSWORD_TEXT
        self.assertEqual(self.password.header_title_forgot_password.text, expected_title,
                         msg=f'Actual text: "{self.password.header_title_forgot_password.text}" is not same as'
                             f'Expected text: "{expected_title}"')
        self.assertTrue(self.password.username_input.is_displayed(), msg=' "Username" input is not available')
        self.assertFalse(self.password.submit_button.is_enabled(expected_result=False), msg=' "Submit" button is  enabled')
        self.assertTrue(self.password.live_chat.is_displayed(), msg=' "Live chat" button is not available')
        self.assertTrue(self.password.contact_us.is_displayed(), msg=' "Contact Us" button is not present')

    def test_003_when_the_username_is_entered_and_submitted(self):
        """
        DESCRIPTION: When the username is entered and submitted
        EXPECTED: The user is asked to enter registered email id and DOB and when submitted, a link to reset password is sent to the email.
        """
        self.password.username_input = self.email
        self.password.day = self.birth_date[:1]
        self.password.month = self.birth_date[3]
        self.password.year = self.birth_date[5:9]
        self.password.submit_button.click()
        self.site.wait_content_state_changed()
        self.password.no_longer_mobile_num.click()
        self.site.wait_content_state_changed()
        self.assertEqual(self.password.reset_password.text, vec.bma.RESET_MAIL_TXT,
                         msg=f'Actual text: "{self.password.reset_password.text}" is not same as'
                             f'Expected text: "{vec.bma.RESET_MAIL_TXT}"')
