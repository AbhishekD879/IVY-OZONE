import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C29441_Price_changes_on_Private_Markets(Common):
    """
    TR_ID: C29441
    NAME: Price changes on Private Markets
    DESCRIPTION: This test case verifies Price changes on Private Markets.
    DESCRIPTION: AUTOTEST: [C9770234]
    PRECONDITIONS: User should be logged in and has Private Market available
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: For setting private markets use the link:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+Setup+and+Use+Private+Markets
    """
    keep_browser_open = True

    def test_001_trigger_price_change_for_private_market_outcome(self):
        """
        DESCRIPTION: Trigger price change for private market outcome
        EXPECTED: 'Price/Odds' button immediately displays new price and for a few seconds it changes its color to:
        EXPECTED: *   blue color if price has decreased
        EXPECTED: *   pink color if price has increased
        """
        pass
