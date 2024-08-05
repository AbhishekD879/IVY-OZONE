import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


# @pytest.mark.tst2 # This functionality is no longer applicable from release 108
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.login
# @pytest.mark.desktop
# @pytest.mark.critical
# @pytest.mark.user_account
# @pytest.mark.user_password
@pytest.mark.na
@vtest
class Test_C16646861_Vanilla_Unsuccessful_Log_In_with_card_and_PIN_Multi_channel_user(BaseUserAccountTest):
    """
    TR_ID: C16646861
    NAME: [Vanilla] Unsuccessful Log In with card and PIN (Multi-channel user)
    DESCRIPTION: This test case verifies Unsuccessful log in with connect card number and PIN
    DESCRIPTION: Note: User is considered as retail user only when he is trying to log in with 16-digit card number and 4-digit PIN, in all other cases when card number <> 16 digits and/or PIN <> 4 digits
    DESCRIPTION: user will be handled as online user that is trying to log in with username and password
    DESCRIPTION: Following user(ukmigct-tstEUR01/123123) can be used for testing:
    DESCRIPTION: Card: 5544440553493973
    DESCRIPTION: PIN: 1234
    DESCRIPTION: Other users can be found in doc: https://docs.google.com/spreadsheets/d/1VX1aBRgqLmclGxLYm-YcWVazCnODcDdebILKHpNHrI0/edit#gid=1026296319
    PRECONDITIONS: User is logged out
    """
    keep_browser_open = True

    def test_001_click_tap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" pop up is not displayed')
        self.dialog.connect_card_toggle.click()

    def test_002_do_not_enter_anything(self):
        """
        DESCRIPTION: Do not enter anything.
        EXPECTED: Card number and PIN fields are blank.
        """
        self.assertEqual(self.dialog.connect_card_number, "", msg='Grid card number field is not empty')
        self.assertEqual(self.dialog.connect_card_pin.input_value, "", msg='Grid pin number field is not empty')

    def test_003_click_log_in_button(self):
        """
        DESCRIPTION: Click LOG IN button.
        EXPECTED: 'Please enter your credentials' error message is displayed.
        """
        self.dialog.click_login()
        expected_error_message = self.site.window_client_config.connect_card_empty_credentials_error
        self.assertTrue(self.dialog.wait_error_message(),
                        msg=f'Error message "{expected_error_message}" is not displayed')
        self.__class__.error_message = self.dialog.error_message
        self.assertEqual(self.error_message, expected_error_message,
                         msg=f'Error message "{self.error_message}" '
                             f'does not equal the expected message: "{expected_error_message}"')

    def test_004_enter_the_correct_card_number_and_correct_pin_and_click_on_log_in_button(self):
        """
        DESCRIPTION: Enter the correct card number and correct PIN and click on LOG IN button.
        EXPECTED: User should NOT be logged in.
        EXPECTED: "You have upgraded your account. Please use your Username and Password to log in with" Red message should be displayed.
        """
        self.dialog.connect_card_number = tests.settings.inshop_upgraded_user
        self.dialog.connect_card_pin = tests.settings.in_shop_pin
        self.dialog.click_login()
        expected_error_message = vec.retail.UPGRADED_INSHOP_USER_LOGIN_ERROR
        self.assertTrue(self.dialog.wait_for_error_message_to_change(expected_error_message),
                        msg=f'Error message has not changed from "{self.error_message}" to "{expected_error_message}"')
        self.assertFalse(self.site.wait_logged_in(timeout=1), msg='User is logged in')
