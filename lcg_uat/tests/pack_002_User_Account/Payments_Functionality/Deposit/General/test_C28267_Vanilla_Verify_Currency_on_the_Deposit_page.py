from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec
import pytest
import tests


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C28267_Vanilla_Verify_Currency_on_the_Deposit_page(BaseBetSlipTest):
    """
    TR_ID: C28267
    NAME: [Vanilla] Verify Currency on the Deposit page
    DESCRIPTION: This test case verifies Currency on the Deposit page.
    PRECONDITIONS: 1.  User is logged in
    PRECONDITIONS: 2.  User has registered Debit/Credit Cards from which they can deposit funds from
    PRECONDITIONS: 3.  User knows his/her Daily Limit
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: *   'GBP': symbol = **'£'**;
    PRECONDITIONS: *   'USD': symbol = **'$'**;
    PRECONDITIONS: *   'EUR': symbol = **'€'**.
    """
    keep_browser_open = True
    invalid_deposit_amount = 0.00
    valid_deposit_amount = 20.00

    def validate_user_input_amount_error(self, currency):
        self.deposit_menu.amount.input.value = self.invalid_deposit_amount
        self.deposit_menu.cvv_2.input.value = tests.settings.master_card_cvv
        self.deposit_menu.deposit_button.click()
        wait_for_result(lambda: self.deposit_menu.user_input_amount_error, timeout=10)
        expected_error_message = f'Minimum deposit for this option is {currency} 5.00.'
        actual_error_message = str(self.deposit_menu.user_input_amount_error.text)
        self.assertEqual(actual_error_message, expected_error_message,
                         msg=f'expected error message {expected_error_message} is not equal to actual error message {actual_error_message}')

    def deposit_valid_amount_and_verify_successful_message(self, currency):
        self.deposit_menu.amount.input.value = self.valid_deposit_amount
        actual_amount = self.deposit_menu.amount.input.value
        expected_amount = str(self.valid_deposit_amount)
        self.assertEqual(actual_amount, expected_amount,
                         msg=f'Actual amount "{actual_amount}" != Expected "{expected_amount}"')
        self.deposit_menu.deposit_button.click()
        wait_for_result(lambda: self.site.deposit_transaction_details.ok_button.is_displayed(),
                        name='OK button is displayed',
                        timeout=5)
        expected = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.valid_deposit_amount)
        expected_message = expected.replace("GBP", currency)
        actual_message = self.site.deposit_transaction_details.successful_message
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual message "{actual_message}" != Expected "{expected_message}"')

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        username = tests.settings.master_card_user
        self.site.login(username=username)
        self.site.wait_content_state('HomePage')
        self.site.close_all_dialogs()

    def test_002_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: 'Deposit' page is opened
        """
        self.site.header.right_menu_button.avatar_icon.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        cashier_title = self.site.window_client_config.cashier_menu_title
        self.site.right_menu.click_item(item_name=cashier_title)
        result = wait_for_result(lambda: self.site.right_menu.header.title == cashier_title,
                                 name='Wait for header title to change')
        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                                    f'expected "{cashier_title}"')
        sections = self.site.right_menu.items_names
        deposit = self.site.window_client_config.deposit_menu_title
        self.assertIn(deposit, sections,
                      msg=f'"{deposit}" is not found in "{sections}"')
        self.site.right_menu.click_item(item_name=self.site.window_client_config.deposit_menu_title)
        self.assertTrue(self.site.deposit.is_displayed(scroll_to=False),
                        msg='"Deposit" menu is not displayed')

    def test_003_verify_currency_symbol_next_to_the_quick_deposit_buttons___plus20___plus50___plus100___plus250___plus500(self):
        """
        DESCRIPTION: Verify currency symbol next to the quick deposit buttons:
        DESCRIPTION: *   +20
        DESCRIPTION: *   +50
        DESCRIPTION: *   +100
        DESCRIPTION: *   +250
        DESCRIPTION: *   +500
        EXPECTED: Currency symbol matches with the currency symbol:
        EXPECTED: *   as per user's settings set during registration
        EXPECTED: *   next to the user balance
        """
        # skipping this step validation as it is not implemented on deposit page and able to see on quick deposit page.

    def test_004_select_debitcredit_cards_and_enter_valid_cv2(self):
        """
        DESCRIPTION: Select **Debit/Credit Cards** and enter valid CV2
        """
        self.__class__.deposit_menu = self.site.deposit
        self.deposit_menu.cvv_2.input.value = tests.settings.master_card_cvv
        actual_cvv2 = self.deposit_menu.cvv_2.input.value
        self.assertEqual(actual_cvv2, tests.settings.master_card_cvv,
                         msg=f'Actual CVV2 "{actual_cvv2}" != Expected "{tests.settings.master_card_cvv}"')

    def test_005_check_transaction_currency_field(self):
        """
        DESCRIPTION: Check 'Transaction Currency' field
        EXPECTED: Currency by default matches with the currency symbol:
        EXPECTED: *   as per user's settings set during registration
        """
        # covered in step 6

    def test_006_enter_invalid_amount_into_amount_edit_field_tap_deposit_button_and_verify_currency_symbol_on_the_error_message(self):
        """
        DESCRIPTION: Enter invalid amount into amount edit field, tap 'Deposit' button and verify currency symbol on the error message
        EXPECTED: *   Error message  "**Minimum deposit for this option is <currency symbol> 5.00**" is shown
        EXPECTED: *   Currency symbol matches with the currency symbol as per user's settings
        """
        self.validate_user_input_amount_error(currency="GBP")

    def test_007_enter_valid_amount_tap_deposit_button_and_verify_currency_symbol_on_successful_message(self):
        """
        DESCRIPTION: Enter valid amount, tap 'Deposit' button and verify currency symbol on successful message
        EXPECTED: *   Successfull message: **"Your deposit of XX.XX <currency symbol> has been successful.** is shown
        EXPECTED: *   Currency symbol matches with the currency symbol as per user's settings
        """
        self.deposit_valid_amount_and_verify_successful_message(currency="GBP")

    def test_008_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        self.navigate_to_page("Homepage")
        self.site.wait_content_state('HomePage', timeout=5)
        self.site.logout()

    def test_009_log_in_user_witheur_currency(self):
        """
        DESCRIPTION: Log in user with **EUR** currency
        EXPECTED: User is logged in successfully
        """
        username = tests.settings.user_with_euro_currency_and_card
        self.site.login(username=username)
        self.site.wait_content_state('HomePage')
        self.site.close_all_dialogs()

    def test_010_repeat_steps_2_14(self):
        """
        DESCRIPTION: Repeat steps №2-14
        """
        self.test_002_open_deposit_page()
        self.test_003_verify_currency_symbol_next_to_the_quick_deposit_buttons___plus20___plus50___plus100___plus250___plus500()
        self.test_004_select_debitcredit_cards_and_enter_valid_cv2()
        self.test_005_check_transaction_currency_field()
        self.validate_user_input_amount_error(currency="EUR")
        self.deposit_valid_amount_and_verify_successful_message(currency="EUR")

    def test_011_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        self.navigate_to_page("Homepage")
        self.site.wait_content_state('HomePage', timeout=5)
        self.site.logout()

    def test_012_log_in_user_with_usd_currency(self):
        """
        DESCRIPTION: Log in user with **USD** currency
        EXPECTED: User is logged in successfully
        """
        username = tests.settings.user_with_usd_currency_and_card
        self.site.login(username=username)
        self.site.wait_content_state('HomePage')
        self.site.close_all_dialogs()

    def test_013_repeat_steps_2_14(self):
        """
        DESCRIPTION: Repeat steps №2-14
        """
        self.test_002_open_deposit_page()
        self.test_003_verify_currency_symbol_next_to_the_quick_deposit_buttons___plus20___plus50___plus100___plus250___plus500()
        self.test_004_select_debitcredit_cards_and_enter_valid_cv2()
        self.test_005_check_transaction_currency_field()
        self.validate_user_input_amount_error(currency="USD")
        self.deposit_valid_amount_and_verify_successful_message(currency="USD")
