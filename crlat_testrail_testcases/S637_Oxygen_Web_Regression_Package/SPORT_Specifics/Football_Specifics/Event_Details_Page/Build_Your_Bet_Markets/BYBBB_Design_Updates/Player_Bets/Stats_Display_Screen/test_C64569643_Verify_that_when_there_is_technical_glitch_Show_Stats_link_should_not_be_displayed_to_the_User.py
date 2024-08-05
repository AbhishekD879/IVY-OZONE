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
class Test_C64569643_Verify_that_when_there_is_technical_glitch_Show_Stats_link_should_not_be_displayed_to_the_User(Common):
    """
    TR_ID: C64569643
    NAME: Verify that when there is technical glitch Show Stats link should not be displayed to the User
    DESCRIPTION: This test case verifies when there is technical glitch Show Stats link should not be displayed
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

    def test_005_validate_the_show_stats_link_when_there_is_technical_glitch(self):
        """
        DESCRIPTION: Validate the Show Stats link when there is technical glitch
        EXPECTED: * Show Stats link should not be displayed to the user
        """
        pass
