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
class Test_C62700697_Verify_default_background_displayed_in_Pre_live__post_leaderboards_FE_if_no_background_image_uploaded_by_the_content_user(Common):
    """
    TR_ID: C62700697
    NAME: Verify default background displayed  in Pre/live / post leaderboards (FE), if no background image uploaded by the content user.
    DESCRIPTION: Verify default background displayed  in Pre/live / post leaderboards (FE), if no background image uploaded by the content user.
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
    """
    keep_browser_open = True

    def test_001_1_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: 1. Login to CMS as admin user
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_2_validate_the_display_of_5_a_side_showdown_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: 2. Validate the display of '5-A Side showdown' tab in left side menu of CMS
        EXPECTED: User should be able to view the 5-A Side showdown tab
        """
        pass

    def test_003_3_add_contest(self):
        """
        DESCRIPTION: 3. Add Contest
        EXPECTED: Fill all the Mand* fields and save the contest
        """
        pass

    def test_004_5_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: 5. Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_005_6_validate_the_default_green_grassy_background_image_displayed(self):
        """
        DESCRIPTION: 6. Validate the default green grassy background image displayed
        EXPECTED: default green glassy background image should display in pre/live and inactive green glassy background post leaderboards, if no background image uploaded by the content user.
        """
        pass
