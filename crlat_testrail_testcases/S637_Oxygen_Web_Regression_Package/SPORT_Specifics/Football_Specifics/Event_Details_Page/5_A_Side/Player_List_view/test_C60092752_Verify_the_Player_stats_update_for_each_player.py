import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C60092752_Verify_the_Player_stats_update_for_each_player(Common):
    """
    TR_ID: C60092752
    NAME: Verify the Player stats update for each player
    DESCRIPTION: Verify that on selecting a market name from the drop down player stats are updated accordingly
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> 'FiveASide'
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: - Formations are added in CMS -> BYB -> 5 A Side
    PRECONDITIONS: - Static block 'five-a-side-launcher' is created and enabled in CMS > Static Blocks
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_app(self):
        """
        DESCRIPTION: Launch Ladbrokes app
        EXPECTED: User should be able launch the application successfully
        """
        pass

    def test_002_navigate_to_football(self):
        """
        DESCRIPTION: Navigate to Football
        EXPECTED: User should be navigated to Football landing page
        """
        pass

    def test_003_navigate_to_any_football_event_that_has_5_a_side_available(self):
        """
        DESCRIPTION: Navigate to any football event that has 5-A side available
        EXPECTED: User should be navigated to EDP
        """
        pass

    def test_004_navigate_to_5_a_side_tab(self):
        """
        DESCRIPTION: Navigate to 5-A Side tab
        EXPECTED: User should be navigated to 5-A Side tab
        """
        pass

    def test_005_click_on_build_a_team(self):
        """
        DESCRIPTION: Click on Build a Team
        EXPECTED: 1: Pitch View should be displayed
        EXPECTED: 2: Balanced formation should be selected by default
        EXPECTED: 3: User should be able to select any formation displayed in the pitch view
        """
        pass

    def test_006_click_on_plus_icon_from_any_player_position(self):
        """
        DESCRIPTION: Click on + icon from any player position
        EXPECTED: 1: User should be navigated to select a player page
        EXPECTED: 2: Add a <Position> should be displayed
        EXPECTED: 3: < Back button should be displayed
        EXPECTED: 4: Market name should be displayed in blue with chevron
        """
        pass

    def test_007_click_on_the_chevron(self):
        """
        DESCRIPTION: Click on the chevron
        EXPECTED: 1: Drop down should be displayed with all market names
        EXPECTED: 2: User should be able to select any market name
        """
        pass

    def test_008_validate_the_player_stats_updated_as_per_the_market_selected(self):
        """
        DESCRIPTION: Validate the player stats updated as per the market selected
        EXPECTED: 1: Player stats should be updated as per the market selected for all the players in the player list
        EXPECTED: 2: Change the market name and verify that player stats are updated- Player stats should be updated
        """
        pass
