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
class Test_C59551011_Verify_Inplay_event_Fallback_score_board(Common):
    """
    TR_ID: C59551011
    NAME: Verify Inplay event : Fallback score board
    DESCRIPTION: Test case verifies fallback scoreboard for inplay table tennis event which is not subscribed to betradar scoreboard
    PRECONDITIONS: 1. Inplay event should not subscribe to betradar scoreboard or betradar toggle should OFF in CMS
    PRECONDITIONS: 2. Inplay event should subscribe to fallback scoreboard and fallback toggle should ON in CMS
    PRECONDITIONS: Navigate to In play-> Table Tennis -> Tap on any live event
    """
    keep_browser_open = True

    def test_001_navigate_to_table_tennis_inplay_event_landing_page_as_per_the_pre_conditions(self):
        """
        DESCRIPTION: Navigate to table tennis inplay event landing page as per the pre conditions
        EXPECTED: All the inplay events should display fallback scoreboard in event landing page with live icon and current set name playing
        """
        pass

    def test_002_click_on_event_and_verify_scoreboard(self):
        """
        DESCRIPTION: click on event and verify scoreboard
        EXPECTED: + Event Name with 'Live' icon(Desktop), date and time format(day,dd-MMM-YY HH:MM) is displayed in EDP header
        EXPECTED: + Fallback scoreboard should display without any visualization
        EXPECTED: + Scores should be displayed as same as event landing page
        EXPECTED: + Scoreboard should updated as per results
        """
        pass
