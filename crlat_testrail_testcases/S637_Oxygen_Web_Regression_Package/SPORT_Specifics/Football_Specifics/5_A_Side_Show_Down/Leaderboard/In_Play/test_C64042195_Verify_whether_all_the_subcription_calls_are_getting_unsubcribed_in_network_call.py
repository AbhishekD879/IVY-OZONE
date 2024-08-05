import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.5_a_side
@vtest
class Test_C64042195_Verify_whether_all_the_subcription_calls_are_getting_unsubcribed_in_network_call(Common):
    """
    TR_ID: C64042195
    NAME: Verify whether all the subcription calls are getting unsubcribed in network call
    DESCRIPTION: To verify whether all the subcription calls are getting unsubcribed in network call
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
        EXPECTED: Fill all the Mand* fields and save the contest
        """
        pass

    def test_004_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User should be logged in successfully
        """
        pass

    def test_005_navigate_to_5_a_side_event_and_add_5_legs_to_bet_slipornavigate_to_5aside_lobbygtpre_leaderboard_and_add_5_legs(self):
        """
        DESCRIPTION: Navigate to 5-a-side event and add 5 legs to bet slip
        DESCRIPTION: or
        DESCRIPTION: Navigate to 5aside lobby&gt;Pre-leaderboard and add 5 legs
        EXPECTED: User should be able to add 5 legs to bet slip
        """
        pass

    def test_006_enter_valid_stake_for_active_conteststake_should_be_gt_contest_stake(self):
        """
        DESCRIPTION: "Enter valid stake for active contest.
        DESCRIPTION: Stake should be &gt;= contest stake."
        EXPECTED: Entry confirmation message is displayed in bet receipt
        """
        pass

    def test_007_wait_till_the_contest_goes_live(self):
        """
        DESCRIPTION: Wait till the contest goes live
        EXPECTED: Contest should be live
        """
        pass

    def test_008_navigate_to_network_call_and_check_the_subscription_messages_and_also_check_if_they_are_unsubsscribed(self):
        """
        DESCRIPTION: Navigate to Network call and check the subscription messages and also check if they are unsubsscribed
        EXPECTED: For each open subscription message there should be a closed subscription call
        """
        pass
