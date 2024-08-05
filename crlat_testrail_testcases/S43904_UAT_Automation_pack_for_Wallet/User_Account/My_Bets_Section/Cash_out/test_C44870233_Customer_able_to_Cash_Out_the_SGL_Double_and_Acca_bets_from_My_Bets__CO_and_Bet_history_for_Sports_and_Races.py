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
class Test_C44870233_Customer_able_to_Cash_Out_the_SGL_Double_and_Acca_bets_from_My_Bets__CO_and_Bet_history_for_Sports_and_Races(Common):
    """
    TR_ID: C44870233
    NAME: "Customer able to Cash Out the SGL, Double and Acca bets from My Bets -> CO and Bet history for Sports and Races
    DESCRIPTION: "Customer able to Cash Out the SGL, Double and Acca bets from My Bets -> CO and Bet history for Sports and Races
    DESCRIPTION: - Check Cashout successful and header balance
    DESCRIPTION: (b)Customer able to Partial Cash Out for SGL, Double and Acca bets in Open Bets/Cash Out
    DESCRIPTION: Check Cashout successful and header balance
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_user_shall_launch_test_appsite(self):
        """
        DESCRIPTION: User shall Launch Test App/Site
        EXPECTED: User successfully Launches Test App/Site
        """
        pass

    def test_002_user_shall_login_with_valid_credentials(self):
        """
        DESCRIPTION: User shall Login with valid credentials
        EXPECTED: User successfully Logins with valid credentials
        """
        pass

    def test_003_add_the_selections_in_to_bet_slip_and_place_the_bet_on_any_single_or_double_selections(self):
        """
        DESCRIPTION: Add the selections in to bet slip and place the bet on any single or double selections
        EXPECTED: User successfully added the selections in to bet slip and placed bet
        """
        pass

    def test_004_user_shall_go_to_my_bets_at_the_bottom_carousalfind_the_acca_bet_or_single_double_placed_and_taps_on_the_cash_out_option(self):
        """
        DESCRIPTION: User shall go to My Bets at the bottom carousal
        DESCRIPTION: Find the Acca Bet or single ,double placed and Taps on the Cash Out option
        EXPECTED: User successfully goes to My Bet at the bottom carousal
        EXPECTED: Find the Acca Bet,or single ,double placed and Taps on the Cash Out option
        """
        pass

    def test_005_observe_the_header_balance(self):
        """
        DESCRIPTION: Observe the header balance
        EXPECTED: Header balance should be updated
        """
        pass

    def test_006_user_can_go_to_bet_history_via_my_accounts_and_find_the_cash_out_tab_for_particular_bets(self):
        """
        DESCRIPTION: User can go to bet history via my accounts and find the cash out tab for particular bets.
        EXPECTED: User successfully goes to bet history via my accounts
        EXPECTED: Find the Acca Bet,or single ,double placed and Taps on the Cash Out option
        """
        pass
