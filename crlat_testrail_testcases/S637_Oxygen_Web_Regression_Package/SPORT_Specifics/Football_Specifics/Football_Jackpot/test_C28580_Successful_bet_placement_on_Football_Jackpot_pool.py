import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C28580_Successful_bet_placement_on_Football_Jackpot_pool(Common):
    """
    TR_ID: C28580
    NAME: Successful bet placement on Football 'Jackpot' pool
    DESCRIPTION: This test case verifies happy path of bet placement on Football Jackpot pool
    DESCRIPTION: Automated:
    DESCRIPTION: Desktop - C2912208
    DESCRIPTION: Mobile - C2911739
    PRECONDITIONS: *   Football Jackpot pool is available
    PRECONDITIONS: *   User is logged in with valid account with enough balance to place a bet on Football Jackpot pool
    PRECONDITIONS: Note:
    PRECONDITIONS: Line - 15 selections, 1 from each event
    PRECONDITIONS: Total Lines - number of selected combinations of 15 match results
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapfootball_icon_on_the_sports_menu_ribbon(self):
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

    def test_003_tap_jackpot_tab(self):
        """
        DESCRIPTION: Tap 'Jackpot' tab
        EXPECTED: *   Football Jackpot Page is opened with 15 events available
        EXPECTED: *   Each event has 3 buttons
        """
        pass

    def test_004_make_at_least_15_selection_at_least_1_from_each_event_using_lucky_dip_option_or_manually(self):
        """
        DESCRIPTION: Make at least 15 selection (at least 1 from each event) using 'Lucky Dip' option or manually
        EXPECTED: *   Selections that were made are highlighted
        EXPECTED: *   'Total Lines' field counter is increased by number of formed lines
        EXPECTED: *   'Bet Now' button is enabled
        """
        pass

    def test_005_go_to_stake_per_line_drop_down_and_choose_amount_value(self):
        """
        DESCRIPTION: Go to 'Stake Per Line' drop-down and choose amount value
        EXPECTED: Chosen amount is displayed in drop-down
        """
        pass

    def test_006_verify_total_stake_value(self):
        """
        DESCRIPTION: Verify 'Total Stake' value
        EXPECTED: Shown value is automatically updated as the user updates the 'Total Lines' or 'Stake Per Line' values
        """
        pass

    def test_007_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: *   Bet is successfully placed
        EXPECTED: *   User balance is decreased accordingly to 'Total Stake' value
        EXPECTED: *   Football Jackpot bet is handled in page (i.e. wholly independently of bet slip)
        """
        pass
