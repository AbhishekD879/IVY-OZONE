import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28501_Prices_are_changed_on_Sport_Landing_page(Common):
    """
    TR_ID: C28501
    NAME: Prices are changed on <Sport> Landing page
    DESCRIPTION: This test case verifies Prices changes on Today tab of <Sport> Landing page
    DESCRIPTION: AUTOTEST Desktop: [C2709099]
    DESCRIPTION: AUTOTEST Mobile: [C2696912]
    PRECONDITIONS: There are <Sport> Today's events
    PRECONDITIONS: Events should have the following attributes:
    PRECONDITIONS: *   drilldownTagNames="EVFLAG_BL" - Bet in Play List check in TI on the event level
    PRECONDITIONS: *   isMarketBetInRun = "true" - Bet In Run check in TI on the market level
    PRECONDITIONS: To check updates open Dev Tools -> Network tab -> WS option
    PRECONDITIONS: Endpoints to LiveServ MS:
    PRECONDITIONS: Coral:
    PRECONDITIONS: * wss://liveserve-publisher-prd0.ladbrokesoxygen.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - PROD
    PRECONDITIONS: * wss://liveserve-publisher-dev0.coralsports.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - DEV0
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: * wss://liveserve-publisher-prd0.coralsports.prod.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - PROD
    PRECONDITIONS: * wss://liveserve-publisher-dev0.ladbrokesoxygen.dev.cloud.ladbrokescoral.com/websocket/?EIO=3&transport=websocket - DEV0
    """
    keep_browser_open = True

    def test_001_open_sport_landing_pagedesktop___tap_today_tab(self):
        """
        DESCRIPTION: Open <Sport> Landing page
        DESCRIPTION: *Desktop* - tap TODAY tab
        EXPECTED: * Sport landing page is opened
        EXPECTED: * *Desktop* TODAY tab is opened
        EXPECTED: * Websocket connection with LiveServeMS is established
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY
        """
        pass

    def test_002_trigger_price_change_for_the_outcome_from_primary_market_for_one_of_the_events_from_the_current_page(self):
        """
        DESCRIPTION: Trigger price change for the outcome from <Primary market> for one of the events from the current page
        EXPECTED: * Update is received in WS with **type="sSELCN"**
        EXPECTED: * Corresponding 'Price/Odds' button immediately displays new price and for a few seconds it changes its colour to:
        EXPECTED: - blue colour if price has decreased
        EXPECTED: - pink colour if price has increased
        EXPECTED: **Note: colours flashing is not automated**
        """
        pass

    def test_003_collapse_competition_and_trigger_price_change_for_the_outcome_within_it(self):
        """
        DESCRIPTION: Collapse competition and trigger price change for the outcome within it
        EXPECTED: * Unsubscription by IDs are sent to events that are present in collapsed competitions ONLY
        EXPECTED: * Price change update is NOT received in WS
        """
        pass

    def test_004_expand_competition_and_verify_prices_changes(self):
        """
        DESCRIPTION: Expand competition and verify prices changes
        EXPECTED: * Subscription by IDs are sent again to event in the expanded competition
        EXPECTED: * Price change update is received in WS
        EXPECTED: * Corresponding 'Price/Odds' button immediately displays new price
        """
        pass
