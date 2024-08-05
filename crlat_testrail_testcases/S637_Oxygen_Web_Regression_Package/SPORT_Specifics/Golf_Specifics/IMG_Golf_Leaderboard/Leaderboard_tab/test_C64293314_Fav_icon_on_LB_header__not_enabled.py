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
class Test_C64293314_Fav_icon_on_LB_header__not_enabled(Common):
    """
    TR_ID: C64293314
    NAME: Fav icon on LB header - not enabled
    DESCRIPTION: This tc verifies the functionality of fav icon on header in disabled state
    PRECONDITIONS: "1.User should have admin access to CMS
    PRECONDITIONS: 2.Navigate to CMS> System Configuration > Structure both IMGScoreboard and IMGScoreboardsports checkbox should be enabled.
    PRECONDITIONS: 3. Inplay event should be mapped with IMG feed provider event Id.
    PRECONDITIONS: 4. User is logged in.
    PRECONDITIONS: 5. Navigate to Golf inplay EDP -->> Leaderboard tab-->Player position table
    PRECONDITIONS: 6. Mark few players as favorite"
    """
    keep_browser_open = True

    def test_001_navigate_to_golf_edp_page_for_which_leaderboard_is_available(self):
        """
        DESCRIPTION: Navigate to Golf EDP page for which Leaderboard is available.
        EXPECTED: EDP is opened and LB is displayed
        """
        pass

    def test_002_disable_fav_icon_in_the_header(self):
        """
        DESCRIPTION: Disable fav icon in the header.
        EXPECTED: All players should be displayed according to their positions in player position table
        """
        pass
