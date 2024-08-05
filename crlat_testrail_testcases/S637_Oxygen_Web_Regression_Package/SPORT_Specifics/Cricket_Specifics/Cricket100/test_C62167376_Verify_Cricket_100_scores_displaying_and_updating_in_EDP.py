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
class Test_C62167376_Verify_Cricket_100_scores_displaying_and_updating_in_EDP(Common):
    """
    TR_ID: C62167376
    NAME: Verify Cricket 100 scores displaying and updating in EDP
    DESCRIPTION: This test case verifies Cricket 100 scores are displaying and updating in EDP.
    PRECONDITIONS: 1.In order to have scores, Cricket 100 event should be BIP event.
    PRECONDITIONS: 2.Scores are updating.
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage.
        EXPECTED: User should be navigated to Cricket 100 page
        EXPECTED: -Matches tab should be opened by default.
        """
        pass

    def test_002_tap_on_inplay_tab(self):
        """
        DESCRIPTION: Tap on inplay tab.
        EXPECTED: In play tab should be loaded and data should be displayed.
        """
        pass

    def test_003_click_on_any_cricket_100_event_and_check_whether_the_user_is_able_to_navigate_to_edp(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and check whether the user is able to navigate to edp.
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_and_updating_of_scores(self):
        """
        DESCRIPTION: Verify displaying and updating of scores.
        EXPECTED: Scores are displaying and updating, beside Team name.
        """
        pass
