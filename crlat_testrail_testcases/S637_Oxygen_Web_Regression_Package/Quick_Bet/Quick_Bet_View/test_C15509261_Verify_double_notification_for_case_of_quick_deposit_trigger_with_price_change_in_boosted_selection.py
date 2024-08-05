import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.quick_bet
@vtest
class Test_C15509261_Verify_double_notification_for_case_of_quick_deposit_trigger_with_price_change_in_boosted_selection(Common):
    """
    TR_ID: C15509261
    NAME: Verify double notification for case of quick deposit trigger with price change in boosted selection
    DESCRIPTION: This test case verifies double notification being shown for a boosted selection after price change with quick deposit trigger(button appearance) being activated.
    PRECONDITIONS: Quick Bet functionality should be enabled in CMS and user's settings
    PRECONDITIONS: User should be logged in and have at least 1 'Odds boost' token assigned to him/her and be applicable for a further used selection
    PRECONDITIONS: User should have a 'not expired' credit card set as default payment method
    PRECONDITIONS: User's balance should be below 50(USD/GBP/EUR/KR)
    PRECONDITIONS: Event selections should have an option to receive liveserve updates
    """
    keep_browser_open = True

    def test_001_log_in_with_user_that_has_no_betting_restrictions(self):
        """
        DESCRIPTION: Log in with user that has no betting restrictions
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_one_selection_to_quickbet(self):
        """
        DESCRIPTION: Add one selection to QuickBet
        EXPECTED: Quick Bet is displayed at the bottom of page(screen)
        """
        pass

    def test_003_enter_the_stake_value_that_exceeds_users_current_balance_but_doesnt_contradict_with_an_odds_boost_token_max_stake_value(self):
        """
        DESCRIPTION: Enter the 'Stake' value that exceeds user's current balance, but doesn't contradict with an 'Odds Boost' token max stake value.
        EXPECTED: Info icon and 'Please deposit a min of "<currency symbol>XX.XX to continue placing your bet' message is displayed below the on-screen keyboard immediately
        """
        pass

    def test_004_boost_the_selection_in_the_quickbet(self):
        """
        DESCRIPTION: 'Boost' the selection in the QuickBet
        EXPECTED: Additional price 'boosted' value in yellow frame appears on the right side of non-boosted 'crossed out' price value
        EXPECTED: 'Boost' button changes to 'Boosted'
        """
        pass

    def test_005_trigger_a_price_update_of_the_selection_in_the_quickbet(self):
        """
        DESCRIPTION: Trigger a price update of the selection in the QuickBet
        EXPECTED: * Message cyan background appears with text: 'Price changed from 'x' to 'y'
        EXPECTED: * Following message should appear within already shown message about minimum deposit: 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted price'
        EXPECTED: * Both messages should be shown one under another with 1 info icon shown on their left side
        EXPECTED: * Order of messages should be:
        EXPECTED: top message - minimum deposit message
        EXPECTED: bottom message - price change message
        """
        pass

    def test_006_repeat_steps_45_and_3_in_the_exact_same_order(self):
        """
        DESCRIPTION: Repeat steps 4,5 and 3 in the exact same order
        EXPECTED: 
        """
        pass

    def test_007_click_make_a_deposit_button(self):
        """
        DESCRIPTION: Click 'Make a Deposit' button
        EXPECTED: Quick Bet modal(pop-up) changes to Quick Deposit
        """
        pass

    def test_008_trigger_a_price_update_of_the_selection_used_in_the_quickbet(self):
        """
        DESCRIPTION: Trigger a price update of the selection used in the QuickBet
        EXPECTED: Warning Message on yellow/cyan background appears with text: 'Price changed from 'x' to 'y''
        """
        pass

    def test_009_click_x_in_order_to_quit_quick_deposit_modalpop_up(self):
        """
        DESCRIPTION: Click 'X' in order to quit Quick Deposit modal(pop-up)
        EXPECTED: * Quick Deposit modal(pop-up) changes to Quick Bet
        EXPECTED: * Both 'price change' and 'minimum deposit' messages should be shown one under another under Quick Stake buttons line
        EXPECTED: * Order of messages should remain the same as in ER of Step 5.
        """
        pass
