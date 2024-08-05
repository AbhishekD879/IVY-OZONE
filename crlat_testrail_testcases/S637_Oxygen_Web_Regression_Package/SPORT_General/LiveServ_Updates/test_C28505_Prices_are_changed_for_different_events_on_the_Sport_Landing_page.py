import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28505_Prices_are_changed_for_different_events_on_the_Sport_Landing_page(Common):
    """
    TR_ID: C28505
    NAME: Prices are changed for different events on the <Sport> Landing page
    DESCRIPTION: This test-case verifies whether Prices are changed for different events on the <Sport> Landing page
    DESCRIPTION: Jira ticket: BMA-10941 V2 - Selection Icon Updates
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

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_tap_sport_icon_from_the_sports_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>' icon from the sports ribbon
        EXPECTED: <Sport> Landing page is opened
        """
        pass

    def test_003_open_matches_today_tab_for_desktopopen_matches_page_for_mobile(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Today**' tab (for desktop)
        DESCRIPTION: Open '**Matches**' page (for mobile)
        EXPECTED: * Websocket connection with LiveServeMS is established
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY
        """
        pass

    def test_004_trigger_price_change_for_primary_market_market_outcome_for_several_events_from_the_current_page(self):
        """
        DESCRIPTION: Trigger price change for '<Primary market>' market outcome for several events from the current page
        EXPECTED: * Updates are received in WS with **type="sSELCN"**
        EXPECTED: * Corresponding 'Price/Odds' buttons immediately display new prices and for a few seconds and they change their colors to:
        EXPECTED: - blue color if price has decreased
        EXPECTED: - red color if price has increased
        """
        pass

    def test_005_open_matches_tomorrow_tab_for_desktop_only(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Tomorrow**' tab (for desktop only)
        EXPECTED: * Websocket connection with LiveServeMS is kept pending
        EXPECTED: * Unsubscription by IDs are sent for all Today`s events
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY for Tomorrow events
        """
        pass

    def test_006_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: 
        """
        pass

    def test_007_open_matches_future_tab_for_desktop_only(self):
        """
        DESCRIPTION: Open '**Matches**'->'**Future**' tab (for desktop only)
        EXPECTED: * Websocket connection with LiveServeMS is kept pending
        EXPECTED: * Unsubscription by IDs are sent for all Tomorrow`s events
        EXPECTED: * Subscription by IDs are sent to events that are present in the expanded competitions ONLY for Future events
        """
        pass

    def test_008_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: 
        """
        pass
