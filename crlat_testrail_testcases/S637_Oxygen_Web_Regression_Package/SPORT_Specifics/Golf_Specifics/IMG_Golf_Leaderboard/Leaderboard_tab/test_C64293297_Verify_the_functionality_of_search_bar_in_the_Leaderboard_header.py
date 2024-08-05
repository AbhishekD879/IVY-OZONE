import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64293297_Verify_the_functionality_of_search_bar_in_the_Leaderboard_header(Common):
    """
    TR_ID: C64293297
    NAME: Verify the functionality of search bar in the Leaderboard header.
    DESCRIPTION: This Testcase verifies the search option functionality in the header of Leaderboard tab
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_in_play_event_edp_page(self):
        """
        DESCRIPTION: Navigate to golf in-play event EDP page
        EXPECTED: User should be navigated to Leaderboard when the event is in-play
        """
        pass

    def test_002_verify_the_leader_board_is_displayed_in_golf_edp_page(self):
        """
        DESCRIPTION: Verify the Leader board is displayed in golf EDP page
        EXPECTED: User should be displayed Leaderboard
        """
        pass

    def test_003_verify_search_function(self):
        """
        DESCRIPTION: Verify Search function
        EXPECTED: User should be displayed with Player related info.
        """
        pass

    def test_004_enter_any_player_name_and_click_on_enter(self):
        """
        DESCRIPTION: Enter any player name and click on Enter
        EXPECTED: 
        """
        pass

    def test_005_verify_search_function(self):
        """
        DESCRIPTION: Verify Search function
        EXPECTED: User should be displayed with proper error messages.
        """
        pass

    def test_006_enter_any_invalidnot_available_player_name_nd_click_on_enter(self):
        """
        DESCRIPTION: Enter any invalid/not available player name nd click on Enter.
        EXPECTED: 
        """
        pass
