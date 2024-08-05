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
class Test_C64569657_Verify_that_on_Clicking_Show_Stats_user_is_displayed_the_Stats_of_that_Player(Common):
    """
    TR_ID: C64569657
    NAME: Verify that on Clicking 'Show Stats' user is displayed the Stats of that Player
    DESCRIPTION: Test case verifies 'Show Stats' is displayed the Stats of that Player
    PRECONDITIONS: 1: BYB/BB Markets should be available for the event
    PRECONDITIONS: 2: Player Bets should be available for the event
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
        EXPECTED: EDP should be displayed with BYB/BB Markets
        """
        pass

    def test_003_click_on_bybbb_tab(self):
        """
        DESCRIPTION: Click on BYB/BB Tab
        EXPECTED: BYB/BB should be displayed with all the Markets
        """
        pass

    def test_004_navigate_to_any_of_the_player_markets_and_expand(self):
        """
        DESCRIPTION: Navigate to any of the Player Markets and Expand
        EXPECTED: Market should be Expanded and all Players should be displayed with Show More
        """
        pass

    def test_005_validate_show_stats_link(self):
        """
        DESCRIPTION: Validate Show Stats Link
        EXPECTED: * Show Stats should be displayed below Player name for all players and for all Player Markets
        """
        pass
