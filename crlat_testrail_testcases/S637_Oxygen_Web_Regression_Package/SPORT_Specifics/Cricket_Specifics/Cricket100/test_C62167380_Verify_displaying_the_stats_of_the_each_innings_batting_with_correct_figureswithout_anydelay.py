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
class Test_C62167380_Verify_displaying_the_stats_of_the_each_innings_batting_with_correct_figureswithout_anydelay(Common):
    """
    TR_ID: C62167380
    NAME: Verify displaying the stats of the each innings (batting) with  correct figures without any delay. 
    DESCRIPTION: This test case verifies displaying the stats of the each innings(batting) with
    DESCRIPTION: correct figures without any delay.
    PRECONDITIONS: 1.Load the app.
    PRECONDITIONS: 2.Event should be live.
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage.
        EXPECTED: User should be navigated to Cricket 100.
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
        EXPECTED: User should be navigated to event details page(EDP).
        """
        pass

    def test_004_verify_displaying_of_both_team_innings_on_scoreboard(self):
        """
        DESCRIPTION: Verify displaying of both team innings on scoreboard.
        EXPECTED: User should be able to see both team Innings beside their names.
        """
        pass

    def test_005_verify_displaying_of_batters_stats(self):
        """
        DESCRIPTION: Verify displaying of Batters Stats.
        EXPECTED: User should be able to see batters stats.
        EXPECTED: -Batters stats should be display as per below:
        EXPECTED: Batters:      R   B    4's   6's    SR
        EXPECTED: S.Marsh       45  96   5     1      46.87
        EXPECTED: U.Khawaja     45   96   5     1      46.87
        EXPECTED: R- Runs
        EXPECTED: B- Balls
        EXPECTED: SR- Strike Rate
        EXPECTED: Note: A Dot will be displayed beside the batsman name whoever is on strike
        """
        pass
