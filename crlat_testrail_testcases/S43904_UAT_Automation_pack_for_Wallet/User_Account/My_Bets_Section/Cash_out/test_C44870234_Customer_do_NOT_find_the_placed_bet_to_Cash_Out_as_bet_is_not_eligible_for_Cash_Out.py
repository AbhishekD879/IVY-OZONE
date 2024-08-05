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
class Test_C44870234_Customer_do_NOT_find_the_placed_bet_to_Cash_Out_as_bet_is_not_eligible_for_Cash_Out(Common):
    """
    TR_ID: C44870234
    NAME: Customer do NOT find the placed bet to Cash Out as bet is not eligible for Cash Out
    DESCRIPTION: ve
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_make_a_bet_from_a_market_that_does_not_have_cash_out(self):
        """
        DESCRIPTION: Make a bet from a market that does not have cash out.
        EXPECTED: You should have made a bet on a market which does not have cash out.
        """
        pass

    def test_002_check_that_this_bet_does_not_show_a_cash_out_button_in_my_bets_open_bets(self):
        """
        DESCRIPTION: Check that this bet does not show a Cash Out button in My Bets->Open Bets.
        EXPECTED: This bet should not show a Cash Out button in My Bets->Open Bets
        """
        pass
