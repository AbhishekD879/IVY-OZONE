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
class Test_C17752139_Vanilla_Verify_Currency_on_the_Payment_History_page(Common):
    """
    TR_ID: C17752139
    NAME: [Vanilla] Verify Currency on the Payment History page
    DESCRIPTION: This test case verifies Currency on the Transaction History page.
    PRECONDITIONS: *   User has registered Debit/Credit Card, PayPal and NETELLER methods
    PRECONDITIONS: *   Make sure you have 4 registered users with different currency settings: **GBP**, **EUR**, **USD**
    PRECONDITIONS: *   Make sure you have Approved, Pending, Declined and Waiting Deposit/Withdraw transactions.
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: *   'GBP': symbol = '**£**';
    PRECONDITIONS: *   'USD': symbol = '**$**';
    PRECONDITIONS: *   'EUR': symbol = '**€'**;
    """
    keep_browser_open = True

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_go_to_menu___history__payment_history_page(self):
        """
        DESCRIPTION: Go to 'Menu' -> 'History' ->'Payment History' page
        EXPECTED: *   'Payment History' page is opened
        EXPECTED: *   Three buttons are visible: ' **All** ', ' **Deposit** ' and ' **Withdraw** '
        EXPECTED: *   ' **All** ' button is selected by default
        """
        pass

    def test_003_verify_currency_symbol_next_to_the_amount_on_the_listed_depositswithdrawals_displayed_below_go_button(self):
        """
        DESCRIPTION: Verify currency symbol next to the amount on the listed deposits/withdrawals displayed below 'GO' button
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_004_tap_deposit_tab_and_verify_currency_symbol_next_to_the_amount(self):
        """
        DESCRIPTION: Tap 'Deposit' tab and verify currency symbol next to the amount
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_005_tap_withdrawal_tab_and_verify_currency_symbol_next_to_the_amount(self):
        """
        DESCRIPTION: Tap 'Withdrawal' tab and verify currency symbol next to the amount
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_006_tap_reverse_tab_in_one_withdrawal_option_and_verify_currency_symbol_next_to_the_amount(self):
        """
        DESCRIPTION: Tap 'Reverse' tab in one 'Withdrawal' option and verify currency symbol next to the amount
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_007_log_out_and_log_in_user_witheurcurrency(self):
        """
        DESCRIPTION: Log out and log in user with **EUR **currency
        EXPECTED: 
        """
        pass

    def test_008_repeat_steps_2_7(self):
        """
        DESCRIPTION: Repeat steps №2-7
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings
        """
        pass

    def test_009_log_in_user_with_usdcurrency(self):
        """
        DESCRIPTION: Log in user with **USD **currency
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps_2_7(self):
        """
        DESCRIPTION: Repeat steps №2-7
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings
        """
        pass
