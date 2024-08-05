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
class Test_C64293317_fav_icon_player_position_table__Verify_the_favorite_option_selected_for_tournament_on_device_is_reflecting_on_logging_on_another_device_desktop(Common):
    """
    TR_ID: C64293317
    NAME: fav icon player position table - Verify the favorite option selected for tournament on device is reflecting on logging on another device/desktop
    DESCRIPTION: This tc verifies if the fav players selected on one device are saved if we login with another device
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is logged in.
    PRECONDITIONS: 5. Navigate to Golf inplay EDP -->> Leaderboard tab-->Player position table
    PRECONDITIONS: 6. Mark few players as favorite
    PRECONDITIONS: 7. Login into same account on another device/browser
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

    def test_004_login_into_same_account_on_another_devicebrowser(self):
        """
        DESCRIPTION: Login into same account on another device/browser
        EXPECTED: user should be able to login
        """
        pass

    def test_005_navigate_to_the_lb_and_check_if_the_fav_selections_are_saved(self):
        """
        DESCRIPTION: navigate to the LB and check if the fav selections are saved
        EXPECTED: players marked as fav on a device should reflect as fav in FE if the player logs into another device with the same account
        """
        pass
