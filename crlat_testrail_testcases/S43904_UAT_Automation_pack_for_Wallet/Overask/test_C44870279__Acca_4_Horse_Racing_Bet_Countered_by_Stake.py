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
class Test_C44870279__Acca_4_Horse_Racing_Bet_Countered_by_Stake(Common):
    """
    TR_ID: C44870279
    NAME: - Acca 4 Horse Racing Bet Countered by Stake
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_4_fold_hr_acca_with_a_stake_that_will_take_it_to_overask(self):
        """
        DESCRIPTION: Place a 4 fold HR ACCA with a stake that will take it to Overask
        EXPECTED: You should have placed the bet and it should have gone to Overask
        """
        pass

    def test_002_in_traders_ti_counter_by_stake_ie_reduce_the_stake(self):
        """
        DESCRIPTION: In Trader's TI, counter by stake i.e. reduce the stake
        EXPECTED: You should have given a counter offer by reducing the stake
        """
        pass

    def test_003_verify_that_you_see_the_counter_offer_at_the_front_end_that_the_new_stake_is_highlighted_in_yellow_and_that_the_new_potential_returns_are_correct(self):
        """
        DESCRIPTION: Verify that you see the counter offer at the front end, that the new stake is highlighted in yellow and that the new potential returns are correct.
        EXPECTED: In the counter offer, only the new stake should be highlighted in yellow and the new potential returns should be correct.
        """
        pass

    def test_004_place_the_bet_and_in_the_bet_receipt_verify_that_you_see_the_correct_stake_and_returns(self):
        """
        DESCRIPTION: Place the bet and in the bet receipt, verify that you see the correct stake and returns
        EXPECTED: You should have placed the bet and in the bet receipt, you should see the correct stake and returns.
        """
        pass

    def test_005_verify_that_the_bet_is_showing_in_my_bets_open_bets_and_that_it_shows_the_correct_stake_and_potential_returns(self):
        """
        DESCRIPTION: Verify that the bet is showing in My Bets->Open Bets and that it shows the correct stake and potential returns.
        EXPECTED: The bet should show in My Bets->Open Bets and that it shows the correct stake and returns.
        """
        pass
