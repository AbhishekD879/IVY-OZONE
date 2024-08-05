import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.quick_bet
@vtest
class Test_C717043_Verify_Selections_Details_for_regular_selection(Common):
    """
    TR_ID: C717043
    NAME: Verify Selection`s Details for regular selection
    DESCRIPTION: This test case verifies selections details for regular selection within Quick Bet
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. To get event`s details open Dev Tools -> Networks -> WS -> '?EIO=3&transport=websocket' request -> Frames section (wss://remotebetslip-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/quickbet/?id=66a44cc0-c33d-433e-b762-c828533ca905&EIO=3&transport=websocket)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **'name'** on market level to see market name
    PRECONDITIONS: **'name'** on outcome level to see selection name
    PRECONDITIONS: **'priceNum'** and **'priceDen'** to see current odds in fractional format
    PRECONDITIONS: **'priceDec'** to see current odds in decimal format
    """
    keep_browser_open = True

    def test_001_add_one_selection_to_quick_bet(self):
        """
        DESCRIPTION: Add one selection to Quick Bet
        EXPECTED: Quick Bet is displayed at the bottom of page
        """
        pass

    def test_002_verify_selections_details(self):
        """
        DESCRIPTION: Verify selection`s details
        EXPECTED: The following information is displayed within Quick Bet:
        EXPECTED: * selection name
        EXPECTED: * market name
        EXPECTED: * event name
        EXPECTED: * selection`s odds
        """
        pass

    def test_003_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to **'event.markets.outcomes.name'** attribute in WS response (31001)
        """
        pass

    def test_004_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: Market name corresponds to **'event.markets.name'** attribute in WS response (31001)
        """
        pass

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: Event name corresponds to **'event.name'** attribute in WS response (31001)
        """
        pass

    def test_006_verify_selections_odds(self):
        """
        DESCRIPTION: Verify selection`s odds
        EXPECTED: * Selection`s odds correspond to **'data.selectionPrice.priceNum'** and **'data.selectionPrice.priceDen'** attributes from WS response in **fraction** format (31001)
        EXPECTED: * Selection`s odds correspond **'data.selectionPrice.priceDec'** attribute from WS response in **decimal** format (31001)
        EXPECTED: *  Selection`s odds is equal to LP when **'data.selectionPrice.priceType:'LP'** attribute is received in WS response (31001)
        EXPECTED: * Selection`s odds is equal to SP when **NO**  **'data.selectionPrice** attribute is received in WS
        """
        pass
