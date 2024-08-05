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
class Test_C44870274__Single_Horse_Racing_Bet_Countered_by_Price_to_SP(Common):
    """
    TR_ID: C44870274
    NAME: - Single Horse Racing Bet Countered by Price to SP
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_single_overask_bet_on_a_horse(self):
        """
        DESCRIPTION: Place a single overask bet on a horse
        EXPECTED: You should have placed an overask bet
        """
        pass

    def test_002_in_traders_ti_give_a_counter_offer_by_price_to_sp(self):
        """
        DESCRIPTION: In trader's TI, give a counter offer by price to SP
        EXPECTED: You should see a counter offer on the front end
        """
        pass

    def test_003_check_that_the_price_is_sp_and_it_is_highlighted_in_yellow_and_that_the_potential_returns_are_showing_as_na(self):
        """
        DESCRIPTION: Check that the price is SP and it is highlighted in yellow and that the potential returns are showing as N/A
        EXPECTED: The price should be SP and should be highlighted and the potential returns should be N/A
        """
        pass

    def test_004_click_on_place_bet_and_check_the_bet_receipt_shows_the_price_as_sp_and_potential_returns_as_na(self):
        """
        DESCRIPTION: Click on Place Bet and check the Bet Receipt shows the price as SP and Potential returns as N/A
        EXPECTED: Your bet should have been placed and the price on the receipt should be SP and Potential returns should be N/A
        """
        pass

    def test_005_check_the_bet_in_my_bets_open_bets_for_the_correct_price_sp_and_potential_returns_as_na(self):
        """
        DESCRIPTION: Check the bet in My Bets->Open Bets for the correct price (SP) and potential returns as N/A
        EXPECTED: You should see the bet with a price of SP and potential returns of N/A.
        """
        pass
