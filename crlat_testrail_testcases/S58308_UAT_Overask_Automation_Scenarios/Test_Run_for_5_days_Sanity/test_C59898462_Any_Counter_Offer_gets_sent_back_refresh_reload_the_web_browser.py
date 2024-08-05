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
class Test_C59898462_Any_Counter_Offer_gets_sent_back_refresh_reload_the_web_browser(Common):
    """
    TR_ID: C59898462
    NAME: Any Counter Offer gets sent back refresh/reload the  web browser
    DESCRIPTION: The desktop equivalent to this is log out and close the tab. Open a new tab in the same browser and check that the bet is still there and you can place the bet.
    PRECONDITIONS: Load Oxygen/Roxanne Application and login
    PRECONDITIONS: Overask is enabled for logged in user
    """
    keep_browser_open = True

    def test_001_add_selection_to_quick_betbetsliptrigger_overask__try_to_place_bet_with_higher_stake_than_a_max_allowed_stake(self):
        """
        DESCRIPTION: Add selection to Quick bet/Betslip
        DESCRIPTION: Trigger Overask ( try to place bet with higher stake than a max allowed stake)
        EXPECTED: Overask flow is triggered
        """
        pass

    def test_002_counter_offer_by_stakeprice(self):
        """
        DESCRIPTION: Counter Offer by Stake/Price
        EXPECTED: Counter offer gets sent back
        """
        pass

    def test_003_refreshreload_the_web_browser(self):
        """
        DESCRIPTION: Refresh/reload the web browser.
        EXPECTED: Should still see the running counter offer, with the time still counting down and the accept and decline buttons
        """
        pass

    def test_004_if_customer_accepts_the_offer(self):
        """
        DESCRIPTION: If Customer accepts the offer
        EXPECTED: The bet is placed and they are taken to the bet receipt
        EXPECTED: Balance should be updated
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
