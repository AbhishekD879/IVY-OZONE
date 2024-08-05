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
class Test_C1663791_Verify_deposit_using_expired_card_when_users_balance_is_100_and_expired_card_is_default_Betslip(Common):
    """
    TR_ID: C1663791
    NAME: Verify deposit using expired card when user's balance is > 100 and expired card is default (Betslip)
    DESCRIPTION: This test case verifies Deposit functionality with expired card via Quick Deposit on Betslip and Quickbet when user's balance is > 100 and expired card is default payment method
    DESCRIPTION: NOTE: not up to date due to old cashier steps
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has a card that expired
    PRECONDITIONS: User balance is > 100 and expired card is a default payment method
    """
    keep_browser_open = True

    def test_001_add_any_selection_to_the_bet_slip_and_open_bet_slip_page__widget(self):
        """
        DESCRIPTION: Add any selection to the Bet Slip and open Bet Slip page / widget
        EXPECTED: Add any selection to the Bet Slip and open Bet Slip page / widget
        """
        pass

    def test_002_enter_stake_amount_that_exceeds_the_users_balance(self):
        """
        DESCRIPTION: Enter 'Stake' amount that exceeds the user`s balance
        EXPECTED: * 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' error message is displayed at the bottom of Betslip immediately
        EXPECTED: where,
        EXPECTED: <currency symbol> - currency that was set during registration
        EXPECTED: 'XX.XX' - the difference between entered stake value and users balance
        EXPECTED: * 'PLACE BET' button becomes 'MAKE A DEPOSIT' immediately and is enabled by default
        """
        pass

    def test_003_tap_make_a_deposit_button(self):
        """
        DESCRIPTION: Tap 'MAKE A DEPOSIT' button
        EXPECTED: * Quick Deposit section is displayed at the bottom of Betslip
        EXPECTED: * 'MAKE A DEPOSIT' button becomes 'DEPOSIT & PLACE BET'
        EXPECTED: * The expired card is selected by default
        EXPECTED: * 'DEPOSIT & PLACE BET' button is disabled
        EXPECTED: * "Sorry, but your credit/debit card is expired. Please go to Account Settings to resolve the issue." message displayed.
        EXPECTED: ---
        EXPECTED: WHERE *Account Settings* is a tappable/clickable link-label, that redirects user to 'https://accountone.ladbrokes.com/deposit?clientType=sportsbook&back_url=https%3A%2F%2Fmsports.ladbrokes.com%2F' page, closing 'Quick Deposit' section once tapped/clicked.
        """
        pass
