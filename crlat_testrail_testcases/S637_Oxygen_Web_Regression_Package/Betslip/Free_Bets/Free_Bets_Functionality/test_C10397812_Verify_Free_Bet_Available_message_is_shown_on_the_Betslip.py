import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C10397812_Verify_Free_Bet_Available_message_is_shown_on_the_Betslip(Common):
    """
    TR_ID: C10397812
    NAME: Verify Free Bet Available message is shown on the Betslip
    DESCRIPTION: This test case verifies, that if User has Free Bet available, Free Bet Available message is shown on Betslip.
    PRECONDITIONS: 1. User has Free Bet available on their account
    PRECONDITIONS: 2. User is logged in
    PRECONDITIONS: 3. User has no bets added to the Betslip.
    """
    keep_browser_open = True

    def test_001_navigate_to_the_betslip(self):
        """
        DESCRIPTION: Navigate to the Betslip
        EXPECTED: Betslip is empty
        EXPECTED: There is no message about Free Bets available shown on an empty Betslip.
        """
        pass

    def test_002_click_on_the_selection(self):
        """
        DESCRIPTION: Click on the selection
        EXPECTED: Quick Bet pop-up is open.
        """
        pass

    def test_003_verify_that_no_messages_about_free_bet_expiry_are_shown_on_quick_bet_pop_up(self):
        """
        DESCRIPTION: Verify, that NO messages about Free Bet Expiry are shown on Quick Bet pop-up.
        EXPECTED: No messages about Free Bet Expiry are shown on Quick Bet pop-up.
        """
        pass

    def test_004_press_add_to_betslip_button_and_navigate_to_betslip(self):
        """
        DESCRIPTION: Press "Add to Betslip" button and navigate to Betslip.
        EXPECTED: Betslip is open.
        EXPECTED: Message is shown:
        EXPECTED: You have a free bet available!
        """
        pass

    def test_005_do_some_changes_in_scope_of_current_bet_placement_session_add_more_bets_delete_some_of_them_etc(self):
        """
        DESCRIPTION: Do some changes in scope of current bet placement session (add more bets, delete some of them etc)
        EXPECTED: Verify, that message "You have a free bet available!" is shown each time when User opens Betslip.
        """
        pass

    def test_006_press_close_button_on_free_bet_message(self):
        """
        DESCRIPTION: Press close button on Free Bet message.
        EXPECTED: Free Bet message is closed.
        """
        pass

    def test_007_verify_that_free_bet_message_isnt_shown_in_the_same_bet_placement_session_add_more_bets_delete_some_of_them_etc(self):
        """
        DESCRIPTION: Verify, that Free Bet Message isn't shown in the same bet placement session (add more bets, delete some of them etc).
        EXPECTED: Free Bet Message isn't shown.
        """
        pass

    def test_008_clear_betslip_add_a_bet_to_the_betslip_again_and_open_the_betslip(self):
        """
        DESCRIPTION: Clear Betslip, add a bet to the Betslip again and open the Betslip.
        EXPECTED: Message is shown:
        EXPECTED: You have a free bet available!
        """
        pass

    def test_009_place_a_betclose_the_betslipopen_empty_betslip(self):
        """
        DESCRIPTION: Place a bet
        DESCRIPTION: Close the Betslip
        DESCRIPTION: Open empty Betslip
        EXPECTED: "You have a free bet available!" message is NOT shown.
        """
        pass
