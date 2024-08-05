import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.cash_out
@vtest
class Test_C146510_Currency_Symbol_on_the_Cash_Out_tab(Common):
    """
    TR_ID: C146510
    NAME: Currency Symbol on the 'Cash Out' tab
    DESCRIPTION: This test case verifies Verify Currency Symbol on the 'Cash Out' tab
    PRECONDITIONS: Make sure you have 4 registered users with different currency settings: **GBP**, **EUR**, **USD**, **SEK**
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: CORAL
    PRECONDITIONS: *   'GBP': symbol = '**£**';
    PRECONDITIONS: *   'USD': symbol = '**$**';
    PRECONDITIONS: *   'EUR': symbol = '**€'**;
    PRECONDITIONS: *   'NOK': symbol = '**NOK**'
    PRECONDITIONS: LADBROKES:
    PRECONDITIONS: *   GBP currency
    PRECONDITIONS: *   AUD currency
    PRECONDITIONS: *   EUR currency
    PRECONDITIONS: *   NOK currency
    PRECONDITIONS: *   NZD currency
    PRECONDITIONS: *   CHF currency
    PRECONDITIONS: *   USD currency
    PRECONDITIONS: User has placed a bet on Pre Match or In-Play match (Singles or Multiple bets) where **Cash Out** offer is available (on SS see cashoutAvail="Y" on Event and Market level to be sure whether COMB option is available)
    """
    keep_browser_open = True

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_navigate_to_cash_out_tab_on_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: 
        """
        pass

    def test_003_verify_currency_symbol_near_stake_amount_on_cashout_accordion_header(self):
        """
        DESCRIPTION: Verify currency symbol near stake amount on cashout accordion header
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_004_verify_currency_symbol_next_to_the_stake_value_in_bet_line_details(self):
        """
        DESCRIPTION: Verify currency symbol next to the **Stake** value in bet line details
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_005_verify_currency_symbol_next_to_the_est_returns_value_in_bet_line_details(self):
        """
        DESCRIPTION: Verify currency symbol next to the **Est. Returns** value in bet line details
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_006_verify_currency_symbol_on_the_cash_out_button(self):
        """
        DESCRIPTION: Verify currency symbol on the '**CASH OUT**' button
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_007_tap_cash_out_button_and_verify_currency_symbol_on_the_confirm_button(self):
        """
        DESCRIPTION: Tap 'CASH OUT' button and verify currency symbol on the '**CONFIRM**' button
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_008_click_partial_cashout_button_and_verify_the_currency_symbol_on_it(self):
        """
        DESCRIPTION: Click 'Partial Cashout' button and verify the currency symbol on it.
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_009_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        pass

    def test_010_log_in_user_witheurcurrency(self):
        """
        DESCRIPTION: Log in user with **EUR **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_011_repeat_steps_2_9(self):
        """
        DESCRIPTION: Repeat steps #2-9
        EXPECTED: 
        """
        pass

    def test_012_log_in_user_with_usdcurrency(self):
        """
        DESCRIPTION: Log in user with **USD **currency
        EXPECTED: User is logged out successfully
        """
        pass

    def test_013_repeat_steps_2_9(self):
        """
        DESCRIPTION: Repeat steps #2-9
        EXPECTED: 
        """
        pass

    def test_014_log_in_user_withother_available_currency(self):
        """
        DESCRIPTION: Log in user with other available currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_015_repeat_steps_2_9(self):
        """
        DESCRIPTION: Repeat steps #2-9
        EXPECTED: 
        """
        pass
