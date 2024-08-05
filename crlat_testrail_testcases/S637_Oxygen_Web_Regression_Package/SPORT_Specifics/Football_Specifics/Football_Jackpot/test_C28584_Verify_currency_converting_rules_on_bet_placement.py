import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28584_Verify_currency_converting_rules_on_bet_placement(Common):
    """
    TR_ID: C28584
    NAME: Verify currency converting rules on bet placement
    DESCRIPTION: This test case verifies currency converting rules when user places bet on Football Jackpot pool using accounts with different currencies set.
    PRECONDITIONS: Make sure you have 4 registered users with positive balance and different currency settings: **GBP**, **EUR**, **USD**, **SEK**
    PRECONDITIONS: In order to verify currency symbol use:
    PRECONDITIONS: *   'GBP': symbol = '**£**';
    PRECONDITIONS: *   'USD': symbol = '**$**';
    PRECONDITIONS: *   'EUR': symbol = '**€'**;
    PRECONDITIONS: *   'SEK': symbol = '**Kr**'
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_log_in_with_valid_user_account_where_gbp_currency_is_set(self):
        """
        DESCRIPTION: Log in with valid user account where **GBP **currency is set
        EXPECTED: User is successfully logged in
        """
        pass

    def test_003_tapfootball_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Football' icon on the Sports Menu Ribbon
        EXPECTED: **Desktop**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches'->'Today' sub tab is opened by default
        EXPECTED: **Mobile**:
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * 'Matches' tab is opened by default
        """
        pass

    def test_004_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: *   Football Jackpot Page is opened with 15 events available
        EXPECTED: *   Each event has 3 buttons
        """
        pass

    def test_005_verify_currency_symbols_in_stake_per_line_drop_down_and_total_stake_fields(self):
        """
        DESCRIPTION: Verify currency symbols in 'Stake Per Line' drop-down and 'Total Stake' fields
        EXPECTED: All currency symbols at any time are:
        EXPECTED: GBP: symbol = '**£**';
        """
        pass

    def test_006_make_at_least_15_selection_at_least_1_from_each_event_using_lucky_dip_option_or_manually(self):
        """
        DESCRIPTION: Make at least 15 selection (at least 1 from each event) using 'Lucky Dip' option or manually
        EXPECTED: *   Selections that were made are highlighted
        EXPECTED: *   'Bet Now' button is enabled
        """
        pass

    def test_007_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   Bet is successfully placed
        EXPECTED: *   User balance is decreased accordingly to 'Total Stake' value
        """
        pass

    def test_008_log_in_with_valid_user_account_where_eurcurrency_is_set(self):
        """
        DESCRIPTION: Log in with valid user account where **EUR **currency is set
        EXPECTED: User is successfully logged in
        """
        pass

    def test_009_repeat_steps_3_6(self):
        """
        DESCRIPTION: Repeat steps №3-6
        EXPECTED: 
        """
        pass

    def test_010_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   Bet is successfully placed
        EXPECTED: *   User balance is decreased accordingly to converted 'Total Stake' value from GBP to user's currency using the exchange rates setup in back office (**UAT team to provide**)
        """
        pass

    def test_011_log_in_with_valid_user_account_where_usdcurrency_is_set(self):
        """
        DESCRIPTION: Log in with valid user account where **USD **currency is set
        EXPECTED: User is successfully logged in
        """
        pass

    def test_012_repeat_steps_9_10(self):
        """
        DESCRIPTION: Repeat steps №9-10
        EXPECTED: 
        """
        pass

    def test_013_log_in_with_valid_user_account_where_sekcurrency_is_set(self):
        """
        DESCRIPTION: Log in with valid user account where **SEK **currency is set
        EXPECTED: User is successfully logged in
        """
        pass

    def test_014_repeat_steps_9_10(self):
        """
        DESCRIPTION: Repeat steps №9-10
        EXPECTED: 
        """
        pass
