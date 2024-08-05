import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C28267_Vanilla_Verify_Currency_on_the_Deposit_page(Common):
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

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: 'Deposit' page is opened
        """
        pass

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
        pass

    def test_004_select_debitcredit_cards_and_enter_valid_cv2(self):
        """
        DESCRIPTION: Select **Debit/Credit Cards** and enter valid CV2
        EXPECTED: 
        """
        pass

    def test_005_check_transaction_currency_field(self):
        """
        DESCRIPTION: Check 'Transaction Currency' field
        EXPECTED: Currency by default matches with the currency symbol:
        EXPECTED: *   as per user's settings set during registration
        """
        pass

    def test_006_enter_invalid_amount_into_amount_edit_field_tap_deposit_button_and_verify_currency_symbol_on_the_error_message(self):
        """
        DESCRIPTION: Enter invalid amount into amount edit field, tap 'Deposit' button and verify currency symbol on the error message
        EXPECTED: *   Error message  "**Minimum deposit for this option is <currency symbol> 5.00**" is shown
        EXPECTED: *   Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_007_enter_valid_amount_tap_deposit_button_and_verify_currency_symbol_on_successful_message(self):
        """
        DESCRIPTION: Enter valid amount, tap 'Deposit' button and verify currency symbol on successful message
        EXPECTED: *   Successfull message: **"Your deposit of XX.XX <currency symbol> has been successful.** is shown
        EXPECTED: *   Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_008_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        pass

    def test_009_log_in_user_witheur_currency(self):
        """
        DESCRIPTION: Log in user with **EUR** currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_010_repeat_steps_2_14(self):
        """
        DESCRIPTION: Repeat steps №2-14
        EXPECTED: 
        """
        pass

    def test_011_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        pass

    def test_012_log_in_user_with_usd_currency(self):
        """
        DESCRIPTION: Log in user with **USD** currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_013_repeat_steps_2_14(self):
        """
        DESCRIPTION: Repeat steps №2-14
        EXPECTED: 
        """
        pass
