import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870232_Customer_able_to_Cash_Out_the_bets_placed_using_Free_bets(Common):
    """
    TR_ID: C44870232
    NAME: Customer able to Cash Out the bets placed using Free bets
    DESCRIPTION: 
    PRECONDITIONS: Free bet available
    PRECONDITIONS: UserName : goldenbuild  Password: password1
    """
    keep_browser_open = True

    def test_001_launch_httpsbeta_sportscoralcouk(self):
        """
        DESCRIPTION: Launch https://beta-sports.coral.co.uk/
        EXPECTED: HomePage is opened
        """
        pass

    def test_002_place_a_bet_on_selection_with_cashout_available_using_free_bet(self):
        """
        DESCRIPTION: Place a bet on selection with cashout available using free bet
        EXPECTED: Bet placed successfully
        """
        pass

    def test_003_verify_bet_in_my_bets__openbet(self):
        """
        DESCRIPTION: Verify bet in My bets > openbet
        EXPECTED: Bet is displayed in OpenBet
        """
        pass

    def test_004_verify_green_cashout_bar_is_available_for_bet(self):
        """
        DESCRIPTION: Verify Green cashout bar is available for bet
        EXPECTED: Cashout is displayed with cash out value
        """
        pass

    def test_005_click_on_cashout_and_verify_user_is__able_to_cash_out_the_bets_placed_using_free_bets(self):
        """
        DESCRIPTION: Click on Cashout and verify user is  able to Cash Out the bets placed using Free bets
        EXPECTED: Free bet, cashed out successfully
        EXPECTED: Header balance is updated with cashout value
        """
        pass
