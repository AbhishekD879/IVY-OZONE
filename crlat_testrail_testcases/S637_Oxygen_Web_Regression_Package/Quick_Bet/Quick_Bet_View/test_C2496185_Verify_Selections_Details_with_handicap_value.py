import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.quick_bet
@vtest
class Test_C2496185_Verify_Selections_Details_with_handicap_value(Common):
    """
    TR_ID: C2496185
    NAME: Verify Selection`s Details with handicap value
    DESCRIPTION: This test case verifies selections details with handicap value within Quick Bet
    DESCRIPTION: AUTOTEST [C2610728]
    PRECONDITIONS: 1. Quick Bet functionality should be enabled in CMS
    PRECONDITIONS: 2. Quick Bet functionality is available for Mobile ONLY
    PRECONDITIONS: 3. To get event`s details open Dev Tools -> Networks -> WS -> '?EIO=3&transport=websocket' request -> Frames section (wss://remotebetslip-tst0.coralsports.nonprod.cloud.ladbrokescoral.com/quickbet/?id=66a44cc0-c33d-433e-b762-c828533ca905&EIO=3&transport=websocket)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: **'name'** on event level to see event name and local time
    PRECONDITIONS: **'name'** on market level to see market name
    PRECONDITIONS: **'name'** on outcome level to see selection name
    PRECONDITIONS: **'priceNum'** and 'priceDen' to see current odds in fractional format
    PRECONDITIONS: **'priceDec'** to see current odds in decimal format
    PRECONDITIONS: **SiteServe Response Example**
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForEvent/**eventID**?simpleFilter=event.suspendAtTime:greaterThan:YYYY-MM-DDTHH:MM:SS.000Z&scorecast=true&translationLang=en&responseFormat=json
    """
    keep_browser_open = True

    def test_001_add_one_selection_to_quick_bet_where_handicap_is_available(self):
        """
        DESCRIPTION: Add one selection to Quick Bet where handicap is available
        EXPECTED: - Quick Bet is displayed at the bottom of page
        """
        pass

    def test_002_verify_selections_details(self):
        """
        DESCRIPTION: Verify selection`s details
        EXPECTED: The following information is displayed within Quick Bet:
        EXPECTED: * selection name and handicap value (e.g <Selection name> (handicap value))
        EXPECTED: * market name
        EXPECTED: * event name
        EXPECTED: * selection`s odds
        """
        pass

    def test_003_verify_selection_name_and_handicap_value(self):
        """
        DESCRIPTION: Verify selection name and handicap value
        EXPECTED: - Selection name corresponds to **'event.markets.outcomes.name'** attribute in WS response (31001) **OR** Selection name corresponds to **'name'** attribute on the outcome level in SiteServe response
        EXPECTED: - Handicap value corresponds to **rawHandicapValue** attribute in WS (**'data.selectionPrice.rawHandicapValue) **OR** attribute **'handicapValueDec'** from the Site Server response to the event
        """
        pass

    def test_004_verify_sign_for_handicap_value(self):
        """
        DESCRIPTION: Verify sign for handicap value
        EXPECTED: * handicap value is displayed with **'-'** sign if **rawHandicapValue** contains nagative value in WS ( **'data.selectionPrice.rawHandicapValue** ) **OR** attribute **'handicapValueDec'** in SiteServe response
        EXPECTED: * handicap value is displayed with **'+'** sign if **rawHandicapValue** contains positive value in WS ( **'data.selectionPrice.rawHandicapValue** ) **OR** attribute **'handicapValueDec'** in SiteServe response
        EXPECTED: * handicap value is displayed with **'+'** sign if **rawHandicapValue** has no sign in WS ( **'data.selectionPrice.rawHandicapValue** ) **OR** attribute **'handicapValueDec'** in SiteServe response
        """
        pass

    def test_005_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: - Market name corresponds to **'event.markets.name'** attribute in WS response (31001) **OR** Market name corresponds to **'name'** attribute on the market level in SiteServer response
        """
        pass

    def test_006_verify_event_name(self):
        """
        DESCRIPTION: Verify event name
        EXPECTED: - Event name corresponds to **'event.name'** attribute in WS response (31001) **OR** Event name corresponds to **'name'** attribute on the event level in SiteServer response
        """
        pass

    def test_007_verify_selections_odds(self):
        """
        DESCRIPTION: Verify selection`s odds
        EXPECTED: * Selection`s odds correspond to **'data.selectionPrice.priceNum'** and **'data.selectionPrice.priceDen'** attributes in **fraction** format
        EXPECTED: * Selection`s odds correspond **'data.selectionPrice.priceDec'** attribute in **decimal** format
        EXPECTED: * Selection`s odds is equal to SP when **NO**  **'data.selectionPrice** attribute is received in WS
        """
        pass
