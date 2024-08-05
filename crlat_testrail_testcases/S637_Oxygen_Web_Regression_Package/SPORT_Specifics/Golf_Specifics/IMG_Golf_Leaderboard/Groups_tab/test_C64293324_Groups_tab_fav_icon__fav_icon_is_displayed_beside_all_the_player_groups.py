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
class Test_C64293324_Groups_tab_fav_icon__fav_icon_is_displayed_beside_all_the_player_groups(Common):
    """
    TR_ID: C64293324
    NAME: Groups tab fav icon - fav icon is displayed beside all the player groups
    DESCRIPTION: Verify favorite option beside player groups in groups tab
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is Logged in.
    PRECONDITIONS: 5. Navigate to inplay Golf EDP--> Groups tab in LB
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
        EXPECTED: LB should load
        """
        pass

    def test_003_navigate_to_groups_tab(self):
        """
        DESCRIPTION: Navigate to Groups tab.
        EXPECTED: Groups tab is opened
        """
        pass

    def test_004_verify_if_the_favorite_option_is_displayed_before_all_player_groups_in_the_table(self):
        """
        DESCRIPTION: Verify if the favorite option is displayed before all player groups in the table.
        EXPECTED: Favorite option should be displayed beside all player groups
        """
        pass

    def test_005_verify_user_can_selectdeselect_favourite_icon(self):
        """
        DESCRIPTION: Verify user can select/Deselect favourite icon
        EXPECTED: User can select and deselect the favorite icon with a click/tap
        """
        pass
