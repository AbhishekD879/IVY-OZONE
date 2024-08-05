import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.5_a_side
@vtest
class Test_C62700734_Verify_if_leaderboard_toggle_is_disabled_for_that_team_then_fallback_to_the_crests_display(Common):
    """
    TR_ID: C62700734
    NAME: Verify, if leaderboard toggle is disabled for that team then fallback to the crests display.
    DESCRIPTION: Verify, if leaderboard toggle is disabled for that team then fallback to the crests display.
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: 1. Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2)  user should not placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    PRECONDITIONS: Asset Manager
    PRECONDITIONS: 1. Upload image to team, if team is created
    PRECONDITIONS: 2. Create team, if team is not created with both Primary & secondary Color hexa codes
    """
    keep_browser_open = True

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_validate_the_display_of_5_a_side_showdown_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: Validate the display of '5-A Side showdown' tab in left side menu of CMS
        EXPECTED: User should be able to view the 5-A Side showdown tab
        """
        pass

    def test_003_add_contest(self):
        """
        DESCRIPTION: Add Contest
        EXPECTED: Fill all the Mand* fields and save the contest
        """
        pass

    def test_004_add_images_in_asset_manager_for_team(self):
        """
        DESCRIPTION: Add images in asset manager for team
        EXPECTED: Images should be uploaded for team in asset manager
        """
        pass

    def test_005_leaderboard_toggle_is_off(self):
        """
        DESCRIPTION: Leaderboard toggle is "OFF"
        EXPECTED: Leader board toggle should be disabled
        """
        pass

    def test_006_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_007_validate_the_shape_of_the_team_images_in_fe(self):
        """
        DESCRIPTION: Validate the shape of the team images in FE
        EXPECTED: shape of the team should fallback to crests in FE
        """
        pass
