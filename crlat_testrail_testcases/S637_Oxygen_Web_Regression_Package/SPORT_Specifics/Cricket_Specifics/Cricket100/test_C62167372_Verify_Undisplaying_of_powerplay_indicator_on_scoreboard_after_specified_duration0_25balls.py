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
class Test_C62167372_Verify_Undisplaying_of_powerplay_indicator_on_scoreboard_after_specified_duration0_25balls(Common):
    """
    TR_ID: C62167372
    NAME: Verify Undisplaying of powerplay indicator on scoreboard after specified duration(0-25)balls.
    DESCRIPTION: This testcase verifies Undisplaying of powerplay indicator on scoreboard after (0-25)balls.
    PRECONDITIONS: Event should be live.
    PRECONDITIONS: Powerplay Rules:
    PRECONDITIONS: 1. The power play will be only between 1st ball to 25th ball of each innings
    PRECONDITIONS: 2. When the powerplay is on, there should be an thunderstorm icon beside the team name along with a message as "Poweplay Active- Team Name"
    PRECONDITIONS: 3. When the powerplay is completed after 25th ball, the icon and the powerplay message will be disappeared
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

    def test_003_click_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to__event_details_page_edp(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify whether the user is able to navigate to  event details page (edp).
        EXPECTED: User should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_scoreboard(self):
        """
        DESCRIPTION: Verify displaying of scoreboard.
        EXPECTED: Scoreboard should be displayed in event details page (edp).
        """
        pass

    def test_005_verify_undisplaying_of_powerplay_indicator_on_scoreboard_after_specified_duration_0_25balls(self):
        """
        DESCRIPTION: Verify Undisplaying of powerplay indicator on scoreboard after specified duration (0-25)balls.
        EXPECTED: Powerplay indicator and the message should be disappeared on scoreboard after powerplay is inactive.
        """
        pass
