import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C29219_Verify_Currency_Symbol_on_the_Open_Bets_and_Settled_Bets(Common):
    """
    TR_ID: C29219
    NAME: Verify Currency Symbol on the 'Open Bets' and Settled Bets
    DESCRIPTION: This test case verifies  Currency Symbol on the 'My Bets' tab.
    DESCRIPTION: **Jira tickets:** BMA-3145, BMA-17176, BMA-17820
    DESCRIPTION: AUTOTEST [C1501874]
    PRECONDITIONS: 1. Make sure you have 4 registered users with different currency settings: **GBP**, **EUR**, **USD**, **SEK**
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: CORAL
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
    PRECONDITIONS: 2. User should have 'Pending' bets and 'Settled' bets
    PRECONDITIONS: This test case is applied for **Mobile** and **Tablet** application.
    """
    keep_browser_open = True

    def test_001_log_in_user_withgbpcurrency(self):
        """
        DESCRIPTION: Log in user with **GBP **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_002_go_to_my_bets_pagebet_slip_widget(self):
        """
        DESCRIPTION: Go to 'My Bets' page/'Bet Slip' widget
        EXPECTED: *   'My Bets' page/'Bet Slip' widget is opened
        EXPECTED: *   'Open Bets' tab is shown next to 'Cash Out' tab
        """
        pass

    def test_003_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: *   'Regular', 'Player Bets', 'Lotto' and 'Pools' sort filters are shown
        EXPECTED: *   'Regular' sort filter is selected by default
        """
        pass

    def test_004_verify_open_bets_tab_content_when_regular_sort_filter_is_selected(self):
        """
        DESCRIPTION: Verify 'Open Bets' tab content when 'Regular' sort filter is selected
        EXPECTED: 'Pending' (Open) bets are displayed
        """
        pass

    def test_005_verify_currency_symbol_in_bet_details(self):
        """
        DESCRIPTION: Verify currency symbol in Bet Details
        EXPECTED: Currency symbol matches with the currency symbol:
        EXPECTED: *   as per user's settings set during registration
        EXPECTED: *   next to the user balance
        """
        pass

    def test_006_verify_open_bets_tab_content_when_pools_sort_filter_is_selected(self):
        """
        DESCRIPTION: Verify 'Open Bets' tab content when 'Pools' sort filter is selected
        EXPECTED: 'Pending' (Open) bets are displayed
        """
        pass

    def test_007_verify_currency_symbol_on_bet_section_header_and_in_bet_details(self):
        """
        DESCRIPTION: Verify currency symbol on bet section header and in bet details
        EXPECTED: All currency symbols at any time are:
        EXPECTED: GBP: symbol = '**£**';
        """
        pass

    def test_008_tap_logout_menu_item(self):
        """
        DESCRIPTION: Tap Logout menu item
        EXPECTED: User is logged out successfully
        """
        pass

    def test_009_log_in_user_witheurcurrency(self):
        """
        DESCRIPTION: Log in user with **EUR **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_010_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps №2-6
        EXPECTED: The same as on the steps №2-7
        """
        pass

    def test_011_log_in_user_withusdcurrency(self):
        """
        DESCRIPTION: Log in user with **USD **currency
        EXPECTED: User is logged out successfully
        """
        pass

    def test_012_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps №2-6
        EXPECTED: The same as on the steps №2-7
        """
        pass

    def test_013_log_in_user_withsekcurrency(self):
        """
        DESCRIPTION: Log in user with **SEK **currency
        EXPECTED: User is logged in successfully
        """
        pass

    def test_014_repeat_steps_2_6(self):
        """
        DESCRIPTION: Repeat steps №2-6
        EXPECTED: The same as on the steps №2-7
        """
        pass

    def test_015_repeat_test_case_on_settle_bets(self):
        """
        DESCRIPTION: Repeat test case on Settle Bets
        EXPECTED: 
        """
        pass
