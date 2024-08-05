import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C12834168_Opta_Scoreboard(Common):
    """
    TR_ID: C12834168
    NAME: Opta Scoreboard
    DESCRIPTION: This test case verifies In-Play Football event that is subscribed to Opta and has available Scoreboard & Visualization
    DESCRIPTION: To map Opta Scoreboard to an OB event:
    DESCRIPTION: https://confluence.egalacoral.com/display/SPI/Opta+Scoreboard+mapping+to+an+OB+event
    PRECONDITIONS: In-Play Football event subscribed to Opta Scoreboards (to be sure if Opta Scoreboard mapped to event please check Request URL:
    PRECONDITIONS: https://com-[ENV].api.datafabric.dev.aws.ladbrokescoral.com/sdm/stats/inplay/CORAL/[EVENT_ID]/?api-key=[API_KEY] >> Status Code: 200
    PRECONDITIONS: https://api.strategicdatahub.com/events/bymapping/CORAL/[event_id] >> Status Code: 200)
    """
    keep_browser_open = True

    def test_001_navigate_to_the_inplay_football_event_details_page_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the Inplay Football event details page from Preconditions
        EXPECTED: Event details page is opened
        """
        pass

    def test_002_swipe_through_opta_scoreboard_screens(self):
        """
        DESCRIPTION: Swipe through Opta Scoreboard screens
        EXPECTED: User is able to navigate between Opta Scoreboard screens
        """
        pass

    def test_003_verify_opta_scoreboard_screens(self):
        """
        DESCRIPTION: Verify Opta Scoreboard screens
        EXPECTED: - 'Live Team Stats' screen
        EXPECTED: - 'Total Shots' screen
        EXPECTED: - 'Visualization' screen
        """
        pass

    def test_004_verify_live_team_stats_screen(self):
        """
        DESCRIPTION: Verify 'Live Team Stats' screen
        EXPECTED: 'Live Team Stats' screen:
        EXPECTED: - 'Possession' bar graph
        EXPECTED: - 'Dangerous Attacks' bar graph
        EXPECTED: - 'Shots on Target' bar graph
        EXPECTED: - 'Corners' bar graph
        EXPECTED: - Cards count (yellow/red) for each team
        EXPECTED: For an In-Play event that has not yet started: For 'Possession' 50% for both teams. For the rest 50/50 with 0 values
        """
        pass

    def test_005_verify_total_shots_screen(self):
        """
        DESCRIPTION: Verify 'Total Shots' screen
        EXPECTED: - 'Total Shots' with downward clickable chevron
        EXPECTED: - Top three player's details (home team on the left, away team on the right)
        EXPECTED: - # of shots next to each player
        EXPECTED: - Bar graph below each player
        EXPECTED: Pre Match event that has just become In-Play: Total Shots text with bars for both teams at 50% in inactive state with text N/A
        """
        pass

    def test_006_verify_visualization_screen(self):
        """
        DESCRIPTION: Verify 'Visualization' screen
        EXPECTED: Incidents are being shown
        """
        pass

    def test_007_verify_live_updates_in_real_time_for_all_opta_scoreboard_screens(self):
        """
        DESCRIPTION: Verify live updates in real time for all Opta Scoreboard screens
        EXPECTED: Bar graph stats and card counts are updating in real time via live feeds from opta >> Scoreboard event (Console)
        """
        pass
