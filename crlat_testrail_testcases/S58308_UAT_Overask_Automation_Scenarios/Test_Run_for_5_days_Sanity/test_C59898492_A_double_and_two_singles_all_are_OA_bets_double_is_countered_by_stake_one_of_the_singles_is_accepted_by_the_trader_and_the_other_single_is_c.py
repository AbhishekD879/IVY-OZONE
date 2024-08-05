import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898492_A_double_and_two_singles_all_are_OA_bets_double_is_countered_by_stake_one_of_the_singles_is_accepted_by_the_trader_and_the_other_single_is_countered_by_price(Common):
    """
    TR_ID: C59898492
    NAME: A double and two singles all are OA bets, double is countered by stake, one of the singles is accepted by the trader and the other single is countered by price
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_two__selections_to_betslip_enter_stake_for_two_singles_and_doubletrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two  selections to Betslip ,Enter stake for two singles and Double
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_offer_by_price_for_one_singlestake_for_double_and_accept_the_single(self):
        """
        DESCRIPTION: Counter offer by price for one single,stake for double and accept the single
        EXPECTED: Counter offer shows the double with the stake highlighted, the single countered with price has the price highlighted and the single which was accepted has neither the price nor the stake highlighted
        EXPECTED: All bets have a remove button, even the accepted bet.
        """
        pass

    def test_003_if_user_accepts_the_bet(self):
        """
        DESCRIPTION: If user accepts the bet
        EXPECTED: Bet receipt shown to the customer.
        EXPECTED: Correct potential return should be shown
        EXPECTED: My Bets and Account History will show the bet.
        """
        pass

    def test_004_if_offer_is_declined_by_user(self):
        """
        DESCRIPTION: If offer is declined by user
        EXPECTED: Then no bet is placed and My Bets and Account History reflect this.
        """
        pass
