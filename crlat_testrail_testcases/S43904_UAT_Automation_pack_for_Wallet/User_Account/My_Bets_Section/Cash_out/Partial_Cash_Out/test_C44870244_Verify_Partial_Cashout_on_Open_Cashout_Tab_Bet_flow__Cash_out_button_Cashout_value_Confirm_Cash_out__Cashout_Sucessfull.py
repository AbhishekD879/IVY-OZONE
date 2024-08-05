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
class Test_C44870244_Verify_Partial_Cashout_on_Open_Cashout_Tab_Bet_flow__Cash_out_button_Cashout_value_Confirm_Cash_out__Cashout_Sucessfull(Common):
    """
    TR_ID: C44870244
    NAME: Verify Partial Cashout on Open/Cashout Tab Bet flow --> Cash-out button (Cashout value)-->Confirm Cash-out -->Cashout Sucessfull
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_place_a_single_on_a_cash_out_market(self):
        """
        DESCRIPTION: Place a single on a Cash Out market
        EXPECTED: You should have placed a single
        """
        pass

    def test_002_go_to_my_bets_open_bets_and_verify_that_your_bet_has_partial_cash_out_available_if_it_does_not_place_more_single_bets_until_you_have_a_bet_with_partial_cash_out(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that your bet has Partial Cash Out available. (If it does not, place more single bets until you have a bet with partial cash out)
        EXPECTED: Your bet should have Partial Cash Out available.
        """
        pass

    def test_003_click_on_the_partial_cash_out_button_and_verify_that_you_see_a_slider_where_you_can_vary_the_amount_that_you_can_cash_out(self):
        """
        DESCRIPTION: Click on the Partial Cash Out button and verify that you see a slider where you can vary the amount that you can cash out.
        EXPECTED: You should have clicked on the Partial Cash Out button and see a slider
        """
        pass

    def test_004_move_the_slider_in_any_direction_and_cash_out_the_bet(self):
        """
        DESCRIPTION: Move the slider in any direction and cash out the bet
        EXPECTED: You should have cashed out
        """
        pass

    def test_005_verify_that_you_see_the_partial_cash_out_successful_message_and_that_you_header_balance_has_updated(self):
        """
        DESCRIPTION: Verify that you see the Partial Cash Out Successful message and that you header balance has updated
        EXPECTED: You should see a Partial Cash Out Successful message and your header should have updated
        """
        pass

    def test_006_go_to_my_bets_settled_bets_and_verify_that_the_bet_is_not_seen_there(self):
        """
        DESCRIPTION: Go to My Bets->Settled Bets and verify that the bet is not seen there
        EXPECTED: Your partially cashed out bet should not be seen in My Bets->Settled Bets
        """
        pass

    def test_007_go_to_my_bets_open_bets_and_verify_that_the_bet_is_still_there_with_a_partial_cash_out_history_link(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that the bet is still there with a PARTIAL CASH OUT HISTORY LINK
        EXPECTED: Your the bet should still be there with a PARTIAL CASH OUT HISTORY LINK
        """
        pass

    def test_008_click_on_the_partial_cash_out_history_link(self):
        """
        DESCRIPTION: Click on the PARTIAL CASH OUT HISTORY LINK
        EXPECTED: Partial Bet History should be seen
        """
        pass
