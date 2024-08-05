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
class Test_C62745260_Verify_my_entries_are_loaded_in_Pre_Live_transistion(Common):
    """
    TR_ID: C62745260
    NAME: Verify my entries are loaded in Pre-Live transistion.
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
    PRECONDITIONS: The ‘Free Bet Allowed’ field will determine if the qualifying stake can come from bonus fun
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

    def test_004_wait_for_event_to_start_off_and_check_if_the_pre_live_transition_happened(self):
        """
        DESCRIPTION: Wait for event to start off and check if the pre-live transition happened
        EXPECTED: Event should kick off and transition should happen
        """
        pass

    def test_005_verify_if_the_my_entries_section_is_loaded_initially_along_with_llb_in_leaderboard_after_transition(self):
        """
        DESCRIPTION: Verify if the 'My entries' section is loaded initially along with LLB in Leaderboard after transition
        EXPECTED: 'My entries' section should be loaded immediately after transition
        """
        pass
