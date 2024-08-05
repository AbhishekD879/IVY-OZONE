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
class Test_C62167373_Verify_displaying_and_updating_of_ball_by_ball_indicator_on_scoreboard(Common):
    """
    TR_ID: C62167373
    NAME: Verify displaying and updating of ball by ball indicator on scoreboard
    DESCRIPTION: This testcase verifies displaying and updating of ball by ball indicator on scoreboard.
    PRECONDITIONS: Event should be live.
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage.
        EXPECTED: User should be navigated to cricket 100.
        EXPECTED: -Matches tab should be displayed by default.
        """
        pass

    def test_002_go_to_in_play_tab(self):
        """
        DESCRIPTION: Go to in-play tab.
        EXPECTED: in-play page should be loaded.
        """
        pass

    def test_003_click_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to__event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify whether the user is able to navigate to  event details page (edp ).
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_score_board_in_event_details_page_edp(self):
        """
        DESCRIPTION: Verify displaying of score board in event details page (edp).
        EXPECTED: Scoreboard should be displayed in event details page (edp).
        """
        pass

    def test_005_verify_displaying_of_ball_by_ball_indicator_in_5_or_10_ball_spell_along_with_extras_if_anyon_scoreboard(self):
        """
        DESCRIPTION: Verify displaying of ball by ball indicator in 5 or 10 ball spell along with Extras (If any)on scoreboard.
        EXPECTED: In 5 or 10 ball spell ,dot should be displayed on scoreboard during the match which keeps track of total no of balls bowled.
        EXPECTED: eg:  (5balls) 4  1  1lb _  _
        EXPECTED: (10 balls) 1  2  4   4   1w  _  _  _  _  _ _
        EXPECTED: Note:
        EXPECTED: 1.When a ball is bowled by a bowler in a 5 ball spell, display 5 blocks/dots. Also, increase the dots/ indicators if there are any wide or no balls bowled.
        EXPECTED: 2. Same logic applies for a 10 balls spell if the captain decides to increase the spell to 10 balls.
        EXPECTED: 3. Each bowler can bowl a maximum of 20 balls in a whole game
        EXPECTED: 4. The captain will select how many balls each bowler will bowl in a spell with a minimum of 5balls.
        EXPECTED: 5. bowlers will simply change ends after they finish bowling their current spell
        EXPECTED: 6. In Case if the bowler bowls wide in the last balls of the spell- the indicator will not be displayed.
        """
        pass
