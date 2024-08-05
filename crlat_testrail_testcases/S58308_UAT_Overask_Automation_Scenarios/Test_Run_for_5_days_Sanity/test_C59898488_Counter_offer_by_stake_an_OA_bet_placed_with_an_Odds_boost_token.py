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
class Test_C59898488_Counter_offer_by_stake_an_OA_bet_placed_with_an_Odds_boost_token(Common):
    """
    TR_ID: C59898488
    NAME: Counter offer by stake an OA bet placed with an Odds boost token
    DESCRIPTION: 
    PRECONDITIONS: You should have an Odds Boost token to use
    """
    keep_browser_open = True

    def test_001_add_a_selection_to_bet_slip_or_quick_bet_boost_your_odds_and_trigger_overask(self):
        """
        DESCRIPTION: Add a selection to bet slip or Quick Bet, boost your odds and trigger Overask.
        EXPECTED: Your bet should have entered the Overask flow.
        """
        pass

    def test_002_in_ti_counter_offer_bet_by_stake(self):
        """
        DESCRIPTION: In TI, counter offer bet by stake.
        EXPECTED: You should have given a counter offer by stake.
        """
        pass

    def test_003_in_the_front_end_verify_that_you_see_the_new_stake_and_that_it_is_highlighted_in_yellow_and_that_the_new_potential_returns_are_correct(self):
        """
        DESCRIPTION: In the front end, verify that you see the new stake and that it is highlighted in yellow and that the new potential returns are correct.
        EXPECTED: The counter offer should show the new stake and it should be highlighted in yellow and the new potential returns should be correct.
        """
        pass

    def test_004_if_you_accept_the_bet_then_you_should_see_the_bet_receipt_with_the_new_stake_and_correct_potential_returns_and_the_bet_should_be_in_my_bets_open_bets(self):
        """
        DESCRIPTION: If you accept the bet, then you should see the bet receipt, with the new stake and correct potential returns, and the bet should be in My Bets->Open Bets
        EXPECTED: You should see the bet receipt and the bet should be seen in My Bets->Open Bets.
        """
        pass

    def test_005_if_you_decline_the_counter_offer_then_the_counter_offer_should_close_and_no_bet_should_have_been_placed_check_the_my_bets_open_bets_and_verify_there_is_no_sign_of_this_bet_there(self):
        """
        DESCRIPTION: If you decline the counter offer, then the counter offer should close and no bet should have been placed. Check the My Bets->Open Bets and verify there is no sign of this 'bet' there.
        EXPECTED: The counter offer should close and the bet should not have been placed and no bet should appear in My Bets->Open Bets.
        """
        pass
