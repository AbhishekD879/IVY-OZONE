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
class Test_C59898454_Double_and_Singles_on_Football_Countered_by_Stake_for_Double_and_a_Price_for_one_of_the_Singles(Common):
    """
    TR_ID: C59898454
    NAME: Double and Singles on Football Countered by Stake for Double and a Price for one of the Singles
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_two_selections_from_football_sport_to_betslip(self):
        """
        DESCRIPTION: Add two selections from Football sport to Betslip
        EXPECTED: Selections are added to betslip
        """
        pass

    def test_002_enter_stake_for_both_singles_and_doublestrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Enter stake for both singles and doubles
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_003_counter_by_stake_for_double_and_a_price_for_one_of_the_singles(self):
        """
        DESCRIPTION: Counter by Stake for Double and a Price for one of the Singles
        EXPECTED: Customer should be shown a counter offer with the stake for the double highlighted and the price of the single being highlighted.
        EXPECTED: Updated potential returns should be shown to the customer on FE
        """
        pass

    def test_004_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: Balance should be updated correctly
        """
        pass

    def test_005_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        pass

    def test_006_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass
