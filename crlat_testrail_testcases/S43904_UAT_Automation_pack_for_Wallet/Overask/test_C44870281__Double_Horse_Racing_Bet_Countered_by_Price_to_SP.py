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
class Test_C44870281__Double_Horse_Racing_Bet_Countered_by_Price_to_SP(Common):
    """
    TR_ID: C44870281
    NAME: - Double Horse Racing Bet Countered by Price to SP
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_an_oa_hr_double_bet_using_lp_prices(self):
        """
        DESCRIPTION: Place an OA HR double bet using LP prices
        EXPECTED: The bet should have gone to the Over Ask flow
        """
        pass

    def test_002_in_the_traders_interface_give_a_counter_offer_by_changing_the_prices_to_sp_and_click_submit(self):
        """
        DESCRIPTION: In the Trader's Interface, give a counter offer by changing the prices to SP and click Submit
        EXPECTED: On the Front End, you should see a counter offer with the LP prices crossed out and next to them should be the text SP and it should be highlighted in yellow
        """
        pass

    def test_003_check_that_the_potential_returns_are_showing_as_na(self):
        """
        DESCRIPTION: Check that the Potential Returns are showing as N/A
        EXPECTED: The Potential Returns should be shown as N/A
        """
        pass

    def test_004_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: You should see the bet receipt and the prices should be SP and the Potential Returns should be N/A
        """
        pass
