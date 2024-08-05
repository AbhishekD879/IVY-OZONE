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
class Test_C44870280__Treble_Horse_Racing_Bet_Countered_by_Price(Common):
    """
    TR_ID: C44870280
    NAME: - Treble Horse Racing Bet Countered by Price
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_hr_treble_with_a_stake_that_will_take_it_to_overask(self):
        """
        DESCRIPTION: Place a HR treble with a stake that will take it to Overask
        EXPECTED: You should have placed the bet and it should have gone to Overask
        """
        pass

    def test_002_in_traders_ti_counter_by_price_ie_reduce_the_price_you_can_reduce_the_prices_of_all_or_some_of_the_selections_in_the_bet(self):
        """
        DESCRIPTION: In Trader's TI, counter by price i.e. reduce the price. You can reduce the prices of all or some of the selections in the bet.
        EXPECTED: You should have given a counter offer by reducing the prices of all or some of the selections
        """
        pass

    def test_003_in_the_counter_offer_verify_that_only_the_prices_that_you_changed_in_ti_the_are_highlighted_in_yellow_and_verify_that_the_new_potential_returns_are_correct(self):
        """
        DESCRIPTION: In the counter offer, verify that only the prices that you changed in TI the are highlighted in yellow and verify that the new potential returns are correct.
        EXPECTED: You should see changed prices in yellow and you should see the correct potential returns.
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
