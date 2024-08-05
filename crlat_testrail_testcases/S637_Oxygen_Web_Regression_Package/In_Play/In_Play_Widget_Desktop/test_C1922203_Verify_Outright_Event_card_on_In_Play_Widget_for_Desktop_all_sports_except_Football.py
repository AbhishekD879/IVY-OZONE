import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C1922203_Verify_Outright_Event_card_on_In_Play_Widget_for_Desktop_all_sports_except_Football(Common):
    """
    TR_ID: C1922203
    NAME: Verify Outright Event card on In-Play Widget for Desktop (all sports except Football)
    DESCRIPTION: This test case verifies how Live Outright events for all sports except Football are displayed on Desktop In-Play widget.
    PRECONDITIONS: * Live Outright Events are events with the following attributes:
    PRECONDITIONS: 1)   **eventSortCode="TNMT"**/"TRxx" ****(xx - numbers from 01 to 20) AND/OR ​**dispSortName **is positive (e.g. dispSortName="3W")
    PRECONDITIONS: 2)   AND **isMarketBetInRun="true" **(on the any Market level)
    PRECONDITIONS: 3)   AND **rawIsOffCode="Y"** OR (**isStated="true"** AND **rawIsOffCode="-")**
    PRECONDITIONS: 4)   AND **drilldownTagNames: "EVFLAG_BL"** (eventFlagCodes: "BL")
    PRECONDITIONS: * For checking data get from In-Play MS use the following instruction:
    PRECONDITIONS: 1. Dev Tools->Network->WS
    PRECONDITIONS: 2. Open "IN_PLAY_SPORTS::XX::LIVE_EVENT::XX" response
    PRECONDITIONS: XX - category ID
    PRECONDITIONS: 3. Look at 'eventCount' attribute for every type available in WS for appropriate category
    PRECONDITIONS: * Use the following link for checking attributes of In-Play events: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    PRECONDITIONS: isStarted="true" - means event is started
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sports_landing_page_that_contains_live_outright_events(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Live Outright events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed on the bottom of the 'Matches' tab
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Carousel with event cards are available on In-play widget
        """
        pass

    def test_003_verify_outright_event_card_displaying_on_in_play_widget(self):
        """
        DESCRIPTION: Verify Outright Event card displaying on In-Play widget
        EXPECTED: Outright Event card is displayed with following elements:
        EXPECTED: * Event card header (event class/type, 'Cash out' icon)
        EXPECTED: * Event name
        EXPECTED: * 'LIVE' label
        EXPECTED: * Selections/outcomes names
        EXPECTED: * Price/Odds buttons
        """
        pass

    def test_004_verify_outright_event_card_header(self):
        """
        DESCRIPTION: Verify Outright event card header
        EXPECTED: The title on event card header is in the following format and corresponds to the following attributes:
        EXPECTED: * 'Type Name' if section is named Category Name + Type Name on Pre-Match pages
        EXPECTED: * 'Class Name' - 'Type Name' if section is named Class Name (sports name should not be displayed) + Type Name on Pre-Match pages
        """
        pass

    def test_005_verify_cash_out_icon(self):
        """
        DESCRIPTION: Verify 'CASH OUT' icon
        EXPECTED: * 'CASH OUT' icon is shown next to the Class/Type Name
        EXPECTED: * 'CASH OUT' icon is shown 'cashoutAvail="Y" attribute is present on
        EXPECTED: Market level that is displayed in widget
        """
        pass

    def test_006_verify_outright_event_name(self):
        """
        DESCRIPTION: Verify Outright event name
        EXPECTED: * Event name corresponds to 'name' attribute on event level
        EXPECTED: * Event name is displayed in the center of event card
        EXPECTED: * Event name is truncated in case it doesn't fit on a card
        """
        pass

    def test_007_verify_live_label_displaying(self):
        """
        DESCRIPTION: Verify 'LIVE' label displaying
        EXPECTED: * 'LIVE' red label is displayed below Outright Event name
        EXPECTED: * 'LIVE' label is shown if the following attributes are present for event: rawIsOffCode="Y" OR rawIsOffCode="-" AND isStarted="true"
        """
        pass

    def test_008_verify_selectionsoutcomes(self):
        """
        DESCRIPTION: Verify Selections/outcomes
        EXPECTED: * Selections from market with 'templateMarketName=Outright' are shown
        EXPECTED: * In case of several markets with 'templateMarketName=Outright', the one with lowest display order is used; if dispOrder is the same, then alphabetically
        EXPECTED: * Selections/outcomes names correspond to 'name' attribute on outcome level
        EXPECTED: * Selections/outcomes names are truncated in case they don't fit
        """
        pass

    def test_009_verify_order_of_selectionsoutcomes(self):
        """
        DESCRIPTION: Verify order of Selections/outcomes
        EXPECTED: Selections/outcomes are ordered by:
        EXPECTED: * price in ascending order > lowest to highest
        EXPECTED: * if price is the same > by displayOrder
        EXPECTED: * if displayOrder is the same > alphabetically
        """
        pass

    def test_010_verify_displaying_of_priceodds_buttons(self):
        """
        DESCRIPTION: Verify displaying of 'Price/Odds' buttons
        EXPECTED: * 'Price/Odds' buttons are displayed below respective Selections/outcomes names
        EXPECTED: * Max 3 price/odds buttons are shown
        EXPECTED: * If only 1 price/odds button is available, it is shown fully on a card, if 2 > they occupy space evenly
        EXPECTED: * 'Price/Odds' corresponds to the 'priceNum/priceDen' if eventStatusCode="A" in fraction format
        EXPECTED: * 'Price/Odds' corresponds to the 'priceDec' if eventStatusCode="A" in decimal format
        EXPECTED: * Disabled 'Price/Odds' button is displayed with 'priceNum/priceDen' (for fractional format) or 'priceDec' (for Decimal format if eventStatusCode="S"
        """
        pass

    def test_011_navigate_to_sports_landing_page_that_contains_football_live_outright_events(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Football Live Outright events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed on the bottom of the 'Matches' tab
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Carousel with event cards are available on In-play widget
        """
        pass

    def test_012_verify_football_outright_event_card_displaying_on_in_play_widget(self):
        """
        DESCRIPTION: Verify Football Outright Event card displaying on In-Play widget
        EXPECTED: Outright Event card is displayed with following elements:
        EXPECTED: * Event card header (event class/type, 'Cash out' icon)
        EXPECTED: * Event name
        EXPECTED: * 'LIVE' label
        EXPECTED: * Selections/outcomes names are NOT displayed
        EXPECTED: * Price/Odds buttons are NOT displayed
        """
        pass
