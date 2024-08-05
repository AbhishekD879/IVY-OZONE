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
class Test_C44870284__Acca_5_Tennis_Bet_Countered_by_Price(Common):
    """
    TR_ID: C44870284
    NAME: - Acca 5 Tennis Bet Countered by Price
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_an_oa_5_fold_tennis_acca(self):
        """
        DESCRIPTION: Place an OA 5-fold tennis ACCA
        EXPECTED: The bet should have gone through to TI
        """
        pass

    def test_002_in_ti_change_the_price_of_all_the_selections_or_just_some_of_them_and_click_submit(self):
        """
        DESCRIPTION: In TI, change the price of all the selections or just some of them and click Submit
        EXPECTED: On the Front End, you should see a counter offer with the prices which have been changed crossed out and the new prices highlighted in yellow.
        """
        pass

    def test_003_check_that_the_potential_returns_are_correct_on_the_counter_offer(self):
        """
        DESCRIPTION: Check that the Potential Returns are correct on the counter offer
        EXPECTED: The Potential Returns should be correct
        """
        pass

    def test_004_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: You should see the bet receipt and it should have the correct Potential Returns
        """
        pass

    def test_005_check_that_the_bets_are_correctly_seen_in_________my_bets_open_bets(self):
        """
        DESCRIPTION: Check that the bets are correctly seen in         My Bets->Open Bets
        EXPECTED: The bets should correctly be seen in My Bets->Open Bets
        """
        pass
