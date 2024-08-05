import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
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
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get live events
        """
        if tests.settings.backend_env == 'prod':
            self.get_active_events_for_category(in_play_event=True)
        else:
            self.ob_config.add_autotest_premier_league_football_event(is_live=True)

    def test_001_navigate_to_sports_landing_page_that_contains_live_events(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Live events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Carousel with event cards are available on In-play widget
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state('FOOTBALL')
        section = self.site.football.in_play_widget.items_as_ordered_dict.get('In-Play LIVE Football')
        self.assertTrue(section, msg='"In-Play" widget not found on SLP')
        self.assertTrue(section.is_expanded(), msg='"In-Play" widget is not expanded by default')
        self.__class__.events = section.content.items_as_ordered_dict
        self.assertTrue(self.events, msg='events are not displayed')

    def test_002_click_on_selection_from_the_widget(self):
        """
        DESCRIPTION: Click on selection from the widget
        EXPECTED: * Selection is successfully added to Betslip
        EXPECTED: * Selection is marked as added in In Play widget
        """
        self.__class__.event1 = list(self.events.values())[0]
        selections = self.event1.odds_buttons.items_as_ordered_dict
        selection = list(selections.values())[0]
        selection.click()
        self.assertTrue(selection.is_selected(), msg='selection is not marked as added to betslip')

    def test_003_hover_the_mouse_over_event_card(self):
        """
        DESCRIPTION: Hover the mouse over Event card
        EXPECTED: Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility to click on particular area
        """
        # cannot automate this step

    def test_004_click_on_event_card_except_priceodds_buttons_in_the_widget(self):
        """
        DESCRIPTION: Click on Event card (except 'Price/Odds' buttons) in the widget
        EXPECTED: User is redirected to Event Details Page
        """
        self.event1.in_play_card.click()
        self.site.wait_content_state('EventDetails', timeout=20)
