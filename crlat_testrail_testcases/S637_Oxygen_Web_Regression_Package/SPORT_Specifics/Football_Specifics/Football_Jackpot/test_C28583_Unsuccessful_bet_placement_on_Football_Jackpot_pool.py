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
class Test_C28583_Unsuccessful_bet_placement_on_Football_Jackpot_pool(Common):
    """
    TR_ID: C28583
    NAME: Unsuccessful bet placement on Football 'Jackpot' pool
    DESCRIPTION: This test case verifies unhappy path and error handling of bet placement on Football Jackpot pool
    PRECONDITIONS: *   Football Jackpot pool is available
    PRECONDITIONS: *   User is logged out
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

    def test_002_log_in_with_valid_credentials(self):
        """
        DESCRIPTION: Log in with valid credentials
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

    def test_005_make_at_least_15_selection_at_least_1_from_each_event_using_lucky_dip_option_or_manually(self):
        """
        DESCRIPTION: Make at least 15 selection (at least 1 from each event) using 'Lucky Dip' option or manually
        EXPECTED: *   Selections that were made are highlighted
        EXPECTED: *   'Bet Now' button is enabled
        """
        pass

    def test_006_make_sure_that_total_stake_value_is_higher_than_user_balance(self):
        """
        DESCRIPTION: Make sure that 'Total Stake' value is higher than user balance
        EXPECTED: All selections and fields values are shown correctly
        """
        pass

    def test_007_tap_bet_now_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' button
        EXPECTED: 'Bet is not placed due to insufficient funds. Please make a deposit' (deposit links to 'deposit/registered) message is shown above the 'Clear All Selections' and 'Bet Now' buttons
        """
        pass

    def test_008_repeat_steps_2_5(self):
        """
        DESCRIPTION: Repeat steps №2-5
        EXPECTED: 
        """
        pass

    def test_009_triggerwait_until_bet_placement_on_displayed_pool_will_be_canceled_by_provider_or_services_will_not_respond(self):
        """
        DESCRIPTION: Trigger/Wait until bet placement on displayed pool will be canceled by provider or services will not respond
        EXPECTED: Corresponding error message returned from the server is shown
        """
        pass
