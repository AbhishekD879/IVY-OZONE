import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726395_Event_hub_Live_Price_Updates_for_Enhanced_Multiple_Events(Common):
    """
    TR_ID: C9726395
    NAME: Event hub: Live Price Updates for Enhanced Multiple Events
    DESCRIPTION: This test case verified live price updates for Enhanced Multiple events which are added to the 'Event Hub' tab (mobile/tablet)
    DESCRIPTION: **NOTE** : Live price updates are NOT applicable to Football Enhanced Multiples Events.
    PRECONDITIONS: 1) To get into SiteServer use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Make sure on 'Event Hub' tab there are a Football Enhanced Multiples Events
    PRECONDITIONS: 3) To verify suspension and price changes check received data using Dev Tools-> Network -> Web Sockets -> ?module=featured&EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCN depend on level of triggering suspension event/market/selection and response with type: PRICE when trigger price changes
    PRECONDITIONS: 4) User is on Event hub tab
    """
    keep_browser_open = True

    def test_001_trigger_price_change_for_this_outcome_for_this_event(self):
        """
        DESCRIPTION: Trigger price change for this outcome for this event
        EXPECTED: * The 'Price/Odds' button is displayed new prices immediately and it changes the color:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        EXPECTED: * Updates are received in WS
        """
        pass

    def test_002_trigger_the_following_situation_for_the_eventeventstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the event:
        DESCRIPTION: **eventStatusCode='S'**
        EXPECTED: * Price/Odds buttons of this event immediately start to be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        pass

    def test_003_trigger_the_following_situation_for_the_event_primary_marketmarketstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the event primary market:
        DESCRIPTION: **marketStatusCode='S'**
        EXPECTED: * Price/Odds buttons of this market immediately start to be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        pass

    def test_004_trigger_the_following_situation_for_the_selection_from_the_eventoutcomestatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the selection from the event:
        DESCRIPTION: **outcomeStatusCode='S'**
        EXPECTED: * Price/Odds button of this outcome immediately start to be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        pass
