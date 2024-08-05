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
class Test_C60079295_Verify_Volleyball_Inplay_event_Match_Point(Common):
    """
    TR_ID: C60079295
    NAME: Verify  Volleyball Inplay event: Match Point
    DESCRIPTION: This test case verifies display of match point of an inplay event with betradar visualization
    PRECONDITIONS: Make sure you have Volleyball Inplay event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to Inplay-> Volleyball -> Tap on event (which is subscribed to betradar)
    PRECONDITIONS: How to check whether event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar scoreboard and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_inplay_event_as_per_the_pre_conditions(self):
        """
        DESCRIPTION: Navigate to Event Details Page of Inplay event as per the pre-conditions
        EXPECTED: Event Details Page should be opened with match visualization and scoreboards
        """
        pass

    def test_002_verify_display_of_match_point(self):
        """
        DESCRIPTION: Verify display of MATCH POINT
        EXPECTED: MATCH POINT message should be shown below the corresponding player name
        EXPECTED: In a situation where the corresponding player will win the match by winning the next point
        """
        pass
