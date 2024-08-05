import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C59551016_Verify_betradar_Scoreboard_Visualization_of_table_tennis_EDP_when_Betradar_Scoreboard_is_enabled_in_CMS(Common):
    """
    TR_ID: C59551016
    NAME: Verify betradar Scoreboard & Visualization of table tennis EDP when Betradar Scoreboard is enabled in CMS
    DESCRIPTION: Test case verifies the view of Scoreboard & Visualization in EDP when Betradar Scoreboard is enabled in CMS
    PRECONDITIONS: 1. Betradar scoreboard should enable in CMS - system configuration - config - Betradar scoreboard
    PRECONDITIONS: 2. In play Table tennis event(s) should present and subscribed to betradar scoreboard
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_navigate_to_table_tennis_edp_from_home___table_tennis___inplay(self):
        """
        DESCRIPTION: Launch the application and navigate to table tennis EDP from Home - table tennis - inplay
        EXPECTED: table tennis events should display with player names, live icon, fallback scoreboard default markets odds and link with all other markets
        """
        pass

    def test_002_verify_table_tennis_inplay_landing_page(self):
        """
        DESCRIPTION: verify table tennis inplay landing page
        EXPECTED: League wise inplay events should display
        EXPECTED: 1. Team names(Player) with live icon(Coral below to team names and Lads above to player name) should display
        EXPECTED: 2. Fall back score board with live score should display
        EXPECTED: 3. Ball indication(Coral beside player name and Lads beside to fallback scoreboard) should display
        EXPECTED: 4. Odds should update as per feed from OB
        EXPECTED: 5. markets with clickable links should display
        EXPECTED: Coral - # of markets with clickable link should display
        EXPECTED: Lads - # of markets with more link
        """
        pass

    def test_003_click_on_any_inplay_event_and_verify(self):
        """
        DESCRIPTION: click on any inplay event and verify
        EXPECTED: 1. Event name with back icon at top left corner and live icon event time and date should display
        EXPECTED: 2. betradar scoreboard should display
        EXPECTED: 3. Scoreboard should updated as per the feed from betradar
        EXPECTED: 4. Below to the scoreboard all the markets should display with respective odds
        """
        pass

    def test_004_compare_scoreboard_in_both_the_brandslads_and_coral(self):
        """
        DESCRIPTION: Compare scoreboard in both the brands(Lads and Coral)
        EXPECTED: Score should match in both the screens and there should not any delay
        """
        pass