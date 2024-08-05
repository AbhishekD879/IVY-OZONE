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
class Test_C64293311_Verify_Player_position_table(Common):
    """
    TR_ID: C64293311
    NAME: Verify Player position table
    DESCRIPTION: Check Player position table on Laederboard tab
    PRECONDITIONS: 1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_edp_page_for_which_leaderboard_is_available(self):
        """
        DESCRIPTION: Navigate to Golf EDP page for which Leaderboard is available.
        EXPECTED: User should see Leaderboard.
        """
        pass

    def test_002_scroll_down_on_leaderboad_tab_till_you_see_player_position_table(self):
        """
        DESCRIPTION: Scroll down on Leaderboad tab till you see player position table.
        EXPECTED: Player position table is displayed as per the design and updates by push
        """
        pass
