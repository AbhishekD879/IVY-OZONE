import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C29392_Live_Price_Updates_for_Enhanced_Multiple_Events(Common):
    """
    TR_ID: C29392
    NAME: Live Price Updates for Enhanced Multiple Events
    DESCRIPTION: This test case verified live price updates for Enhanced Multiple events which are added to the 'Featured' tab (mobile/tablet)/ Featured section (desktop)
    DESCRIPTION: **NOTE** : Live price updates are NOT applicable to Football Enhanced Multiples Events.
    DESCRIPTION: **JIRA Ticket **: BMA-2451 'Feature tab: Live serve price updates'
    PRECONDITIONS: 1) To get into SiteServer use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ  - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXX - event ID
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) Make sure on 'Featured' tab there are a Football Enhanced Multiples Events (you need to create Featured module with "Select events" by "Enhanced Multiples" and define the |Enhanced Multiples| type Id)
    PRECONDITIONS: ![](index.php?/attachments/get/120236993)
    PRECONDITIONS: 3) To verify suspension and price changes check received data using Dev Tools-> Network -> Web Sockets -> ?module=featured&EIO=3&transport=websocket-> response with type: EVENT/EVMKT/SELCN depend on level of triggering suspension event/market/selection and response with type: PRICE when trigger price changes
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_on_the_homepage_open_featured_tab(self):
        """
        DESCRIPTION: On the Homepage open 'Featured' tab
        EXPECTED: **For mobile/tablet:**
        EXPECTED: 'Featured' tab is opened
        EXPECTED: **For desktop:**
        EXPECTED: Module Ribbon Tabs are transformed into sections, displayed in the following order:
        EXPECTED: 1) Enhanced multiples carousel
        EXPECTED: 2) In-Play & Live Stream
        EXPECTED: 3) Next Races Carousel
        EXPECTED: 4) Featured area
        """
        pass

    def test_003_trigger_price_change_for_this_outcome_for_this_event(self):
        """
        DESCRIPTION: Trigger price change for this outcome for this event
        EXPECTED: * The 'Price/Odds' button is displayed new prices immediately and it changes the color:
        EXPECTED: * blue color if a price has decreased
        EXPECTED: * pink color if a price has increased
        EXPECTED: * Updates are received in WS
        """
        pass

    def test_004_trigger_the_following_situation_for_the_eventeventstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the event:
        DESCRIPTION: **eventStatusCode='S'**
        EXPECTED: * Price/Odds buttons of this event immediately start to be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        pass

    def test_005_trigger_the_following_situation_for_the_event_primary_marketmarketstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the event primary market:
        DESCRIPTION: **marketStatusCode='S'**
        EXPECTED: * Price/Odds buttons of this market immediately start to be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        pass

    def test_006_trigger_the_following_situation_for_the_selection_from_the_eventoutcomestatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for the selection from the event:
        DESCRIPTION: **outcomeStatusCode='S'**
        EXPECTED: * Price/Odds button of this outcome immediately start to be displayed as greyed out
        EXPECTED: * Price/Odds buttons are disabled
        EXPECTED: * Updates are received in WS
        """
        pass
