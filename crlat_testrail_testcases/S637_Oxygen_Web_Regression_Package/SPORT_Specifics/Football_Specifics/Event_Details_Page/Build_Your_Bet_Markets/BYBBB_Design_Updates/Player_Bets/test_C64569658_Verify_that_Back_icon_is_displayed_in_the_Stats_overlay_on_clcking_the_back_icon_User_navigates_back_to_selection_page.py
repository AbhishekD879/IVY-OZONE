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
class Test_C64569658_Verify_that_Back_icon_is_displayed_in_the_Stats_overlay_on_clcking_the_back_icon_User_navigates_back_to_selection_page(Common):
    """
    TR_ID: C64569658
    NAME: Verify that Back icon is displayed in the Stats overlay , on clcking the back icon User navigates back to selection page
    DESCRIPTION: This Test case verifies the display of Back icon
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
        EXPECTED: * Market should be Expanded and all Players should be displayed with Show More
        """
        pass

    def test_005_click_on_show_stats_link_displayed_under_any_player(self):
        """
        DESCRIPTION: Click on Show Stats link displayed under any player
        EXPECTED: * Show Stats Overlay should be displayed
        EXPECTED: * Back button should be displayed
        """
        pass

    def test_006_click_on_back_button(self):
        """
        DESCRIPTION: Click on Back button
        EXPECTED: * Overlay should be closed
        EXPECTED: * Players should be displayed
        """
        pass
