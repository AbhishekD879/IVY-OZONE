import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C62167370_Verify_Undisplaying_of_Timeout_indicator_on_scoreboard(Common):
    """
    TR_ID: C62167370
    NAME: Verify Undisplaying of Timeout  indicator on scoreboard
    DESCRIPTION: This testcase verifies Undisplaying of Timeout indicator on scoreboard
    PRECONDITIONS: Event should be live.
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage.
        EXPECTED: User should be navigated to cricket 100.
        EXPECTED: -Matches tab should be  displayed by default.
        """
        pass

    def test_002_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to in-play page.
        EXPECTED: In-play page should be loaded.
        """
        pass

    def test_003_tapclick_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to_event_details_page(self):
        """
        DESCRIPTION: Tap/Click on any Cricket 100 event and verify whether the user is able to navigate to event details page.
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_that_the_timeout_indicator_is_greyed_out__after_the_strategic_timeout_session_is_completed(self):
        """
        DESCRIPTION: Verify that the timeout indicator is greyed out  after the strategic timeout session is completed.
        EXPECTED: Strategic timeout message should disappear and Timeout indicator will be greyed out beside team name and the match will be resumed with message "Resumption of play "
        EXPECTED: Note:. Time out indicator should be displayed as greyed out throughout after the completion of strategic timeout session for that particular team.
        """
        pass
