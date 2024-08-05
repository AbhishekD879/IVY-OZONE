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
class Test_C59551023_Verify_volleyball_Inplay_event_Set_Point(Common):
    """
    TR_ID: C59551023
    NAME: Verify volleyball Inplay event:  Set Point
    DESCRIPTION: This test case verifies display of SET point of an inplay event with betradar visualization
    PRECONDITIONS: Make sure you have volleyball Inplay event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to Inplay-> volleyball -> Tap on event (which is subscribed to betradar)
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

    def test_002_verify_display_of_set_point(self):
        """
        DESCRIPTION: Verify display of SET POINT
        EXPECTED: SET POINT message should be shown below for away player/above for home player the corresponding player name.
        EXPECTED: In a situation where the corresponding player will win the SET by winning the next point
        """
        pass
