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
class Test_C62167382_Verify_the_value_of_Cricket_100_Economy_rate_on_scoreboard_for_a_bowler(Common):
    """
    TR_ID: C62167382
    NAME: Verify the value of Cricket 100 Economy rate on scoreboard for a bowler
    DESCRIPTION: This testcase verifies the value of Cricket 100 Economy rate on scoreboard for a bowler.
    PRECONDITIONS: 1.Login to app.
    PRECONDITIONS: 2.Event should be live.
    PRECONDITIONS: Note:
    PRECONDITIONS: 1.The Formula for Calculating the economy rate  =  (Total Runs Given by bowler / Legal balls bowled by bowler) * (balls in 1 over)
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

    def test_003_click_on_any_cricket_100_event_and_verifywhether_the_user_is_able_to_navigate_to__event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify
        DESCRIPTION: whether the user is able to navigate to  event details page (edp ).
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_scoreboard_in_event_details_page_edp_(self):
        """
        DESCRIPTION: Verify displaying of scoreboard in event details page (edp) .
        EXPECTED: Scoreboard should be displayed on event details page.
        """
        pass

    def test_005_verify_the_value_of_economy_rate_on_scoreboard(self):
        """
        DESCRIPTION: Verify the value of Economy rate on scoreboard
        EXPECTED: Economy rate should be displayed as Econ with a value  on scoreboard
        EXPECTED: Eg:Bowler:      B      R       W        Econ
        EXPECTED: M. Abbas       20     4       1          2.04
        EXPECTED: B-Balls,R-Runs,W-Wickets,Econ-Economy rate.
        EXPECTED: Note: Refer preconditions for calculating the economy rate of the bowler.
        EXPECTED: See the below example:
        EXPECTED: S.no	Runs Conceded for ball	Total Balls By Bowler	ECON (After each ball)	Ball Description	Description
        EXPECTED: 1	1	0	Empty	Wide	T.Runs - 1 , T.Balls -0
        EXPECTED: 2	1	1	10	1 run	T.Runs - 2 , T.Balls -1 =  ((2 runs/1 ball )*5 bs for over) = 10
        EXPECTED: 3	2	2	10	2 runs	T.Runs - 4 , T.Balls -2
        EXPECTED: 4	0	3	6.67	dot ball	T.Runs - 4 , T.Balls -3
        EXPECTED: 5	6	4	12.5	6 runs	T.Runs - 10 , T.Balls -4
        EXPECTED: 6	1	4	13.75	Wide	T.Runs - 11 , T.Balls -4
        EXPECTED: 7	3	5	14	3 runs	T.Runs - 14 , T.Balls -5
        """
        pass
