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
class Test_C59551313_Verify_Fallback_scoreboard_visualization_of_Futsal_EDP_when_bet_radar_scoreboard_is_enabled_in_CMS_but_the_event_is_not_subscribed_to_bet_radar_scoreboard(Common):
    """
    TR_ID: C59551313
    NAME: Verify Fallback scoreboard & visualization of Futsal EDP when bet radar scoreboard is enabled in CMS but the event is not subscribed to bet radar scoreboard
    DESCRIPTION: Test case verifies the view of Scoreboard & Visualization in EDP when Bet radar Scoreboard is enabled in CMS but event is not subscribed to bet radar scoreboard
    PRECONDITIONS: 1. Bet radar scoreboard should enabled in CMS - system configuration - config - Bet radar scoreboard
    PRECONDITIONS: 2. In play Table Futsal event(s) should present and not subscribe to bet radar scoreboard
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_navigate_to_table_tennis_edp_from_home___futsal___in_play(self):
        """
        DESCRIPTION: Launch the application and navigate to table tennis EDP from Home - Futsal - in play
        EXPECTED: Futsal events should display with player names, live icon, fallback scoreboard default markets odds and link with all other markets
        """
        pass

    def test_002_click_on_any_in_play_event_which_is_not_subscribed_to_bet_radar_scoreboard_and_verify_tbd(self):
        """
        DESCRIPTION: click on any in play event which is not subscribed to bet radar scoreboard and verify [TBD]
        EXPECTED: 1. Event name with back icon at top left corner and live icon event time and date should display
        EXPECTED: 2. Fallback scoreboard should display
        EXPECTED: 3. Scoreboard should updated as per results
        EXPECTED: 4. all the markets should display with respective odds
        """
        pass
