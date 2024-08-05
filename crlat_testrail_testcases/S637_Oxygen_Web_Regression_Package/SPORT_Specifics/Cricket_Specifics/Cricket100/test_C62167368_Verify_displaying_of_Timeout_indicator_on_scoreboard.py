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
class Test_C62167368_Verify_displaying_of_Timeout_indicator_on_scoreboard(Common):
    """
    TR_ID: C62167368
    NAME: Verify displaying of Timeout indicator on scoreboard
    DESCRIPTION: This testcase verifies displaying of Timeout indicator on scoreboard.
    PRECONDITIONS: Event should be live(In Play).
    """
    keep_browser_open = True

    def test_001_navigate_to_cricket_100__from_a_z_sportsribbon_tabhomepage(self):
        """
        DESCRIPTION: Navigate to Cricket 100  from A-Z sports/ribbon tab/Homepage.
        EXPECTED: User should be navigated to cricket 100.
        EXPECTED: -Matches tab is displayed by default.
        """
        pass

    def test_002_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to in-play page.
        EXPECTED: In-play page should be loaded.
        """
        pass

    def test_003_tapclick_on_cricket_100__event_and_verify_whether_the_user_is_able_to_navigate_to_event_details_page(self):
        """
        DESCRIPTION: Tap/Click on Cricket 100  event and verify whether the user is able to navigate to event details page.
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_scoreboard_in_event_details_page_edp(self):
        """
        DESCRIPTION: Verify displaying of scoreboard in event details page (edp).
        EXPECTED: Scoreboard should be displayed on event details page.
        """
        pass

    def test_005_verify_if_any_team_is_having_a_strategic_timeout_on_scoreboard(self):
        """
        DESCRIPTION: Verify if any team is having a strategic timeout on scoreboard.
        EXPECTED: Scoreboard with Timeout indicator should displayed beside team name, specifying which team has taken a strategic timeout (150 seconds)during the game and with message as “Timeout - Bowling/Batting Team Name”.
        """
        pass
