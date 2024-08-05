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
class Test_C64537829_Verify_inbox_notifications_for_the_customer_after_the_rewards_are_received(Common):
    """
    TR_ID: C64537829
    NAME: Verify inbox notifications for the customer after the rewards are received
    DESCRIPTION: 
    PRECONDITIONS: "1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: Creating contests
    PRECONDITIONS: Create multiple contests for different events
    PRECONDITIONS: Contest should be created for future events
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) Place  few 5-A-Side bets by selecting any contest with a qualifying stake and non qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: 5) Wait for Event to start
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    """
    keep_browser_open = True

    def test_001_in_cms_create_a_contest_with_prizes_which_has_different_prizes_configured_and_user_should_place_bets_on_the_contest(self):
        """
        DESCRIPTION: In CMS, create a contest with prizes which has different prizes configured and User should place bets on the contest.
        EXPECTED: Prizes should be allocated in leaderboard as per configurations.
        """
        pass

    def test_002_once_event_is_live_and_ert_is_received_check_the_prize_allocation(self):
        """
        DESCRIPTION: Once event is live and ERT is received, Check the prize allocation
        EXPECTED: Prizes should be allocated as configured
        """
        pass

    def test_003_now_check_customers_inbox_notifications(self):
        """
        DESCRIPTION: Now check customers inbox notifications
        EXPECTED: Customer should recieve inbox notification for the rewards received.
        EXPECTED: Ex: There are 2 rewards received(cash, freebet) Customer should get 2 inbox notifications.
        """
        pass
