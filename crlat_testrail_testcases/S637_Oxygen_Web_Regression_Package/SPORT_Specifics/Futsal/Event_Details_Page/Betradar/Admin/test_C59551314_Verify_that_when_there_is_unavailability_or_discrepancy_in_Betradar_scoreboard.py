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
class Test_C59551314_Verify_that_when_there_is_unavailability_or_discrepancy_in_Betradar_scoreboard(Common):
    """
    TR_ID: C59551314
    NAME: Verify that when there is unavailability or discrepancy in Betradar scoreboard
    DESCRIPTION: This test case verifies  when there is unavailability or discrepancy in Betradar scoreboard as admin user able to disable the toggle
    PRECONDITIONS: 1: Navigate to Sports Menu(Fustal)/From A-Z all Sports->Fustal
    PRECONDITIONS: 2:Futsal event(s) are subscribed to Bet radar Scoreboards
    PRECONDITIONS: Event in InPlay state
    PRECONDITIONS: 3:Betradar scoreboard configuration in CMS is Enabled.
    PRECONDITIONS: TBD?
    PRECONDITIONS: CMS > System Configuration > Structure > Betradar Scoreboard
    PRECONDITIONS: How to check event is mapped to betradar or not?
    PRECONDITIONS: inspect elements click on inplay event and while loading EDP check for api-key network call. if we get 200 response then event has betradar and if we get 404 this event should show fallback
    PRECONDITIONS: Confluence link:
    PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=139380661
    """
    keep_browser_open = True

    def test_001_launch_the_application_and_navigate_to_futsal_edp_from_home___futsal__inplay(self):
        """
        DESCRIPTION: Launch the application and navigate to Futsal EDP from Home - Futsal- inplay
        EXPECTED: Futsal inplay landing page should display
        """
        pass

    def test_002_verify_inplay_landing_page(self):
        """
        DESCRIPTION: Verify inplay landing page
        EXPECTED: League wise inplay events should display
        EXPECTED: 1.Team names(Player) with live icon(Coral below to team names and Lads above to player name) should display
        EXPECTED: 2. Fall back score board with live score should display
        EXPECTED: 3.Odds should update as per feed from OB
        EXPECTED: 4. markets with clickable links should display
        EXPECTED: Coral - # of markets with clickable link should display
        EXPECTED: Lads - # of markets with more link
        """
        pass

    def test_003_navigate_to_the_fustal_event_details_page_from_preconditions(self):
        """
        DESCRIPTION: Navigate to the Fustal event details page from Preconditions
        EXPECTED: It should navigated to Fustal EDP.
        """
        pass

    def test_004_validate_the_live_score_and_details(self):
        """
        DESCRIPTION: Validate the Live score and details
        EXPECTED: Deatails should be accurate
        """
        pass

    def test_005_if_unavailability_or_discrepancy_in_betradar_scoreboard_admin_user_able_to_toggle_off_the_bet_radar_score_boared(self):
        """
        DESCRIPTION: If unavailability or discrepancy in Betradar scoreboard admin User able to toggle off the bet radar score boared
        EXPECTED: Changes Should saved
        """
        pass

    def test_006_verify_the_fall_back_score_board_is_displaying_in_front_end(self):
        """
        DESCRIPTION: Verify the fall back score board is displaying in Front end
        EXPECTED: Fall back score board should be displayed
        """
        pass
