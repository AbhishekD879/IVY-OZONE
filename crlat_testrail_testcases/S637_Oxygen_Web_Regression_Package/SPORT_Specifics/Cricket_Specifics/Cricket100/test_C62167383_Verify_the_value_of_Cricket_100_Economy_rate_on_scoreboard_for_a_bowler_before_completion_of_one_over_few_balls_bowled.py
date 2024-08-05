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
class Test_C62167383_Verify_the_value_of_Cricket_100_Economy_rate_on_scoreboard_for_a_bowler_before_completion_of_one_over_few_balls_bowled(Common):
    """
    TR_ID: C62167383
    NAME: Verify the value of Cricket 100 Economy rate on scoreboard for a bowler before completion of one over (few balls bowled)
    DESCRIPTION: This testcase verifies the value of Cricket 100 Economy rate on scoreboard for a bowler before completion of one over (few balls bowled)
    PRECONDITIONS: 1.Login to app.
    PRECONDITIONS: 2.Event should be live.
    PRECONDITIONS: Note:
    PRECONDITIONS: 1.The Formula for Calculating the economy rate  =  (Total Runs Given by bowler / Legal balls bowled by bowler) * (balls in 1 over)
    PRECONDITIONS: 2.5 balls will be consider as 1 over for economy calculation(For C100).
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage.
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

    def test_005_verify_the_value_of_economy_rate_on_scoreboard_before_completion_of_an_over__few_balls_bowled(self):
        """
        DESCRIPTION: Verify the value of Economy rate on scoreboard before completion of an over ( few balls bowled)
        EXPECTED: Economy rate should be displayed as Econ with a value  on scoreboard
        EXPECTED: For example:
        EXPECTED: Batsmen        R    B    4s   6s  SR
        EXPECTED: AN. Cook       1     1     0    0  100
        EXPECTED: MAH. Biiov•    2     3     0   0  66.67
        EXPECTED: Bowler               B    R    W     Econ
        EXPECTED: N.M. Lyon (5)        4    3    1       0
        EXPECTED: For current bowler :
        EXPECTED: Completed balls : 2
        EXPECTED: Completed overs : 0 (Opta sends 5 balls as 1 over)
        EXPECTED: Total runs given :  4
        EXPECTED: Economy  =  0, as overs is 0.
        EXPECTED: Note: Refer preconditions for calculating the economy rate of the bowler.
        EXPECTED: Cricket 100
        """
        pass
