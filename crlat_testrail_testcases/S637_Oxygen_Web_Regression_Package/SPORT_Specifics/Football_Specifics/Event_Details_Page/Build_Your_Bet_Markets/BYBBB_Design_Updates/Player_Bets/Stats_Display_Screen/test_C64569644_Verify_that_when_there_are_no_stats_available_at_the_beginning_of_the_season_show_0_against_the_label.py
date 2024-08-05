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
class Test_C64569644_Verify_that_when_there_are_no_stats_available_at_the_beginning_of_the_season_show_0_against_the_label(Common):
    """
    TR_ID: C64569644
    NAME: Verify that when there are no stats available at the beginning of the season show '0' against the label
    DESCRIPTION: This test case verifies when there are no stats available form the beginning of the season shows '0'
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets -Markets should be Configure in CMS
    PRECONDITIONS: Goals
    PRECONDITIONS: Goals inside the box
    PRECONDITIONS: Goals outside the box
    PRECONDITIONS: Offsides
    PRECONDITIONS: Passes
    PRECONDITIONS: Shots
    PRECONDITIONS: Shots on target
    PRECONDITIONS: Shots outside the box
    PRECONDITIONS: 2: Banach events should be available with all or ANY of the Markets
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

    def test_006_validate_the_stats_screen(self):
        """
        DESCRIPTION: Validate the Stats screen
        EXPECTED: * Back button should be displayed
        EXPECTED: * Stats screen should be similar to 5-A side Player Stats Screen
        EXPECTED: * CSS styles should be as per Zeplin
        """
        pass

    def test_007_validate_the_labels_displayed(self):
        """
        DESCRIPTION: Validate the Labels displayed
        EXPECTED: Labels should be displayed as per the Market from which Show Stats link is clicked
        """
        pass

    def test_008_validate_the_stats_displayed_during_the_start_of_the_season_when_stats_are_not_available(self):
        """
        DESCRIPTION: Validate the Stats displayed during the start of the season when Stats are not available
        EXPECTED: '0' should be displayed beside the Label when there are no stats likely to be during the start of the season
        """
        pass

    def test_009_validate_the_back_button_displayed_on_stats_screen(self):
        """
        DESCRIPTION: Validate the back button displayed on Stats screen
        EXPECTED: * Back button should be displayed as per the Zeplin designs
        """
        pass

    def test_010_click_on_back_button_displayed_stats_screen(self):
        """
        DESCRIPTION: Click on back button displayed Stats screen
        EXPECTED: * Stats Overlay should be closed
        EXPECTED: * User should be back to previous page
        """
        pass
