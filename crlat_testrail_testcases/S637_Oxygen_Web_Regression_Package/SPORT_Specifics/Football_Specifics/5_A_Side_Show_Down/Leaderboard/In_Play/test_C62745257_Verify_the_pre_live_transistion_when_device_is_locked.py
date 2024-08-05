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
class Test_C62745257_Verify_the_pre_live_transistion_when_device_is_locked(Common):
    """
    TR_ID: C62745257
    NAME: Verify the pre-live transistion when device is locked.
    DESCRIPTION: 
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: 5-A Side Showdown menu should be configured in CMS
    PRECONDITIONS: 3: User's 5-A Side bets should enter into Showdown
    PRECONDITIONS: How to Configure Menu Item
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: 5-A-Side Showdown
    PRECONDITIONS: Path: /five-a-side-showdown
    PRECONDITIONS: To Qualify for Showdown
    PRECONDITIONS: 1) Event has an 'Active' Contest set-up
    PRECONDITIONS: with 'Display = Yes', a ‘Start Date’ not in the past, an ‘event ID’ and ‘Contest Size’ has not been reached
    PRECONDITIONS: 2) That user has not already placed the maximum amounts of bets allowed on that event
    PRECONDITIONS: The amount is set by the ‘Teams’ field in CMS
    PRECONDITIONS: 3) The 5-A-Side bet has 5 legs
    PRECONDITIONS: 4) The 5-A-Side bet with a qualifying stake
    PRECONDITIONS: The qualifying stake is set by the ‘Entry Stake’ field in CMS.
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus funds.
    """
    keep_browser_open = True

    def test_001_login_to_the_ladbrokes_application(self):
        """
        DESCRIPTION: Login to the ladbrokes application
        EXPECTED: User should be able to login
        """
        pass

    def test_002_navigate_to_5_a_side_lobby_and_place_a_bet_on_a_contest_which_is_going_to_live(self):
        """
        DESCRIPTION: Navigate to 5-a-side lobby and place a bet on a contest which is going to live
        EXPECTED: Customer should be able to place bet on the contest
        """
        pass

    def test_003_verify_if_the_customer_has_got_entry_confirmation_message_and_is_qualified_for_the_contest(self):
        """
        DESCRIPTION: verify if the customer has got entry confirmation message and is qualified for the contest
        EXPECTED: Customer should be qualified for the contest
        """
        pass

    def test_004_lock_the_device_and_wait_for_event_to_start_off_and_check_pre_live_transition(self):
        """
        DESCRIPTION: Lock the device and Wait for event to start off and check pre-live transition
        EXPECTED: User should lock the device
        """
        pass

    def test_005_unlock_the_device_when_event_has_kicked_off_and_check_whether_the_pre_live_transition_happened_successfully(self):
        """
        DESCRIPTION: Unlock the device when event has kicked off and check whether the pre-live transition happened successfully
        EXPECTED: Pre-live transition should happen when user unlocks the device after locking the device and keeping in background
        """
        pass
