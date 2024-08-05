import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@vtest
class Test_C29019_Verify_Currency_Symbol_on_the_Betslip(Common):
    """
    TR_ID: C29019
    NAME: Verify Currency Symbol on the Betslip
    DESCRIPTION: This test case verifies Verify Currency on the Betslip page.
    DESCRIPTION: AUTOTEST [C2493227]
    PRECONDITIONS: *   Make sure you have 4 registered users with different currency settings: **GBP**, **EUR**, **USD**, **SEK**
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: CORAL:
    PRECONDITIONS: *   'GBP': symbol = '**£**';
    PRECONDITIONS: *   'USD': symbol = '**$**';
    PRECONDITIONS: *   'EUR': symbol = '**€'**;
    PRECONDITIONS: *   'SEK': symbol = '**Kr**'
    PRECONDITIONS: LADBROKES:
    PRECONDITIONS: *   GBP currency
    PRECONDITIONS: *   AUD currency
    PRECONDITIONS: *   EUR currency
    PRECONDITIONS: *   NOK currency
    PRECONDITIONS: *   NZD currency
    PRECONDITIONS: *   CHF currency
    PRECONDITIONS: *   USD currency
    """
    keep_browser_open = True

    def test_001_log_in_user_with_gbp_currency(self):
        """
        DESCRIPTION: Log in user with **GBP** currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_add_one_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one selection to the BetSlip
        EXPECTED: 
        """
        pass

    def test_003_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: *   Betslip is shown
        EXPECTED: *   'Singles' section is present
        """
        pass

    def test_004_verify_currency_symbol_next_to_the_est_returns_value(self):
        """
        DESCRIPTION: Verify currency symbol next to the **'Est. Returns'** value
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_005_verify_currency_symbol_within_the_stake_field(self):
        """
        DESCRIPTION: Verify currency symbol within the **Stake** field
        EXPECTED: Currency symbol shouldn't be present next to the **Stake** field
        """
        pass

    def test_006_verify_currency_symbol_next_to_the_total_stake__and_total_est_returns_values(self):
        """
        DESCRIPTION: Verify currency symbol next to the ** Total Stake ** and **Total Est. Returns** values
        EXPECTED: Currency symbol matches with the currency symbol as per user's settings set during registration
        """
        pass

    def test_007_add_two_or_more_selections_from_different_events_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two or more selections from different events to the Bet Slip
        EXPECTED: * Selections are added
        EXPECTED: * 'All single stakes' field is present
        """
        pass

    def test_008_go_to_bet_slip_multiples_section(self):
        """
        DESCRIPTION: Go to Bet Slip, 'Multiples' section
        EXPECTED: 'Multiples' section is selected
        """
        pass

    def test_009_repeat_steps__4___5(self):
        """
        DESCRIPTION: Repeat steps # 4 - 5
        EXPECTED: 
        """
        pass

    def test_010_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        pass

    def test_011_log_in_user_withother_available_currency_usd_sek_audetc_(self):
        """
        DESCRIPTION: Log in user with other available currency (USD, SEK, AUD...etc )
        EXPECTED: User is logged in successfully
        """
        pass

    def test_012_repeat_steps_2_12(self):
        """
        DESCRIPTION: Repeat steps #2-12
        EXPECTED: 
        """
        pass
