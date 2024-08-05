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
class Test_C64293312_fav_icon_is_displayed_beside_all_the_player_names(Common):
    """
    TR_ID: C64293312
    NAME: fav icon is displayed beside all the player names
    DESCRIPTION: Verify favorite option beside player names in player position table
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is logged in.
    PRECONDITIONS: 5. Navigate to Golf inplay EDP -->> Leaderboard tab-->Player position table
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_leaderboard(self):
        """
        DESCRIPTION: Navigate to Golf Leaderboard
        EXPECTED: User should navigate to Golf Leaderboard
        """
        pass

    def test_002_scroll_down_to_player_position_table(self):
        """
        DESCRIPTION: Scroll down to player position table.
        EXPECTED: User should able to access player position table.
        """
        pass

    def test_003_verify_if_the_favorite_option_is_displayed_before_all_player_names_in_the_table(self):
        """
        DESCRIPTION: Verify if the favorite option is displayed before all player names in the table.
        EXPECTED: Favorite option should be displayed beside all player names
        """
        pass

    def test_004_verify_user_can_selectdeselect_favourite_icon(self):
        """
        DESCRIPTION: Verify user can select/Deselect favourite icon
        EXPECTED: User can select and deselect the favorite icon with a click/tap
        """
        pass
