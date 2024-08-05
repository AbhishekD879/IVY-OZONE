import pytest
import tests
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.base_test import vtest


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.in_play
@pytest.mark.desktop_only
@pytest.mark.adhoc_suite
@vtest
# this test case covers C65946737,C65946738
class Test_C1045461_Event_card_layout_on_In_Play_Widget_for_Desktop(BaseSportTest):
    """
    TR_ID: C1045461
    NAME: Event card layout on In-Play Widget for Desktop
    DESCRIPTION: This test case verifies Event card layout on In-Play Widget for Desktop.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: Oxygen app is loaded
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) For checking data get from In-Play MS use the following instruction:
    PRECONDITIONS: * Dev Tools->Network->WS
    PRECONDITIONS: * Open "IN_PLAY_SPORTS::XX::LIVE_EVENT::XX" response
    PRECONDITIONS: XX - category ID
    PRECONDITIONS: 2) Look at 'eventCount' attribute for every type available in WS for the appropriate category
    PRECONDITIONS: 3) Use the following link for checking attributes of In-Play events: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: * drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    PRECONDITIONS: * isStarted="true" - means event is started
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get live events
        """
        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(in_play_event=True, raise_exceptions=False)
            self.__class__.sport_name = "football"
            if not events:
                self.get_active_events_for_category(in_play_event=True, category_id=34)
                self.__class__.sport_name = "tennis"
        else:
            self.ob_config.add_autotest_premier_league_football_event(is_live=True)
            self.__class__.sport_name = "football"

        in_play_status = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle').get('inPlay')
        live_stream_status = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle').get("liveStream")
        if not in_play_status:
            self.cms_config.update_system_configuration_structure(config_item='DesktopWidgetsToggle',
                                                                  field_name='inPlay', field_value=True)
        if not live_stream_status:
            self.cms_config.update_system_configuration_structure(config_item='DesktopWidgetsToggle',
                                                                  field_name='liveStream', field_value=True)

    def test_001_navigate_to_sports_landing_page_that_contains_live_events(self):
        """
        DESCRIPTION: Navigate to Sports Landing page that contains Live events
        EXPECTED: * Sports Landing page is opened
        EXPECTED: * In-Play widget is displayed in 3-rd column
        EXPECTED: * In-Play widget is expanded by default
        EXPECTED: * Carousel with event cards are available on In-play widget
        """
        self.navigate_to_page(name=f'sport/{self.sport_name}')
        self.site.wait_content_state(state_name=self.sport_name)

    def test_002_verify_event_card_displaying_on_in_play_widget(self):
        """
        DESCRIPTION: Verify Event card displaying on In-Play widget
        EXPECTED: Event card is displayed with following elements:
        EXPECTED: * Event card header
        EXPECTED: * Event card body
        EXPECTED: * Fixture header
        EXPECTED: * Price/Odds' buttons
        """
        sections = self.site.sports_page.in_play_widget.items_as_ordered_dict.get('In-Play LIVE '+self.sport_name.title())
        self.__class__.widgets = sections.content.items_as_ordered_dict
        sections.is_expanded()
        self.assertTrue(self.widgets, msg='Widget are not available')
        self.__class__.event_name, self.__class__.event = list(self.widgets.items())[-1]
        self.assertTrue(self.event.is_displayed(), msg=f'Widget {self.event_name} is not displayed')
        event_header = (list(sections.content.items_as_ordered_dict.items())[0][1]).fixture_header
        self.assertTrue(event_header.is_displayed(), msg=f'Widget {event_header} is not displayed')

    def test_003_verify_title_on_event_card_header_within_carousel(self):
        """
        DESCRIPTION: Verify title on event card header within carousel
        EXPECTED: The title on event card header is in the following format and corresponds to the following attributes:
        EXPECTED: * 'Type Name' if section is named Category Name + Type Name on Pre-Match pages
        EXPECTED: * 'Class Name' - 'Type Name' if section is named Class Name (sports name should not be displayed) + Type Name on Pre-Match pages
        EXPECTED: 'CASH OUT' label is shown next to the Type Name if available (on Type level)
        """
        cashout = self.event.cashout_inplay_icon
        self.assertTrue(cashout, msg=f'Widget {cashout} is not displayed')

    def test_004_verify_event_name_displaying_on_event_card_body(self):
        """
        DESCRIPTION: Verify event name displaying on Event card body
        EXPECTED: * Event name corresponds to 'name' attribute
        EXPECTED: Event name and is displayed in format: <Team1/Player1> and <Team2/Player2> below
        EXPECTED: * Event name is displayed at the center of event card
        """
        event_header = self.event_name
        self.assertTrue(event_header, msg=f'Widget {event_header} is not displayed')

    def test_005_verify_scores_and_live_label_displaying_on_event_card_body(self):
        """
        DESCRIPTION: Verify Scores and 'Live' label displaying on Event card body
        EXPECTED: * 'LIVE'/'Time'/'Set'> red badge is displayed below the Event name and between Scores
        EXPECTED: * Scores are displayed in one row for 'Home' and 'Away' team/player respectively
        EXPECTED: * Tennis Scores from all sets are displayed in one row but scores from previous sets have grey color and less font-size
        """
        score = self.event.in_play_card.in_play_score
        self.assertTrue(score.is_displayed(), msg=f'Widget {score} is not displayed')

    def test_006_verify_more_markets_link_displaying_on_event_card_body(self):
        """
        DESCRIPTION: Verify 'More markets' link displaying on Event card body
        EXPECTED: * 'More Markets' link is displayed below 'Live/Time/Set' badge and scores
        EXPECTED: * Digits are underlined within link when hovering the mouse on it
        EXPECTED: * 'More Markets' link is NOT displayed if there are no additional markets
        EXPECTED: * User is redirected to the EDP page when clicking on link
        """
        markets = self.event.in_play_card.more_markets_link_inplay
        self.assertTrue(markets, msg=f'Widget {markets} is not displayed')
        markets.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_007_verify_watch_live_icon(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon
        EXPECTED: * 'Watch Live' icon is shown on the right side at the top of Event card body if ‘drilldownTagNames’ attribute is available (one of following flags):
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: * 'Watch Live' icon is NOT shown when 'drilldownTagNames' attribute has more than one flag from the list above
        EXPECTED: * User is redirected to the EDP page when clicking on icon
        """
        self.navigate_to_page(name=f'sport/{self.sport_name}')
        self.site.wait_content_state(state_name=self.sport_name)
        sections = self.site.sports_page.in_play_widget.items_as_ordered_dict.get('In-Play LIVE '+self.sport_name.title())
        self.widgets = sections.content.items_as_ordered_dict
        self.event_name, self.event = list(self.widgets.items())[-1]
        live_icon = self.event.in_play_card.live_icon
        self.assertTrue(live_icon.is_displayed(), msg=f'Widget "{live_icon}" is not displayed')
        live_icon.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_008_verify_favorite_icon_for_football_only(self):
        """
        DESCRIPTION: Verify 'Favorite' icon (For Football only)
        EXPECTED: * 'Favorite' (Star) icon is shown on the left side at the top of Event card body
        EXPECTED: *  'Favorite' (Star) icon filled with yellow color after clicking on it
        """
        self.navigate_to_page(name=f'sport/{self.sport_name}')
        self.site.wait_content_state(state_name=self.sport_name)
        sections = self.site.sports_page.in_play_widget.items_as_ordered_dict.get(
            'In-Play LIVE ' + self.sport_name.title())
        self.__class__.widgets = sections.content.items_as_ordered_dict
        self.__class__.event_name, self.__class__.event = list(self.widgets.items())[-1]
        if self.brand == 'bma' and self.sport_name == 'football':
            favourite_icon = self.event.in_play_card.favourites_icon
            self.assertTrue(favourite_icon.is_displayed(),
                            msg=f'Favorite icon is not displayed for event: "{self.event_name}"')

    def test_009_verify_displaying_of_fixture_header(self):
        """
        DESCRIPTION: Verify displaying of Fixture header
        EXPECTED: * Name of Market is displayed between Event card body and Fixture header
        EXPECTED: * Fixture header is shown with 'Home'/'Draw'/'Away' options if events in the section have 3-way Primary Market being shown
        EXPECTED: * Fixture header is shown with '1'/'2' options if events in the section have 2-way Primary Market being shown
        """
        header = self.event.fixture_header
        self.assertTrue(header, msg=f'Fixture {header} is not displayed')

    def test_010_verify_displaying_of_priceodds_buttons(self):
        """
        DESCRIPTION: Verify displaying of 'Price/Odds' buttons
        EXPECTED: * 'Price/Odds' buttons are displayed below Fixture header in one row
        EXPECTED: * 'Price/Odds' corresponds to the 'priceNum/priceDen' if eventStatusCode="A" in fraction format
        EXPECTED: * 'Price/Odds' corresponds to the 'priceDec' if eventStatusCode="A" in decimal format
        EXPECTED: * Disabled 'Price/Odds' button is displayed with 'priceNum/priceDen' (for fractional format) or 'priceDec' (for Decimal format if eventStatusCode="S"
        EXPECTED: * 'Price/Odds' buttons are ordered by the rule for 2-Way Market bellow respective option from Fixture header:
        EXPECTED: * outcomeMeaningMinorCode="H" is a Home
        EXPECTED: * outcomeMeaningMinorCode="A" is an Away
        EXPECTED: * 'Price/Odds' buttons are ordered by the rule for 3-Way Market bellow respective option from Fixture header:
        EXPECTED: * outcomeMeaningMinorCode="H" is a Home
        EXPECTED: * outcomeMeaningMinorCode="D" is a Draw
        EXPECTED: * outcomeMeaningMinorCode="A" is an Away
        """
        odds_buttons = self.event.odds_buttons
        self.assertTrue(odds_buttons, msg=f'"{odds_buttons}" are not displayed')
