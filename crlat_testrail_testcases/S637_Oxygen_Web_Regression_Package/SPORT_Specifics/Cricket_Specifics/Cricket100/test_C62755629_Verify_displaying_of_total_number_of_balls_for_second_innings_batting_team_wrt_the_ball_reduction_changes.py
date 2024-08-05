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
class Test_C62755629_Verify_displaying_of_total_number_of_balls_for_second_innings_batting_team_wrt_the_ball_reduction_changes(Common):
    """
    TR_ID: C62755629
    NAME: Verify displaying of total number of balls for second innings batting team( wrt the ball reduction changes)
    DESCRIPTION: This testcase verifies displaying of total number of balls for second innings batting team( wrt the ball reduction changes)
    PRECONDITIONS: 1.Login to Application.
    PRECONDITIONS: 2.Event should be live.
    PRECONDITIONS: Note:
    PRECONDITIONS: When the 1st innings is going on - any change or reduction in total balls will be for both innings. In case if there is any change in the total balls for the 2nd innings- it will effect only the 2nd innings.
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage
        EXPECTED: User should be navigated to cricket 100.
        EXPECTED: -Matches tab should be  displayed by default
        """
        pass

    def test_002_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to in-play page.
        EXPECTED: In-play page should be loaded.
        """
        pass

    def test_003_click_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to_event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify whether the user is able to navigate to event details page (edp ).
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_scoreboard_in_event_details_page_edp_(self):
        """
        DESCRIPTION: Verify displaying of scoreboard in event details page (edp) .
        EXPECTED: Scoreboard should be displayed on event details page.
        """
        pass

    def test_005_verify_the_total_number_of_balls_for_the_first_innings__wrt_the_ball_reduction_changes(self):
        """
        DESCRIPTION: Verify the total number of balls for the first innings ( wrt the ball reduction changes)
        EXPECTED: If the 1st innings is reduced to 20 balls from 100 balls(initially it should display 100balls)
        EXPECTED: - after the Nth ball completion, it should be updated to 20 balls along with  the total balls bowled.
        EXPECTED: -the total number of balls should be updated to N/20 and the innings should be completed after 20 balls.
        """
        pass

    def test_006_verify_the_total_number_of_balls_for_second_innings(self):
        """
        DESCRIPTION: Verify the total number of balls for second innings
        EXPECTED: The 2nd innings should be started with 20 balls,but after Nth ball completion- it should be reduced to 10 balls.
        EXPECTED: -the total balls bowled and total number of balls should be changed to N/10.
        """
        pass
