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
class Test_C59551030_Verify_Betradar_Inplay_visualization_widget(Common):
    """
    TR_ID: C59551030
    NAME: Verify Betradar Inplay visualization widget
    DESCRIPTION: This test case verifies Betradar Inplay widget
    PRECONDITIONS: Make sure you have Table Tennis In play event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to In play-> Table Tennis -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
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
        EXPECTED: + Player names with score
        EXPECTED: + Scoreline with blue bar
        EXPECTED: + Table Tennis Pitch with ball rally animation
        """
        pass

    def test_003_verify_display_of_player_names_and_score(self):
        """
        DESCRIPTION: Verify display of player names and score
        EXPECTED: Player Information should be displayed in the following order:
        EXPECTED: + Player1 First and Last name
        EXPECTED: + Score (say SET1  2:1)
        EXPECTED: + Player2 First and Last name
        """
        pass

    def test_004_verify_display_of_scoreline(self):
        """
        DESCRIPTION: Verify display of scoreline
        EXPECTED: 1. Under Player names a section should be displayed with blue line as below:
        EXPECTED: + Player1 and player2 short names
        EXPECTED: + Bluebar is displayed with scores and which SET(dropdown) is
        EXPECTED: currently playing
        EXPECTED: 2. Switch to another tab in the same section where score board is displayed as below:
        EXPECTED: + Player1 and Player 2 names
        EXPECTED: + Both Player Scores in each set
        EXPECTED: + Total sets played by both players
        EXPECTED: *High score in each set is shown in bold
        """
        pass

    def test_005_verify_display_of_table_tennis_court(self):
        """
        DESCRIPTION: Verify display of Table tennis court
        EXPECTED: + Pitch tab should be selected by default
        EXPECTED: + All animations on the pitch are fully visible
        EXPECTED: + Match score should be displayed whenever the player scores
        EXPECTED: + Respective Player names will be displayed in both sides of court diagonally
        """
        pass
