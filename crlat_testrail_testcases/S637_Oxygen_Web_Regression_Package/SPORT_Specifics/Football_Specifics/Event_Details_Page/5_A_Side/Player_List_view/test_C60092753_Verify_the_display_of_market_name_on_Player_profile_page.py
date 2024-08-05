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
class Test_C60092753_Verify_the_display_of_market_name_on_Player_profile_page(Common):
    """
    TR_ID: C60092753
    NAME: Verify the display of market name on Player profile page
    DESCRIPTION: Verify that after selcting the market and adding the player name, player profile page displays the market name in blue with chevron
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

    def test_008_select_any_market(self):
        """
        DESCRIPTION: Select any market
        EXPECTED: 1: User should be able to select the market
        """
        pass

    def test_009_select_any_player_from_the_player_list(self):
        """
        DESCRIPTION: Select any player from the player list
        EXPECTED: 1: User should be able to choose the player and navigated to Player stats page
        EXPECTED: 2: Market name below the player name should be in blue with chevron
        EXPECTED: 3: User should be able to change the market name from the drop down
        EXPECTED: 4: User should be able to edit line ups by clicking on + or -
        """
        pass
