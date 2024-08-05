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
class Test_C64293315_fav_icon_player_position_table__Verify_fav_options_selected_for_a_tournament_is_stored_across_user_sessions(Common):
    """
    TR_ID: C64293315
    NAME: fav icon player position table - Verify fav options selected for a tournament is stored across user sessions
    DESCRIPTION: This tc verifies if the fav players selected in a tournament is saved across user sessions
    PRECONDITIONS: "1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is logged in.
    PRECONDITIONS: 5. Navigate to Golf inplay EDP -->> Leaderboard tab-->Player position table
    PRECONDITIONS: 6. Mark few players as favorite
    PRECONDITIONS: 4. Restart the application."
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

    def test_004_kill_the_app_and_restart(self):
        """
        DESCRIPTION: Kill the app and restart.
        EXPECTED: app should restart
        """
        pass

    def test_005_navigate_to_golf_lb_and_scroll_down_to_player_details_table(self):
        """
        DESCRIPTION: Navigate to Golf LB and scroll down to player details table.
        EXPECTED: User should be able to load scroll down to player detail table in LB after restart
        """
        pass

    def test_006_check_if_the_fav_selections_from_previous_session_are_saved(self):
        """
        DESCRIPTION: Check if the fav selections from previous session are saved.
        EXPECTED: players marked as fav should be saved across all user sessions
        """
        pass
