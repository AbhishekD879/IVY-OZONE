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
class Test_C64569662_Verify_the_display_of_Player_Bets_on_their_own_accordions(Common):
    """
    TR_ID: C64569662
    NAME: Verify the display of Player Bets on their own accordions
    DESCRIPTION: Verify the display of Player Bets on their own accordions
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
        EXPECTED: EDP should be displayed with BYB/BB tab
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB tab
        EXPECTED: BYB/BB tab should be displayed with all the Markets
        """
        pass

    def test_004_validate_the_display_of_player_bets(self):
        """
        DESCRIPTION: Validate the display of Player Bets
        EXPECTED: * Player Bets should no longer be displayed in dropdown view
        EXPECTED: * Player Bets should be displayed in their own accordions
        EXPECTED: * Player Total Assists
        EXPECTED: * Player Total Passes
        EXPECTED: * Player Total Shots
        EXPECTED: * Player Total Shots on Target
        EXPECTED: * Player Total Tackles
        EXPECTED: * Player Shots Outside the box
        EXPECTED: * Offside
        EXPECTED: * Player Total Goals
        EXPECTED: * Goals Inside the box
        EXPECTED: * Goals Outside the box
        """
        pass

    def test_005_validate_the_display_order_of_players(self):
        """
        DESCRIPTION: Validate the display order of Players
        EXPECTED: * Players should be displayed as per 5-A side Order
        EXPECTED: * Player with highest stats should be displayed first
        """
        pass
