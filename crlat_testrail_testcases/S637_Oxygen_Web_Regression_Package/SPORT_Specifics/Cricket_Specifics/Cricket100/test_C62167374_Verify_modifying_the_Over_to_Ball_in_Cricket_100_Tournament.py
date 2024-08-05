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
class Test_C62167374_Verify_modifying_the_Over_to_Ball_in_Cricket_100_Tournament(Common):
    """
    TR_ID: C62167374
    NAME: Verify modifying the 'Over' to 'Ball' in Cricket 100 Tournament
    DESCRIPTION: This testcase verifies modifying the 'Over' to 'Ball' in Cricket 100 Tournament.
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
        EXPECTED: In-play page should be loaded.
        """
        pass

    def test_003_click_on_any_event_and_verify_whether_the_user_is_able_to_navigate_to__event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any event and verify whether the user is able to navigate to  event details page (edp ).
        EXPECTED: User should be navigated to event details page (edp)
        """
        pass

    def test_004_verify_displaying_of_score_board_in_event_details_page_edp(self):
        """
        DESCRIPTION: Verify displaying of score board in event details page (edp).
        EXPECTED: Scoreboard should be displayed in event details page (edp).
        """
        pass

    def test_005_verify_displaying_of_balls_instead_of_overs_as_overs_are_replaced_with_balls_on_scoreboard(self):
        """
        DESCRIPTION: Verify displaying of balls instead of overs (as overs are replaced with balls) on scoreboard.
        EXPECTED: Ball's should be displayed instead of overs as below
        EXPECTED: eg:  (5balls )  4  1  1lb _  _
        EXPECTED: (10 balls)      1  2  4   4  w  _  _  _  _  _
        """
        pass
