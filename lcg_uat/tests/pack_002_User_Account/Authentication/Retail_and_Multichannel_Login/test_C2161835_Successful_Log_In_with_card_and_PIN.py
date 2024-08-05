import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


#@pytest.mark.prod
@pytest.mark.hl
#@pytest.mark.tst2
#@pytest.mark.stg2
@pytest.mark.connect_user
@pytest.mark.user_account
@pytest.mark.user_password
@pytest.mark.critical
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.na
@vtest
@pytest.mark.connect_descoped
class Test_C2161835_C16269002_Successful_Log_In_with_card_and_PIN(BaseUserAccountTest):
    """
    TR_ID: C2161835
    TR_ID: C16269002
    NAME: Successful Log In with card and PIN
    DESCRIPTION: This test case verifies successful log in with connect card number and PIN
    PRECONDITIONS: User is logged out
    """
    keep_browser_open = True
    pin_type = 'password'

    def test_001_click_tap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" pop up is not displayed')

    def test_002_enter_existing_correct_card_number(self):
        """
        DESCRIPTION: Enter existing correct card number
        EXPECTED: Card number is displayed
        """
        # Introducing additional step -> click on connect card toggle
        self.dialog.connect_card_toggle.click()
        self.assertTrue(self.dialog.connect_card_toggle.is_selected(),
                        msg='Connect Card toggle has not been selected!')
        inshop_user = tests.settings.inshop_user
        self.dialog.connect_card_number = inshop_user
        actual_card_number = self.dialog.connect_card_number
        self.assertEqual(actual_card_number, inshop_user,
                         msg=f'Actual card number: "{actual_card_number}" don\'t match expected: "{inshop_user}"')

    def test_003_enter_correct_corresponding_pin_4_digits(self):
        """
        DESCRIPTION: Enter correct corresponding PIN (4 digits)
        EXPECTED: Entered PIN is displayed as ****
        """
        self.dialog.connect_card_pin = tests.settings.in_shop_pin
        pin_type = self.dialog.connect_card_pin.input_type
        pin_value = self.dialog.connect_card_pin.input_value
        self.assertEqual(pin_value, tests.settings.in_shop_pin, msg='PIN field is empty')
        self.assertEqual(pin_type, self.pin_type, msg='PIN is not encrypted')

    def test_004_click_tap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: * Log in popup is closed
        EXPECTED: * User is logged in successfully
        EXPECTED: * Page from which user made log in is still shown
        """
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='Login dialog was not closed')
        if self.site.upgrade_your_account.is_displayed(timeout=10):
            self.site.upgrade_your_account.no_thanks_button.click()
        self.site.wait_content_state(state_name='Homepage')
        self.assertTrue(self.site.wait_logged_in(timeout=10), msg='User is not logged in')
