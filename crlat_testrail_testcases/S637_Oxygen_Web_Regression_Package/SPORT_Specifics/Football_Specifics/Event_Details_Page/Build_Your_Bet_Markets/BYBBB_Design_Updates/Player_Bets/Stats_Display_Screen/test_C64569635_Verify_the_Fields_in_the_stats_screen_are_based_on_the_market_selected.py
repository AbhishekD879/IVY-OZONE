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
class Test_C64569635_Verify_the_Fields_in_the_stats_screen_are_based_on_the_market_selected(Common):
    """
    TR_ID: C64569635
    NAME: Verify the Fields in the stats screen are based on the market selected
    DESCRIPTION: This test case verifies the stats screen based on market selected
    PRECONDITIONS: 1: In CMS &gt; BYB &gt; BYB Markets -Markets should be Configure in CMS
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
        EXPECTED: ![](index.php?/attachments/get/965d69de-ccaf-4eb2-9731-7d355af90880)
        """
        pass

    def test_007_validate_the_labels_displayed(self):
        """
        DESCRIPTION: Validate the Labels displayed
        EXPECTED: Labels should be displayed as per the Market from which Show Stats link is clicked
        """
        pass