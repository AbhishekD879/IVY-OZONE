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
class Test_C62700677_Verify_entry_confirmation_bet_receipt_for_valid_5_a_side_bet_when_5_a_side_Logo_Image_is_uploaded_in_Contest_creation_page(Common):
    """
    TR_ID: C62700677
    NAME: Verify entry confirmation bet receipt for valid 5-a-side bet, when 5-a-side Logo Image is uploaded in Contest creation page.
    DESCRIPTION: Verify entry confirmation bet receipt for valid 5-a-side bet, when 5-a-side Logo Image is uploaded in Contest creation page.
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
        EXPECTED: Fill all the Mandatory * fields and save the contest
        """
        pass

    def test_004_upload_logo_which_allows_to_replaces_the_5_a_side_logo_within_the_leaderboard_header(self):
        """
        DESCRIPTION: Upload ‘Logo’ which allows to replaces the 5-A-Side logo within the Leaderboard header.
        EXPECTED: Logo should upload successfully
        """
        pass

    def test_005_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_006_navigate_to_5_a_side_event_and_add_5_legs_to_bet_slipornavigate_to_5_a_side_lobby__gt_pre_leaderboard_and_add_5_legs(self):
        """
        DESCRIPTION: Navigate to 5-a-side event and add 5 legs to bet slip
        DESCRIPTION: or
        DESCRIPTION: Navigate to 5-a-side lobby -&gt; Pre-leaderboard and add 5 legs
        EXPECTED: User should be able to add 5 legs to bet slip
        """
        pass

    def test_007_enter_valid_stake_for_active_conteststake_should_be_gt_contest_stake(self):
        """
        DESCRIPTION: Enter valid stake for active contest.
        DESCRIPTION: Stake should be &gt;= contest stake.
        EXPECTED: Entry confirmation message is displayed in bet receipt with new 5-a-side logo.
        """
        pass
