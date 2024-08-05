import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29032_Currency_Validation_on_Quick_Deposit(Common):
    """
    TR_ID: C29032
    NAME: Currency Validation on Quick Deposit
    DESCRIPTION: This test case verifies Currency in the Quick Deposit section and on Quick Deposit Validation messages in Betslip.
    DESCRIPTION: AUTOTEST Mobile: [C2605949]
    DESCRIPTION: AUTOTEST Desktop: [C2606190]
    PRECONDITIONS: Four User accounts with different currencies (GBP, EUR, USD, SEK) and registered credit card
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: *   'GBP': symbol = '**£**';
    PRECONDITIONS: *   'USD': symbol = '**$**';
    PRECONDITIONS: *   'EUR': symbol = '**€'**;
    """
    keep_browser_open = True

    def test_001_log_in_with_gb_user_account(self):
        """
        DESCRIPTION: Log in with GB user account
        EXPECTED: - User is logged in
        """
        pass

    def test_002_add_any_selection_to_the_bet_slip___go_to_the_bet_slip_pagewidget(self):
        """
        DESCRIPTION: Add any selection to the Bet Slip -> go to the Bet Slip page/widget
        EXPECTED: - Made selection is displayed correctly within Bet Slip content area
        """
        pass

    def test_003_enter_stake_amount_greater_than_current_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount greater than current user's balance
        EXPECTED: 'GBP' currency is displayed next to:
        EXPECTED: 'Please deposit a min £XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip
        EXPECTED: where,
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        """
        pass

    def test_004_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: - 'Quick Deposit' section is displayed at the bottom of the Bet Slip with all content
        EXPECTED: - 'MAKE A DEPOSIT' changed to 'DEPOSIT & PLACE BET' button disabled by default
        """
        pass

    def test_005_verify_currency_set_within_quick_deposit_section(self):
        """
        DESCRIPTION: Verify currency set within Quick Deposit section
        EXPECTED: GBP' currency is displayed next to:
        EXPECTED: * 'Please deposit a min £XX.XX to continue placing your bet' error message
        EXPECTED: * 'Deposit Amount' field
        EXPECTED: where,
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        """
        pass

    def test_006_enter_invalid_amount_into_amount_field_less_than_5_and_tap_deposit__place_bet__button(self):
        """
        DESCRIPTION: Enter invalid amount into 'Amount' field (less than 5) and tap 'DEPOSIT & PLACE BET'  button
        EXPECTED: Error message  'The minimum deposit amount is **£** **5/50.**' is displayed under 'Amount' field
        """
        pass

    def test_007_close_betslip_and_log_out(self):
        """
        DESCRIPTION: Close Betslip and Log Out
        EXPECTED: Betslip closed
        """
        pass

    def test_008_repeat_steps_1_7_for___usd_symbol_____eur_symbol__(self):
        """
        DESCRIPTION: Repeat steps №1-7 for
        DESCRIPTION: *   'USD': symbol = **$**;
        DESCRIPTION: *   'EUR': symbol = **€**;
        EXPECTED: 
        """
        pass
