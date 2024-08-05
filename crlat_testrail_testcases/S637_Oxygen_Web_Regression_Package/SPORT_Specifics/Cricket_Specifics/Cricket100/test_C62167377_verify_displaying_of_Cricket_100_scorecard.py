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
class Test_C62167377_verify_displaying_of_Cricket_100_scorecard(Common):
    """
    TR_ID: C62167377
    NAME: verify displaying of Cricket 100 scorecard
    DESCRIPTION: This test case verifies displaying of Cricket 100 scorecard.
    PRECONDITIONS: 1.Event should start and player's data should be displayed in scorecard.
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

    def test_003_click_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to__event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify whether the user is able to navigate to  event details page (edp ).
        EXPECTED: user should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_scores_on_scoreboard_in_event_details_page_edp(self):
        """
        DESCRIPTION: Verify displaying of scores on scoreboard in event details page (edp).
        EXPECTED: Scores should be displayed on scoreboard.
        EXPECTED: -Scorecard should not overlap with player's data
        """
        pass
