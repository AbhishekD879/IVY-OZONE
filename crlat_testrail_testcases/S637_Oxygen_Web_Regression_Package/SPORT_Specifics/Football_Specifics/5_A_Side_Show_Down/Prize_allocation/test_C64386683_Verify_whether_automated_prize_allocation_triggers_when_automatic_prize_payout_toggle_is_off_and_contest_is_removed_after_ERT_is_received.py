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
class Test_C64386683_Verify_whether_automated_prize_allocation_triggers_when_automatic_prize_payout_toggle_is_off_and_contest_is_removed_after_ERT_is_received(Common):
    """
    TR_ID: C64386683
    NAME: Verify whether automated prize allocation triggers when automatic prize payout toggle is off and contest is removed after ERT is received
    DESCRIPTION: 
    PRECONDITIONS: 1: User should have admin access to CMS
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
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds."
    PRECONDITIONS: 5) Toggle on automated prize allocation during contest creation
    """
    keep_browser_open = True

    def test_001_in_cms_create_a_contest_with_prizes_which_has_different_prizes_configured_and_user_should_place_bets_on_the_contest(self):
        """
        DESCRIPTION: In CMS, create a contest with prizes which has different prizes configured and User should place bets on the contest.
        EXPECTED: Prizes should be allocated in leaderboard as per configurations.
        """
        pass

    def test_002_once_event_is_live_and_ert_is_received_toggle_off_prize_payout_and_remove_contest(self):
        """
        DESCRIPTION: Once event is live and ERT is received, Toggle off prize payout and remove contest.
        EXPECTED: Prize payout Toggle should be switched off and contest should be removed
        """
        pass

    def test_003_verify_whether_prizes_are_allocated_after_ertplus10(self):
        """
        DESCRIPTION: Verify whether prizes are allocated after ERT+10
        EXPECTED: prizes should not be allocated
        """
        pass
