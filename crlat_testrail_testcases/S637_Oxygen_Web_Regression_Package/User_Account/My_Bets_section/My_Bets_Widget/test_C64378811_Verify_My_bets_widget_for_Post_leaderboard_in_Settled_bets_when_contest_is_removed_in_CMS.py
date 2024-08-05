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
class Test_C64378811_Verify_My_bets_widget_for_Post_leaderboard_in_Settled_bets_when_contest_is_removed_in_CMS(Common):
    """
    TR_ID: C64378811
    NAME: Verify My bets widget for Post-leaderboard in (Settled bets) when contest is removed in CMS
    DESCRIPTION: Verify 5AS Leaderboard widget should be removed in CMS
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: Create a contests for an events
    PRECONDITIONS: Contest should be created for future events
    PRECONDITIONS: Important: While creating contest give multiple prize combinations including Cash, freebet, ticket, voucher.
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    """
    keep_browser_open = True

    def test_001_login_to_sportsbook_with_user_that_satisfies_pre_conditions(self):
        """
        DESCRIPTION: Login to sportsbook with user that satisfies pre conditions.
        EXPECTED: User should be logged in successfully.
        """
        pass

    def test_002_navigate_to_the_postleaderboard_contest_and_login_with_a_user_which_has_bet_placed(self):
        """
        DESCRIPTION: Navigate to the Postleaderboard contest and login with a user which has bet placed.
        EXPECTED: user should able to see Post leaderboard which is configured in CMS.
        """
        pass

    def test_003_click_on_remove_button_and_save_the_contest_in_cms(self):
        """
        DESCRIPTION: Click on Remove Button and Save the contest in CMS.
        EXPECTED: User should not see 5-a-side leaderboard widget in My bets (settled bets) section, for the contest which is removed in CMS.
        """
        pass
