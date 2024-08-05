import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.helpers import string_generator


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.login
@pytest.mark.desktop
@vtest
class Test_C16268958_Vanilla_Verify_Login_Form_Error_Handling(Common):
    """
    TR_ID: C16268958
    NAME: [Vanilla] Verify Login Form Error Handling
    DESCRIPTION: This test case verifies error handling on login for
    PRECONDITIONS: **Choosing the password should include following rules:**
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    PRECONDITIONS: a. To find Error message Open Dev. tool ->Network-> Request 'LoginAndGetTempToken.php?casinoname=coraltst..' -> Response -> 'UserErrors'
    PRECONDITIONS: b. Messages should be displayed in this order (usually only type 2, message 1 is received):
    PRECONDITIONS: 1. UserErrors: displayType:"2" message 1
    PRECONDITIONS: 2. UserErrors: displayType:"2" message 2
    PRECONDITIONS: 3. UserErrors: displayType:"1" message 1
    PRECONDITIONS: c. If there in no element in the UserError array we should display the txt in 'Player message'.
    PRECONDITIONS: d. If there is no 'Player message' we should display errorText
    PRECONDITIONS: e. Every message displayed to the customer should start on a new line
    PRECONDITIONS: f. If no message is received at all, then display 'You have entered an invalid username or password. Please try again.'
    """
    keep_browser_open = True

    def check_error_message(self):
        expected_error_messages = [vec.gvc.INCORRECT_CREDENTIALS, vec.gvc.INCORRECT_PASSWORD_ERROR]
        error_message = self.dialog.error_message
        self.assertIn(error_message, expected_error_messages,
                      msg=f'Error message "{error_message}" does not match any of the expected error messages:'
                          f'"{vec.gvc.INCORRECT_PASSWORD_ERROR}" or "{vec.gvc.PROBLEMS_LOGGING_IN}".')

    def test_001_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' form is opened
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" pop up is not displayed')

    def test_002_enter_valid_username_and_invalid_password(self):
        """
        DESCRIPTION: Enter valid username and invalid password
        EXPECTED: Data is entered and displayed
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = 'wrong'

    def test_003_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' button
        EXPECTED: Validation error message is displayed at the top of 'Log In' pop-up. Error message received in response is displayed according to the order described in Preconditions
        """
        self.dialog.click_login()
        self.assertTrue(self.dialog.wait_error_message(), msg='Error message did not appear!')

    def test_004_verify_error_message_section(self):
        """
        DESCRIPTION: Verify error message section
        EXPECTED: *  Section with error message is aligned with 'username' and 'password' fields
        EXPECTED: *  Error message is displayed in red color
        EXPECTED: * 'i' icon is displayed next to error message
        """
        self.check_error_message()
        self.assertNotEqual(self.dialog.error_message_exclamation_mark, 'none',
                            msg='Exclamation mark is absent before error message!')

    def test_005_enter_invalid_username_and_valid_password(self):
        """
        DESCRIPTION: Enter invalid username and valid password
        EXPECTED: Data is entered and displayed
        """
        self.dialog.username = string_generator()
        self.dialog.password = tests.settings.default_password

    def test_006_tap_on_log_in_button(self):
        """
        DESCRIPTION: Tap on 'Log In' button
        EXPECTED: Validation error message is displayed at the top of 'Log In' pop-up. Error message received in response is displayed according to the order described in Preconditions
        """
        self.dialog.click_login()
        self.assertTrue(self.dialog.wait_error_message(),
                        msg='Error message did not appear!')
        self.check_error_message()

    def test_007_enter_invalid_username_and_invalid_password_tap_on_log_in_button(self):
        """
        DESCRIPTION: Enter invalid username and invalid password -> tap on 'Log In' button
        EXPECTED: Error message received in response is displayed according to the order described in Preconditions
        """
        self.assertTrue(self.dialog.username_field.is_enabled(),
                        msg='Username field is not enabled!')
        self.dialog.username = string_generator()
        self.dialog.password = 'wrong'
        self.dialog.click_login()
        self.assertTrue(self.dialog.wait_error_message(),
                        msg='Error message did not appear!')
        self.check_error_message()
