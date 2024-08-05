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
class Test_C1053809_Verify_In_Play_widget_for_Desktop(Common):
    """
    TR_ID: C1053809
    NAME: Verify In-Play widget for Desktop
    DESCRIPTION: This test case verifies In-Play widget for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
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

    def test_001_navigate_to_sports_landing_page_that_contains_live_events(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Live events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed in 3-rd column
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Carousel with event cards are available on In-play widget
        """
        pass

    def test_002_click_on_selection_from_the_widget(self):
        """
        DESCRIPTION: Click on selection from the widget
        EXPECTED: * Selection is successfully added to Betslip
        EXPECTED: * Selection is marked as added in In Play widget
        """
        pass

    def test_003_hover_the_mouse_over_event_card(self):
        """
        DESCRIPTION: Hover the mouse over Event card
        EXPECTED: Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        pass

    def test_004_click_on_event_card_except_priceodds_buttons_in_the_widget(self):
        """
        DESCRIPTION: Click on Event card (except 'Price/Odds' buttons) in the widget
        EXPECTED: User is redirected to Event Details Page
        """
        pass

    def test_005_repeat_steps_2_4_for_live_outright_events(self):
        """
        DESCRIPTION: Repeat steps 2-4 for Live Outright events
        EXPECTED: 
        """
        pass
