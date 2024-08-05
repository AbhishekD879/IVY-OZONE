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
class Test_C59551010_Verify_display_of_fallback_scoreboard_for_inplay_table_tennis_event_when_events_are_not_subscribed_to_Betradar_Scoreboards(Common):
    """
    TR_ID: C59551010
    NAME: Verify display of fallback scoreboard for inplay table tennis event when event(s) are not subscribed to Betradar Scoreboards
    DESCRIPTION: 
    PRECONDITIONS: Make sure you have LIVE Table Tennis event which is not subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to In play-> Table Tennis Event Landing Page
    """
    keep_browser_open = True

    def test_001_navigate_to_event_landing_page_of_live_events_as_per_the_pre_conditions(self):
        """
        DESCRIPTION: Navigate to Event Landing Page of live events as per the pre-conditions
        EXPECTED: Event Landing page should be opened with live events
        """
        pass

    def test_002_verify_scoreboard_for_an_in_play_event_in_in_play_landing_page(self):
        """
        DESCRIPTION: Verify scoreboard for an in play event in in play Landing Page
        EXPECTED: Team names(Player) with live icon(Coral below to team names and Lads above to player name) should display
        EXPECTED: Fall back score board with live score should display
        EXPECTED: Ball indication(Coral beside player name and Lads beside to fallback scoreboard) should display
        EXPECTED: Odds should update as per feed from OB
        EXPECTED: markets with clickable links should display
        EXPECTED: Coral - # of markets with clickable link should display
        EXPECTED: Lads - # of markets with more link
        """
        pass

    def test_003_click_and_open_the_same_event(self):
        """
        DESCRIPTION: Click and open the same event
        EXPECTED: Event Details Page should be opened with fall back score board
        """
        pass

    def test_004_verify_scoreboard_in_edp_page(self):
        """
        DESCRIPTION: Verify Scoreboard in EDP page
        EXPECTED: + Event Name with 'Live' icon, date and time format(day,dd-MMM-YY HH:MM) is displayed in EDP header
        EXPECTED: + Only Scoreboard with player names is shown without any visualization
        """
        pass
