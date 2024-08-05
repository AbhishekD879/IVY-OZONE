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
class Test_C2807909_Verify_MoneyBack_signposting_icon_on_Football_event_level(Common):
    """
    TR_ID: C2807909
    NAME: Verify "MoneyBack" signposting icon on Football event level
    DESCRIPTION: This test case verifies that the MoneyBack signposting icon is displayed on markets with MoneyBack flag available on the events details page.
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: [Promo / Signposting: MoneyBack] [1]
    DESCRIPTION: [1]:https://jira.egalacoral.com/browse/BMA-36252
    DESCRIPTION: [Redesign Promo Icons] [2]
    DESCRIPTION: [2]:https://jira.egalacoral.com/browse/BMA-43178
    PRECONDITIONS: Events with MoneyBack flag & Cashout flag ticked at market levels available
    """
    keep_browser_open = True

    def test_001_navigate_to_edp_of_event_with_moneyback_flag_ticked_at_market_level(self):
        """
        DESCRIPTION: Navigate to EDP of event with MoneyBack flag ticked at market level
        EXPECTED: * MoneyBack icon is displayed on the right side of market header (eg. on 'Match Result' market header)
        """
        pass

    def test_002_navigate_to_edp_of_event_with_moneyback_flag_ticked_at_market_level__cashout_flag_available(self):
        """
        DESCRIPTION: Navigate to EDP of event with MoneyBack flag ticked at market level & cashout flag available
        EXPECTED: * Cashout icon is present
        EXPECTED: * MoneyBack icon is displayed after CashOut icon
        """
        pass

    def test_003_expandcollapse_market_header(self):
        """
        DESCRIPTION: Expand/Collapse market header
        EXPECTED: * MoneyBack icon remains displayed on the right side of market header
        """
        pass

    def test_004_navigate_to_edp_of_event_with_moneyback_flag_not_ticked(self):
        """
        DESCRIPTION: Navigate to EDP of event with MoneyBack flag not ticked
        EXPECTED: * MoneyBack icon is not displayed
        """
        pass
