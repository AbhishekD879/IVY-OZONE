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
class Test_C60079294_Verify_Volleyball_Inplay_event_Player_Serve_Animation_of_different_types(Common):
    """
    TR_ID: C60079294
    NAME: Verify Volleyball Inplay event: Player Serve Animation of different types
    DESCRIPTION: This test case verifies player serve animation of an inplay event with betradar visualization
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

    def test_002_verify_serve_animation_of_double_hitting(self):
        """
        DESCRIPTION: Verify serve animation of Double hitting
        EXPECTED: Ball flies when the same player hits the ball twice in a row
        """
        pass

    def test_003_verify_serve_animation_of_fault_point_type(self):
        """
        DESCRIPTION: Verify serve animation of **Fault** point type
        EXPECTED: Ball flies to the net, stops in front of the net on server side and falls down
        """
        pass
