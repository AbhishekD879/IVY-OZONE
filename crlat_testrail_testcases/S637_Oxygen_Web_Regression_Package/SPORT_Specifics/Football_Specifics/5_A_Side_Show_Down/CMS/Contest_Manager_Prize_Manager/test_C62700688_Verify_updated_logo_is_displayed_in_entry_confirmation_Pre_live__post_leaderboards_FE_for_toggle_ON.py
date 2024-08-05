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
class Test_C62700688_Verify_updated_logo_is_displayed_in_entry_confirmation_Pre_live__post_leaderboards_FE_for_toggle_ON(Common):
    """
    TR_ID: C62700688
    NAME: Verify updated logo is displayed in entry confirmation/ Pre/live / post leaderboards (FE) for toggle ON.
    DESCRIPTION: Verify updated logo is displayed in entry confirmation/ Pre/live / post leaderboards (FE) for toggle ON.
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

    def test_004_4_validate_toggle_on_for_5_a_side_logo_image(self):
        """
        DESCRIPTION: 4. Validate toggle "ON" for 5-a-side logo image
        EXPECTED: toggle should "ON"
        """
        pass

    def test_005_5_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: 5. Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_006_6_validate_the_uploaded_5_a_side_logo(self):
        """
        DESCRIPTION: 6. Validate the uploaded 5-a-side logo
        EXPECTED: Uploaded logo image should display in entry confirmation & pre/live and post leaderboards
        """
        pass
