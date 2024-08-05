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
class Test_C44870276__Single_Football_Bet_Countered_by_Stake(Common):
    """
    TR_ID: C44870276
    NAME: - Single Football Bet Countered by Stake
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_single_overask_bet_on_a_football_game(self):
        """
        DESCRIPTION: Place a single overask bet on a football game
        EXPECTED: You should have placed an overask bet
        """
        pass

    def test_002_in_traders_ti_give_a_counter_offer_by_stake(self):
        """
        DESCRIPTION: In trader's TI, give a counter offer by stake
        EXPECTED: You should see a counter offer on the front end
        """
        pass

    def test_003_check_that_the_stake_is_highlighted_in_yellow_and_that_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the stake is highlighted in yellow and that the potential returns are correct
        EXPECTED: The stake should be highlighted and the potential returns should be correct
        """
        pass

    def test_004_click_on_place_bet_and_check_the_bet_receipt_for_the_correct_stake_and_potential_returns(self):
        """
        DESCRIPTION: Click on Place Bet and check the Bet Receipt for the correct stake and potential returns
        EXPECTED: Your bet should have been placed and the correct stake and potential returns should be seen
        """
        pass

    def test_005_check_the_bet_in_my_bets_open_bets_for_the_correct_stake_and_potential_returns(self):
        """
        DESCRIPTION: Check the bet in My Bets->Open Bets for the correct stake and potential returns.
        EXPECTED: You should see the bet with the correct stake and potential returns.
        """
        pass
