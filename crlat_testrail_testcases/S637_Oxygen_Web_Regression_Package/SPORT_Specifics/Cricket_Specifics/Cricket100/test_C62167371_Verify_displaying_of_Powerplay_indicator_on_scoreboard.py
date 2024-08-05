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
class Test_C62167371_Verify_displaying_of_Powerplay_indicator_on_scoreboard(Common):
    """
    TR_ID: C62167371
    NAME: Verify displaying of Powerplay indicator on scoreboard
    DESCRIPTION: This testcase verifies displaying of Powerplay indicator on scoreboard
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
        EXPECTED: in-play page should be loaded.
        """
        pass

    def test_003_click_on_any_cricket_100_event_and_verify_whether_the_user_is_able_to_navigate_to__event_details_page_edp_(self):
        """
        DESCRIPTION: Click on any Cricket 100 event and verify whether the user is able to navigate to  event details page (edp ).
        EXPECTED: Click on any event and user should be navigated to event details page (edp).
        """
        pass

    def test_004_verify_displaying_of_score_board_in_event_details_page_edp_(self):
        """
        DESCRIPTION: Verify displaying of score board in event details page (edp ).
        EXPECTED: Scoreboard should be displayed in event details page (edp ).
        """
        pass

    def test_005_verify_displaying_of_powerplay_indicator_beside_team_name_on_scoreboard_between_the_specified_duration1_25ballsnote_refer_pre__conditions(self):
        """
        DESCRIPTION: Verify displaying of powerplay indicator beside team name on scoreboard between the specified duration(1-25)balls.
        DESCRIPTION: Note: Refer Pre- Conditions.
        EXPECTED: Powerplay indicator icon(thunderstorm) should be displayed beside team name and with a message "Powerplay Active-Team name".
        """
        pass
