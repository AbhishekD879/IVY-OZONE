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
class Test_C64293316_fav_icon__player_position_table__Verify_the_fav_options_selected_in_player_position_table_are_saved_for_other_tournaments(Common):
    """
    TR_ID: C64293316
    NAME: fav icon - player position table - Verify the fav options selected in player position table are saved for other tournaments
    DESCRIPTION: This tc verifies if the fav players selected in past tournaments are saved for current/future tournaments
    PRECONDITIONS: "1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is logged in.
    PRECONDITIONS: 5. Navigate to Golf inplay EDP -->> Leaderboard tab-->Player position table
    PRECONDITIONS: 6. Mark few players as favorite
    PRECONDITIONS: 7. Wait for current tournament to end and new tournament to start."
    """
    keep_browser_open = True

    def test_001_login_into_application(self):
        """
        DESCRIPTION: Login into application.
        EXPECTED: User is logged in
        """
        pass

    def test_002_navigate_to_leaderboard_when_the_event_is_inplay(self):
        """
        DESCRIPTION: Navigate to Leaderboard when the event is inplay.
        EXPECTED: User should be able to Navigate to Leaderboad
        """
        pass

    def test_003_scroll_down_to_player_position_table_and_mark_few_players_as_fav(self):
        """
        DESCRIPTION: scroll down to player position table and mark few players as fav.
        EXPECTED: User should be able to mark players are Fav
        """
        pass

    def test_004_wait_for_the_current_tournament_to_end_and_new_tournament_to_start(self):
        """
        DESCRIPTION: Wait for the current tournament to end and new tournament to start.
        EXPECTED: 
        """
        pass

    def test_005_check_if_the_fav_selections_from_previous_tournament_are_saved_for_new_tournament(self):
        """
        DESCRIPTION: Check if the fav selections from previous tournament are saved for new tournament.
        EXPECTED: players marked as fav should be saved across all user sessions
        """
        pass
