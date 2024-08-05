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
class Test_C59898500_Bet_placement_when_one_OA_bet_is_rejected_by_the_trader_and_the_other_OA_bet_is_counter_offered_by_price_and_accepted_by_the_customer(Common):
    """
    TR_ID: C59898500
    NAME: Bet placement when one OA bet is rejected by the trader and the other OA bet is counter offered by price and accepted by the customer.
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_two_selection_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add two selection to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_if_trader_rejects_one_oa_bet_and_the_other_oa_bet_is_counter_offered_by_price(self):
        """
        DESCRIPTION: If trader rejects one OA bet and the other OA bet is counter offered by price
        EXPECTED: The counter offer should show the bet that was not accepted with a 'trader did not accept...' message.
        EXPECTED: The other offer should have the price highlighted and show updated potential returns.
        """
        pass

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt.
        EXPECTED: Balance should be updated correctly
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        pass

    def test_004_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass
