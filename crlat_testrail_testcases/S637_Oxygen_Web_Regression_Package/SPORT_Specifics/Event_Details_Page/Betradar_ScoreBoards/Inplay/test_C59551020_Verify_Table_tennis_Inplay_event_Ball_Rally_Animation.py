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
class Test_C59551020_Verify_Table_tennis_Inplay_event_Ball_Rally_Animation(Common):
    """
    TR_ID: C59551020
    NAME: Verify Table tennis Inplay event: Ball Rally Animation
    DESCRIPTION: This test case verifies ball rally animation of an inplay event with betradar visualization
    PRECONDITIONS: Make sure you have Table Tennis Inplay event which is subscribed to Betradar Scoreboards
    PRECONDITIONS: Navigate to Inplay-> Table Tennis -> Tap on event (which is subscribed to betradar)
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

    def test_002_verify_ball_animation_during_the_serve(self):
        """
        DESCRIPTION: Verify ball animation during the serve
        EXPECTED: + Ball is jumping from the serving player/team side for 2 seconds
        EXPECTED: + Ball rally animation is starting and going until the point is scored
        """
        pass

    def test_003_verify_ball_rally_animation(self):
        """
        DESCRIPTION: Verify ball rally animation
        EXPECTED: Table Tennis ball flies over to net from player side.
        """
        pass

    def test_004_verify_ball_animation_when_server_winning_the_point(self):
        """
        DESCRIPTION: Verify ball animation when Server winning the point
        EXPECTED: Rally animation is stopped to Receiver side if server won the point and restarts serving.
        """
        pass

    def test_005_verify_ball_animation_when_server_losing_the_point(self):
        """
        DESCRIPTION: Verify ball animation when Server losing the point
        EXPECTED: Rally animation is stopped on Server side if server lost the point
        """
        pass

    def test_006_verify_ball_animation_when_server_losing_the_point_before_rally_animation_starting(self):
        """
        DESCRIPTION: Verify ball animation when Server losing the point before rally animation starting
        EXPECTED: + Bouncing ball animation should be running
        EXPECTED: + Ball doesn't fly to opponent side
        EXPECTED: + Ball disappears after finishing Bouncing ball animation
        """
        pass
