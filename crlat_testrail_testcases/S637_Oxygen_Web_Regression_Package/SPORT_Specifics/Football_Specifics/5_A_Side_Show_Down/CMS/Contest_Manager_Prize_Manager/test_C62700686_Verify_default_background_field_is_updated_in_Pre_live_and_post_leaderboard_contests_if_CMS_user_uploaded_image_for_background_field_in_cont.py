import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.5_a_side
@vtest
class Test_C62700686_Verify_default_background_field_is_updated_in_Pre_live_and_post_leaderboard_contests_if_CMS_user_uploaded_image_for_background_field_in_contest_creation_page(Common):
    """
    TR_ID: C62700686
    NAME: Verify default background field is updated in Pre-live and post leaderboard contests, if CMS user uploaded image for background field  in contest creation page.
    DESCRIPTION: Verify default background field is updated in Pre-live and post leaderboard contests, if CMS user uploaded image for background field  in contest creation page.
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
    PRECONDITIONS: ""
    PRECONDITIONS: "
    """
    keep_browser_open = True

    def test_001_1_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: 1. Login to CMS as admin user
        EXPECTED: 1. User should be able to login successfully
        """
        pass

    def test_002_2_validate_the_display_of_5_a_side_showdown_tab_in_left_side_menu_of_cms(self):
        """
        DESCRIPTION: 2. Validate the display of '5-A Side showdown' tab in left side menu of CMS
        EXPECTED: 2. User should be able to view the 5-A Side showdown tab
        """
        pass

    def test_003_3_add_contest(self):
        """
        DESCRIPTION: 3. Add Contest
        EXPECTED: Fill all the Mandatory * fields and save the contest
        """
        pass

    def test_004_4upload_logo_which_allows_to_replaces_the_5_a_side_logo_within_the_leaderboard_header(self):
        """
        DESCRIPTION: 4.Upload ‘Logo’ which allows to replaces the 5-A-Side logo within the Leaderboard header.
        EXPECTED: 4. Logo should upload successfully
        """
        pass

    def test_005_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_006_navigate_to_5_a_side_event_and_add_5_legs_to_bet_slipornavigate_to_5aside_lobbygtpre_leaderboard_and_add_5_legs(self):
        """
        DESCRIPTION: Navigate to 5-a-side event and add 5 legs to bet slip
        DESCRIPTION: or
        DESCRIPTION: Navigate to 5aside lobby&gt;Pre-leaderboard and add 5 legs
        EXPECTED: User should be able to add 5 legs to bet slip
        """
        pass

    def test_007_enter_valid_stake_for_active_conteststake_should_be_gt_contest_stake(self):
        """
        DESCRIPTION: "Enter valid stake for active contest.
        DESCRIPTION: Stake should be &gt;= contest stake."
        EXPECTED: Entry confirmation message is displayed in bet receipt
        """
        pass

    def test_008_click_view_entry_button_to_navigate_to_pre_live_and_post_leader_boards_and_validate_new_background(self):
        """
        DESCRIPTION: Click "View Entry" button to navigate to pre-live and post leader boards and validate new background
        EXPECTED: Uploaded background image should display in pre/live and post leaderboards
        """
        pass
