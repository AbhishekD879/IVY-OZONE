import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C64569677_Verify_when_user_clicks_Show_Stats_it_should_be_GA_tag(Common):
    """
    TR_ID: C64569677
    NAME: Verify when user clicks  ‘Show Stats’ it should be GA tag
    DESCRIPTION: This test case verifies when user click on show stats is Ga Tracked
    PRECONDITIONS: 1: Banach events should be available with all or ANY of the Markets
    """
    keep_browser_open = True

    def test_001_launch_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral application
        EXPECTED: User should be able to launch the application successfully
        """
        pass

    def test_002_navigate_to_football_edp(self):
        """
        DESCRIPTION: Navigate to Football EDP
        EXPECTED: * User should be navigated to EDP
        EXPECTED: * Build Your Bet /Bet Builder tab should be displayed
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: * BYB/BB tab should be displayed
        EXPECTED: * Filters should be displayed
        EXPECTED: * All Markets tab should be displayed by default
        """
        pass

    def test_004_click_on_any_of_the_player_market_either_from_all_markets_filter_or_player_bets_filtergoalsgoals_inside_the_boxgoals_outside_the_boxoffsidespassesshotsshots_on_targetshots_outside_the_box(self):
        """
        DESCRIPTION: Click on ANY of the Player Market either from All Markets filter or Player Bets filter
        DESCRIPTION: Goals
        DESCRIPTION: Goals inside the box
        DESCRIPTION: Goals outside the box
        DESCRIPTION: Offsides
        DESCRIPTION: Passes
        DESCRIPTION: Shots
        DESCRIPTION: Shots on target
        DESCRIPTION: Shots outside the box
        EXPECTED: * Market should be expanded
        EXPECTED: * Players should be displayed
        """
        pass

    def test_005_click_on_show_stats_below_the_player(self):
        """
        DESCRIPTION: Click on Show Stats below the player
        EXPECTED: * Stats Overlay should be displayed
        """
        pass

    def test_006_validate_ga_tracking_in_console_on_interaction_with_show_stats_for_the_player(self):
        """
        DESCRIPTION: Validate Ga Tracking in console on interaction with 'Show Stats' for the player
        EXPECTED: * Show Stats for the player is Ga tagged
        EXPECTED: ![](index.php?/attachments/get/74d5fb60-720c-487e-8e05-6f6656523439)
        """
        pass
