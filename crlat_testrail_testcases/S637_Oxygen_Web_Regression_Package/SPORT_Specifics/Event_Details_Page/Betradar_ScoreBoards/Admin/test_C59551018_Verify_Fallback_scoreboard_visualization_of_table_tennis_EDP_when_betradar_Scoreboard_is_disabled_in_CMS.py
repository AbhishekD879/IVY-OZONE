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
class Test_C59551018_Verify_Fallback_scoreboard_visualization_of_table_tennis_EDP_when_betradar_Scoreboard_is_disabled_in_CMS(Common):
    """
    TR_ID: C59551018
    NAME: Verify Fallback scoreboard & visualization of table tennis EDP when betradar Scoreboard is disabled in CMS
    DESCRIPTION: Test case verifies the view of Scoreboard & Visualization in EDP when Betradar Scoreboard is disabled in CMS
    PRECONDITIONS: 1. Betradar scoreboard should disabled in CMS - system configuration - config - Betradar Scoreboard
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
        EXPECTED: Table tennis inplay landing page should display
        """
        pass

    def test_002_verify_inplay_landing_page(self):
        """
        DESCRIPTION: Verify inplay landing page
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
        EXPECTED: 1. Event name with back icon at top left corner and live icon event time and date should display(for desktop only)
        EXPECTED: 2. Fallback scoreboard should display (G and P table g = no of sets won p = score of current set)
        EXPECTED: 3. Scoreboard should updated as per feed
        EXPECTED: 4. below to the scoreboard all the markets should display with respective odds
        EXPECTED: Refer screenshot for fallback scoreboard
        EXPECTED: ![](index.php?/attachments/get/105781532)
        """
        pass
