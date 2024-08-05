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
class Test_C44870286__Double_and_Singles_on_Football_Countered_by_Stake_for_Double_and_a_Price_for_one_of_the_Single_and_user_removes_the_counter_single_and_places_the_bet(Common):
    """
    TR_ID: C44870286
    NAME: - Double and Singles on Football Countered by Stake for Double and a Price for one of the Single and user removes the counter single and places the bet
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_2_single_football_oa_bets_and_one_oa_double_football_bet(self):
        """
        DESCRIPTION: Place 2 single Football OA bets and one OA double Football bet
        EXPECTED: The bets should go through to the OA flow
        """
        pass

    def test_002_in_the_ti_change_the_prices_for_the_single(self):
        """
        DESCRIPTION: In the TI, change the prices for the single
        EXPECTED: On the front end, you should see the counter offer with the original prices crossed out and the new prices next to them for the singles. The new prices should be highlighted.
        """
        pass

    def test_003_check_that_the_new_potential_returns_are_correct_for_the_singles_and_the_double(self):
        """
        DESCRIPTION: Check that the new Potential Returns are correct for the singles and the double.
        EXPECTED: The new Potential Returns should be correct
        """
        pass

    def test_004_place_the_bets(self):
        """
        DESCRIPTION: Place the bets
        EXPECTED: You should see the bet receipt, with the new prices for the singles and the new stake for the double
        """
        pass

    def test_005_check_the_bets_in_my_bets_open_bets_make_sure_that_the_bets_have_the_correct_prices_and_stake_and_correct_potential_returns(self):
        """
        DESCRIPTION: Check the bets in My Bets->Open Bets. Make sure that the bets have the correct prices and stake and correct Potential Returns
        EXPECTED: The bets should show in My Bets->Open Bets and they should have the correct prices, stake and Potential Returns.
        """
        pass

    def test_006_in_the_ti_change_the_stake_of_the_double_and_click_on_submit(self):
        """
        DESCRIPTION: In the TI, change the stake of the double and click on Submit
        EXPECTED: On the front end,
        EXPECTED: For the double, the new stake should be highlighted.
        """
        pass

    def test_007_now_repeat_steps_1_5_for_double(self):
        """
        DESCRIPTION: Now repeat steps 1-5 for double
        EXPECTED: 
        """
        pass
