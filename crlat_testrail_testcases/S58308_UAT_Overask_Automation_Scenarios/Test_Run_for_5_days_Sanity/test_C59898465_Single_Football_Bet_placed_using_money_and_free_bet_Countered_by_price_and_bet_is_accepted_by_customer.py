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
class Test_C59898465_Single_Football_Bet_placed_using_money_and_free_bet_Countered_by_price_and_bet_is_accepted_by_customer(Common):
    """
    TR_ID: C59898465
    NAME: Single Football Bet placed using money and free bet Countered by price and bet is accepted by customer
    DESCRIPTION: 
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    PRECONDITIONS: Customer should have Freebets in the account
    """
    keep_browser_open = True

    def test_001_add_single_football_selection_to_betslip_and_place_bet_using_money_and_free_bet(self):
        """
        DESCRIPTION: Add Single Football selection to betslip and place bet using money and free bet
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_by_price_in_ob_ti_tool(self):
        """
        DESCRIPTION: Counter by Price in OB TI tool
        EXPECTED: Counter offer with the new price highlighted and updated potential returns shown to the customer.
        """
        pass

    def test_003_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: Bet receipt is shown to the customer and it shows that a free bet signposting
        EXPECTED: Balance should be updated correctly
        """
        pass

    def test_004_navigate_to_my_bets(self):
        """
        DESCRIPTION: Navigate to My Bets
        EXPECTED: The bet should be visible in My Bets and Account History.
        """
        pass

    def test_005_if_the_selection_has_cash_out(self):
        """
        DESCRIPTION: If the selection has cash out
        EXPECTED: Message saying "Free bets has a reduced Cash Out value" should be displayed in My Bets
        """
        pass

    def test_006_if_customer_declines_the_offer(self):
        """
        DESCRIPTION: If Customer declines the offer
        EXPECTED: The counter offer is closed and we should not see a bet in My Bets and Account History.
        """
        pass
