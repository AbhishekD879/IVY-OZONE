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
class Test_C59898510_Bet_more_than_balance_Quick_Deposit__Quick_Deposit_should_open_and_then_after_you_add_funds_the_bet_should_go_to_the_OA_flow(Common):
    """
    TR_ID: C59898510
    NAME: Bet more than balance (Quick Deposit) - Quick Deposit should open and then after you add funds, the bet should go to the OA flow
    DESCRIPTION: 
    PRECONDITIONS: You have Quick Deposit enabled for your user i.e. you have a card attached
    """
    keep_browser_open = True

    def test_001_add_a_selection_to_quick_betbet_slip_and_add_a_stake_that_is_greater_than_that_selections_max_stake_and_is_greater_than_your_balance(self):
        """
        DESCRIPTION: Add a selection to Quick Bet/Bet Slip and add a stake that is greater than that selection's max stake and is greater than your balance.
        EXPECTED: You should have added stake greater than the selection's max stake and your balance.
        """
        pass

    def test_002_verify_that_you_see_the_message_please_deposit_a_min_of_and_that_you_see_a_make_a_deposit_button(self):
        """
        DESCRIPTION: Verify that you see the message "Please deposit a min of..." and that you see a Make A Deposit button.
        EXPECTED: You should see the message and the Make A Deposit button
        """
        pass

    def test_003_click_on_make_a_deposit_add_an_amount_that_will_allow_you_to_place_the_bet_and_then_click_on_deposit__place_bet(self):
        """
        DESCRIPTION: Click on Make A Deposit, add an amount that will allow you to place the bet and then click on Deposit & Place Bet.
        EXPECTED: You should have clicked on Make A Deposit, added an amount to cover the bet and clicked on Deposit & Place Bet
        """
        pass

    def test_004_verify_that_you_are_taken_to_the_overask_flow(self):
        """
        DESCRIPTION: Verify that you are taken to the Overask flow.
        EXPECTED: You should be taken to the Overask flow.
        """
        pass

    def test_005_accept_the_bet_and_verify_the_bet_receipt_is_correct_and_that_the_bet_shows_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Accept the bet and verify the bet receipt is correct and that the bet shows in My Bets->Open Bets
        EXPECTED: The bet receipt should be correct and My Bets->Open Bets should correctly show the bet.
        """
        pass
