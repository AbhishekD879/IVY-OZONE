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
class Test_C62167381_Verify_displaying_the_stats_of_the_each_innings_bowling_with_correct_figureswithout_anydelay(Common):
    """
    TR_ID: C62167381
    NAME: Verify displaying the stats of the each innings (bowling) with correct figures without any delay. 
    DESCRIPTION: This test case verifies displaying the stats of the each innings(bowling) with correct figures without any delay.
    PRECONDITIONS: 1.Load the app.
    PRECONDITIONS: 2.Event should be live.
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage.
        EXPECTED: User should be navigated to cricket 100.
        EXPECTED: -Matches tab should be displayed by default.
        """
        pass

    def test_002_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to in-play page.
        EXPECTED: In-play page should be loaded.
        """
        pass

    def test_003_click_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to__event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify whether the user is able to navigate to  event details page (edp ).
        EXPECTED: User should be navigated to event details page (EDP).
        """
        pass

    def test_004_verify_displaying_of_both_team_innings_on_scoreboard(self):
        """
        DESCRIPTION: Verify displaying of both team innings on scoreboard.
        EXPECTED: User should be able to see both Team Innings beside their names.
        """
        pass

    def test_005_verify_displaying_of_bowler_stats(self):
        """
        DESCRIPTION: Verify displaying of Bowler Stats.
        EXPECTED: User should be able to see bowler stats.
        EXPECTED: Bowler stats should be display as per below:
        EXPECTED: Bowler:      B      R       W        Econ
        EXPECTED: M. Abbas     20     4       1          2.04
        EXPECTED: B-Balls
        EXPECTED: R-Runs
        EXPECTED: W-Wickets
        EXPECTED: Econ-Economy rate
        EXPECTED: Note:
        EXPECTED: Each Bowler can bowl a maximum of 20 Balls in the whole Game.
        EXPECTED: Bowler can continue bowling  next 5 balls after he completes 5 balls based on the captain's decision.
        """
        pass
