import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C59551019_Verify_Fallback_scoreboard_visualization_of_table_tennis_EDP_when_betradar_scoreboard_is_enabled_in_CMS_but_the_event_is_not_subscribed_to_betradar_scoreboard(Common):
    """
    TR_ID: C59551019
    NAME: Verify Fallback scoreboard & visualization of table tennis EDP when betradar scoreboard is enabled in CMS but the event is not subscribed to betradar scoreboard
    DESCRIPTION: Test case verifies the view of Scoreboard & Visualization in EDP when Betradar Scoreboard is enabled in CMS but event is not subscribed to betradar scoreboard
    PRECONDITIONS: 1. Betradar scoreboard should enabled in CMS - system configuration - config - Betradar scoreboard
    PRECONDITIONS: 2. In play Table tennis event(s) should present and not subscribe to betradar scoreboard
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_navigate_to_table_tennis_from_home___table_tennis___inplay(self):
        """
        DESCRIPTION: Launch the application and navigate to table tennis from Home - table tennis - inplay
        EXPECTED: Table tennis inplay landing page should display
        """
        pass

    def test_002_verify_inplay_landing_page(self):
        """
        DESCRIPTION: Verify inplay landing page
        EXPECTED: League wise inplay events should display
        EXPECTED: 1. Team names(Player) with live icon(Coral below to team names and Lads above to player name) should display
        EXPECTED: 2. Live score should display
        EXPECTED: 3. Ball indication(Coral beside player name and Lads beside to scores) should display
        EXPECTED: 4. Odds should update as per feed from OB
        EXPECTED: 5. markets with clickable links should display
        EXPECTED: Coral - no of markets with clickable link should display
        EXPECTED: Lads - no of markets with more link
        """
        pass

    def test_003_click_on_any_inplay_event_which_is_not_subscribed_to_betradar_scoreboard_and_verify_tbd(self):
        """
        DESCRIPTION: click on any inplay event which is not subscribed to betradar scoreboard and verify [TBD]
        EXPECTED: 1. Event name with back icon at top left corner and live icon event time and date should display
        EXPECTED: 2. Fallback scoreboard should display (G and P table g = no of sets won p = score of current set)
        EXPECTED: 3. Scoreboard should updated as per feed
        EXPECTED: 4. below to the scoreboard all the markets should display with respective odds
        EXPECTED: Refer screenshot for fallback scoreboard
        EXPECTED: ![](index.php?/attachments/get/105783184)
        """
        pass
