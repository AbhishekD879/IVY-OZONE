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
class Test_C44870238__Verify_Full_Cashout_on_Open_Cashout_Tab_Bet_flow__Cash_out_button_Cashout_value_Confirm_Cash_out__Cashout_Sucessfull(Common):
    """
    TR_ID: C44870238
    NAME: -Verify Full Cashout on Open/Cashout Tab Bet flow --> Cash-out button (Cashout value)-->Confirm Cash-out -->Cashout Sucessfull
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_make_a_bet_from_a_cash_out_market(self):
        """
        DESCRIPTION: Make a bet from a cash out market
        EXPECTED: You should have made a bet from a cash out market.
        """
        pass

    def test_002_go_to_my_bets_open_bets_and_check_that_you_see_the_cash_out_button_for_this_bet(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and check that you see the Cash Out button for this bet.
        EXPECTED: The bet should show a Cash Out button.
        """
        pass

    def test_003_click_on_the_cash_out_button_and_check_that_you_see_a_flashing_confirm_cash_out_button(self):
        """
        DESCRIPTION: Click on the Cash Out button and check that you see a flashing Confirm Cash Out button
        EXPECTED: You should see the flashing Confirm Cash Out Button
        """
        pass

    def test_004_click_on_the_confirm_cash_out_button(self):
        """
        DESCRIPTION: Click on the Confirm Cash Out button
        EXPECTED: You should have clicked on the Confirm Cash Out button and your bet should have been cashed out
        """
        pass

    def test_005_verify_that_you_see_a_cash_out_successful_message(self):
        """
        DESCRIPTION: Verify that you see a Cash Out Successful message
        EXPECTED: You should see a Cash Out Successful message
        """
        pass

    def test_006_go_to_my_bets_settled_bets_and_verify_that_you_see_the_cashed_out_bet_there(self):
        """
        DESCRIPTION: Go to My Bets->Settled Bets and verify that you see the Cashed Out bet there.
        EXPECTED: Your Cashed Out bet should now be in My Bets->Settled Bets
        """
        pass

    def test_007_go_to_my_bets_open_bets_and_verify_that_the_cashed_out_bet_is_no_longer_there(self):
        """
        DESCRIPTION: Go to My Bets->Open Bets and verify that the Cashed Out bet is no longer there.
        EXPECTED: The Cashed Out bet should not be in My Bets->Open Bets.
        """
        pass
