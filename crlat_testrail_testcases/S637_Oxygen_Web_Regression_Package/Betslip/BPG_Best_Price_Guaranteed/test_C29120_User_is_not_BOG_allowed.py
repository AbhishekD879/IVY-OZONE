import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C29120_User_is_not_BOG_allowed(Common):
    """
    TR_ID: C29120
    NAME: User is not BOG allowed
    DESCRIPTION: 
    PRECONDITIONS: - GP available checkbox is selected on market level in TI (isGpAvailable="true" attribute is returned for the market from SiteServer)
    PRECONDITIONS: - Event has SP and LP prices available
    PRECONDITIONS: - User has GP betting Disabled (OB ti -> Search for the customer -> Account Rules -> GP checkbox under NOT ALLOWED section should be CHECKED)
    PRECONDITIONS: ![](index.php?/attachments/get/107812894)
    """
    keep_browser_open = True

    def test_001_open_race_even_details_page_with_gp_price(self):
        """
        DESCRIPTION: Open <Race> Even Details Page with GP price
        EXPECTED: BOG icon is displayed on market header
        """
        pass

    def test_002_add_selection_to_betslip(self):
        """
        DESCRIPTION: Add selection to Betslip
        EXPECTED: BOG icon is NOT displayed on Betslip
        """
        pass

    def test_003_place_a_bet(self):
        """
        DESCRIPTION: Place a bet
        EXPECTED: BOG icon is NOT displayed on Betreceipt and in My Bets sections: Cash Out, Settle bet, Open Bets
        """
        pass

    def test_004_open_race_even_details_page_without_gp_price(self):
        """
        DESCRIPTION: Open <Race> Even Details Page without GP price
        EXPECTED: BOG icon is NOT displayed on market header
        """
        pass
