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
class Test_C59898453_Acca_5_Tennis_Basketball_Bet_Countered_by_Price(Common):
    """
    TR_ID: C59898453
    NAME: Acca 5 Tennis/Basketball Bet Countered by Price
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_five_selections_from_tennisbasketball_sport_to_betsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add five selections from Tennis/Basketball sport to Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_by_price_for_one_of_the_selection_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by Price for one of the selection in OB TI tool
        EXPECTED: Counter offer with the new price highlighted and updated potential returns shown to the customer on FE
        """
        pass

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: Balance should be updated correctly
        """
        pass

    def test_004_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        pass

    def test_005_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass
