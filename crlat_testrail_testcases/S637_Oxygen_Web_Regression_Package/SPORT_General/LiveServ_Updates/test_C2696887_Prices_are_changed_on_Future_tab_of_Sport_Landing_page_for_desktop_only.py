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
class Test_C2696887_Prices_are_changed_on_Future_tab_of_Sport_Landing_page_for_desktop_only(Common):
    """
    TR_ID: C2696887
    NAME: Prices are changed on Future tab of <Sport> Landing page (for desktop only)
    DESCRIPTION: This test case verifies Prices changes on Future tab of <Sport> Landing page (for desktop only)
    DESCRIPTION: AUTOTEST Mobile: [C2727282]
    DESCRIPTION: AUTOTEST Desktop: [C2727283]
    PRECONDITIONS: There are <Sport> Future events
    PRECONDITIONS: LiveServer is available only for **In-Play <Sport> events** with the following attributes:
    PRECONDITIONS: *   drilldownTagNames="EVFLAG_BL"
    PRECONDITIONS: *   isMarketBetInRun = "true"
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

    def test_001_open_future_tab_of_sport_landing_page_for_desktop_only(self):
        """
        DESCRIPTION: Open Future tab of <Sport> Landing page (for desktop only)
        EXPECTED: * Future tab is selected
        EXPECTED: * Websocket connection with LiveServeMS is established
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY
        """
        pass

    def test_002_trigger_price_change_for_outcome_from_primary_market_for_one_of_events_from_the_current_page(self):
        """
        DESCRIPTION: Trigger price change for outcome from <Primary market> for one of events from the current page
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