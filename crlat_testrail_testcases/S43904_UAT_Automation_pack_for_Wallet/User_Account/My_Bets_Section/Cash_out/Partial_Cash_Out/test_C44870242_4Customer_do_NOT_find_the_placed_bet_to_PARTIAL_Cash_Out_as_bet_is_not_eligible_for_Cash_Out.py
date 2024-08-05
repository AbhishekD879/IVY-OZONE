import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C44870242_4Customer_do_NOT_find_the_placed_bet_to_PARTIAL_Cash_Out_as_bet_is_not_eligible_for_Cash_Out(Common):
    """
    TR_ID: C44870242
    NAME: 4.Customer do NOT find the placed bet to PARTIAL Cash Out as bet is not eligible for Cash Out
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_low_stake_bet_on_a_selection_which_has_high_odds_from_a_cash_out_market_eg_10p_bet_on_a_selection_which_has_odds_of_331_or_greater(self):
        """
        DESCRIPTION: Place a low stake bet on a selection which has high odds from a cash out market e.g. 10p bet on a selection which has odds of 33/1 or greater
        EXPECTED: You should have placed the bet
        """
        pass

    def test_002_go_to_my_bets_open_bets_and_verify_that_you_see_a_cash_out_button_but_no_partial_cash_out_button(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that you see a Cash Out button, but no Partial Cash Out button
        EXPECTED: You should only see a Cash Out button and no Partial Cash Out button
        """
        pass
