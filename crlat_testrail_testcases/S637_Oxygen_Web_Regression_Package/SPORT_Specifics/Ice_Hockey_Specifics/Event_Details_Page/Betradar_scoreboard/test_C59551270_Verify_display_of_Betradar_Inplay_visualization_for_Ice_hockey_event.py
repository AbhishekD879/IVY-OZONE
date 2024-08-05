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
class Test_C59551270_Verify_display_of_Betradar_Inplay_visualization_for_Ice_hockey_event(Common):
    """
    TR_ID: C59551270
    NAME: Verify display of Betradar Inplay visualization  for Ice hockey event
    DESCRIPTION: This test case verifies Betradar Inplay widget for Ice hockey.
    DESCRIPTION: How to check event is mapped to betradar or not?
    DESCRIPTION: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    DESCRIPTION: Confluence link:
    DESCRIPTION: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    PRECONDITIONS: Make sure you have Ice hockey In play event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to In play-> Ice hockey -> Tap on event (which is subscribed to betradar)
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_inplay_event_as_per_the_pre_conditions(self):
        """
        DESCRIPTION: Navigate to Event Details Page of Inplay event as per the pre-conditions
        EXPECTED: Event Details Page should be opened with match visualization and scoreboards.
        """
        pass

    def test_002_verify_inplay_widget_for_betradar_scoreboard(self):
        """
        DESCRIPTION: Verify Inplay widget for Betradar scoreboard
        EXPECTED: Betradar Inplay widget should contains following sections:
        EXPECTED: + Team names with score
        EXPECTED: + Scoreline with blue bar
        EXPECTED: + Ice hockey Pitch with puck moving animation
        """
        pass

    def test_003_verify_display_of_player_names_and_score(self):
        """
        DESCRIPTION: Verify display of player names and score
        EXPECTED: Player Information should be displayed in the following order:
        EXPECTED: + Team1 name
        EXPECTED: + Goal Score (say 2:1)
        EXPECTED: + Team2 name
        """
        pass

    def test_004_verify_display_of_scoreline(self):
        """
        DESCRIPTION: Verify display of scoreline
        EXPECTED: 1. Under Team names a section should be displayed with blue line as below:
        EXPECTED: + Team1 and Team2 short names
        EXPECTED: + Bluebar is displayed with goals, suspensions, timeouts at certain time intervals along with team name
        EXPECTED: 2. Switch to another tab in the same section where score board is displayed as below:
        EXPECTED: + team1 and team2 names
        EXPECTED: + Both team Scores in each half
        EXPECTED: + Total scored by both players
        EXPECTED: *High score in each half is shown in bold
        """
        pass

    def test_005_verify_display_of_ice_hockey_court(self):
        """
        DESCRIPTION: Verify display of Ice Hockey court
        EXPECTED: + Pitch tab should be selected by default
        EXPECTED: + All animations on the pitch are fully visible
        EXPECTED: + Goal score should be displayed whenever the player scores
        EXPECTED: + Respective Player names will be displayed in both sides of court diagonally
        """
        pass
