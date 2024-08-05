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
class Test_C2696859_Verify_SmartBoost_signposting_icon_on_market_level(Common):
    """
    TR_ID: C2696859
    NAME: Verify SmartBoost signposting icon on market level
    DESCRIPTION: This test case verifies that the Smart Boost signposting icon is displayed on market level.
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: [BMA-33496 Promo / Signposting : Price Boost : EDP] [1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-33496
    DESCRIPTION: [BMA-43178 Redesign Promo Icons] [2]
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-43178
    PRECONDITIONS: 'PriceBoost' promo flag should be added to the Football Event on market level.
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_event(self):
        """
        DESCRIPTION: Navigate to EDP of event
        EXPECTED: * Price Boost icon is displayed on the right side of market header (eg. 'Match Result')
        """
        pass

    def test_002_navigate_to_edp_of_event_with_price_boost_flag_ticked_at_market_level__cashout_flag_available(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag ticked at market level & cashout flag available
        EXPECTED: * Cashout icon is present
        EXPECTED: * Price Boost icon is displayed after it
        """
        pass

    def test_003_expandcollapse_market_header(self):
        """
        DESCRIPTION: Expand/Collapse market header
        EXPECTED: * Price Boost icon remains displayed on the right side of market header
        """
        pass

    def test_004_navigate_to_edp_of_event_with_price_boost_flag_not_ticked(self):
        """
        DESCRIPTION: Navigate to EDP of event with Price Boost flag not ticked
        EXPECTED: * Price Boost icon is not displayed
        """
        pass
