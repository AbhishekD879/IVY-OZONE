import pytest
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from voltron.utils.helpers import normalize_name, get_in_play_module_from_ws
from faker import Faker
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.football
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.safari
@vtest
class Test_C28473_Verify_Sport_In_Play_Event_Details_Page(BaseSportTest):
    """
    TR_ID: C28473
    NAME: Verify <Sport> In-Play Event Details Page
    """
    keep_browser_open = True
    event_name = None
    fake = Faker()

    team1 = f'Auto test team one {fake.text(38)}'
    team2 = f'Auto test team two {fake.text(38)}'
    draw = 'Draw'
    widget_section_name = 'In-Play LIVE Football'

    def get_accordion_name_for_market_from_ss(self, ss_market_name):
        key = ss_market_name.replace(' ', '_').lower()
        accordion_name = next((getattr(self.expected_market_sections, name) for name in self.expected_market_sections._fields if name == key), '')
        return accordion_name

    def get_league_on_in_play_tab(self):
        league_name = self.league_name_in_play_tab_slp
        expected_sport_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.in_play,
                                                     self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(expected_sport_tab)
        self.site.wait_content_state(state_name='Football')
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'No sections found on "In-Play" section')
        test_league = sections.get(league_name)
        self.assertTrue(test_league, msg=f'"{league_name}" section not found on Football In Play page')
        return test_league

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(is_live=True,
                                                                                 perform_stream=True,
                                                                                 team1=self.team1,
                                                                                 team2=self.team2)
        self.__class__.eventID = event_params.event_id
        self.__class__.event_name = (event_params.team1.strip() + ' v ' + event_params.team2.strip())
        self.__class__.event_time = event_params.event_date_time
        self.__class__.team1, self.__class__.team2 = event_params.team1.strip(), event_params.team2.strip()

        event = self.ss_req.ss_event_to_outcome_for_event(event_id=event_params.event_id,
                                                          query_builder=self.ss_query_builder)

        self.__class__.league_name_in_play_tab_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                               in_play_tab_slp=True)
        self.__class__.league_name_in_play_module_slp = self.get_accordion_name_for_event_from_ss(event=event[0],
                                                                                                  in_play_module_slp=True)

        self.__class__.is_scoreboard_sport = self.get_scoreboard_sport_status(sport_id=self.ob_config.backend.ti.football.category_id)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='HomePage')

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing Page
        EXPECTED: <Sport> Landing Page is opened
        """
        self.site.open_sport(name='FOOTBALL')

    def test_003_click_tap_on_event_name_in_the_event_card(self):
        """
        DESCRIPTION: Click/Tap on Event name in the event card
        EXPECTED: <Sport> Event Details page is opened
        """
        if self.device_type == 'desktop':
            sections = self.site.football.in_play_widget.items_as_ordered_dict
            self.assertTrue(sections, msg='No sections found on Football page')
            self.assertIn(self.widget_section_name, sections.keys(),
                          msg=f'{self.widget_section_name} not found in {sections.keys()}')
            section = sections[self.widget_section_name]
            events = section.content.items_as_ordered_dict
        else:
            league_name = self.league_name_in_play_module_slp
            resp = get_in_play_module_from_ws(delimiter='42/16,')
            if not resp:
                is_in_module = False
                test_league = self.get_league_on_in_play_tab()
            else:
                inplay_module_items = self.site.football.tab_content.in_play_module.items_as_ordered_dict
                self.assertTrue(inplay_module_items, msg='Can not find any module items')
                test_league = inplay_module_items.get(league_name)
                is_in_module = True
                if not test_league:
                    is_in_module = False
                    test_league = self.get_league_on_in_play_tab()
                self.assertTrue(test_league, msg=f'Can not find league "{league_name}" in {inplay_module_items.keys()}')
            if not is_in_module:
                test_league.expand()
            events = test_league.items_as_ordered_dict
        self.assertTrue(events, msg='No event cards found on Football page')

        if self.event_name not in events.keys():
            _, event = list(events.items())[0]
        else:
            event = events[self.event_name]
        event.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_004_verify_back_button(self):
        """
        DESCRIPTION: Verify 'Back' button
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: 'Back' button is displayed on the top of Event Details Page near label
        EXPECTED: **For desktop view:**
        EXPECTED: 'Back' button is displayed on the top of Event Details Page, on the left side from Event name
        """
        current_url = self.device.get_current_url()
        if self.eventID not in current_url:
            self.navigate_to_edp(event_id=self.eventID, sport_name='football')
            self.site.wait_content_state(state_name='EventDetails')
        self.__class__.event_details_page = self.site.sport_event_details
        has_back_btn = self.site.has_back_button
        self.assertTrue(has_back_btn, msg='Event details page doesn\'t have back button')

    def test_005_verify_event_name(self):
        """
        DESCRIPTION: Verify Event name
        EXPECTED: *   Event name corresponds to '**name**' attribute
        EXPECTED: *   Event name matches with event name on the event section we navigated from
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed below the 'Back' button
        EXPECTED: **For desktop view:**
        EXPECTED: * It is displayed in the same line as 'Back' button, next to it
        EXPECTED: * Long names are truncated
        """
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                                              query_builder=self.ss_query_builder)
        event_name_details_page = self.event_details_page.event_title_bar.event_name
        if self.device_type == 'desktop':
            event_name_resp = normalize_name(self.event_resp[0]['event']['name']).upper()\
                if not self.brand == 'ladbrokes' else normalize_name(self.event_resp[0]['event']['name']).title()
            event_name_ui = self.event_name.upper() if not self.brand == 'ladbrokes' else self.event_name.title()
            self.assertEqual(event_name_details_page, event_name_ui,
                             msg=f'Event name "{event_name_details_page}" on details page doesn\'t match with '
                             f'event name "{event_name_ui}" on Football page')
        else:
            event_name_resp = normalize_name(self.event_resp[0]['event']['name'])
            self.assertEqual(event_name_details_page, self.event_name,
                             msg=f'Event name "{event_name_details_page}" on details page doesn\'t match with '
                             f'event name "{self.event_name}" on Football page')
        self.assertEqual(event_name_details_page, event_name_resp,
                         msg=f'Event name "{event_name_details_page}" doesn\'t corresponds to "**name**"" '
                         f'attribute "{event_name_resp}"')

    def test_006_verify_event_start_datetime(self):
        """
        DESCRIPTION: Verify Event start date/time
        EXPECTED: *   Event start date corresponds to **startTime** attribute
        EXPECTED: *   Event start time is shown in "<name of the day>, DD-MMM-YY. 24 hours HH:MM," format (e.g. "14:00 or 05:00)
        EXPECTED: *   Event start date/time matches with date/time on the event section we navigated from
        EXPECTED: *   Match time is shown instead of Event Start Time if available
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed below the event name
        EXPECTED: **For desktop view:**
        EXPECTED: It is displayed in the same line as Event name, on the right side
        """
        event_time_ui = self.event_details_page.event_title_bar.event_time  # ladbrokes mobile specific
        event_time_resp = self.event_resp[0]['event']['startTime']
        if not self.brand == 'ladbrokes':
            ui_format_pattern = '%A, %-d-%b-%y. %H:%M' if \
                self.device_type == 'desktop' or not self.is_scoreboard_sport \
                else '%H:%M - %d/%m/%y'
        else:
            ui_format_pattern = '%A, %-d-%b-%y, %-I:%M %p' if \
                self.device_type == 'desktop' or not self.is_scoreboard_sport \
                else '%H:%M, %-d %b'

        event_time_resp_converted = self.convert_time_to_local(ob_format_pattern=self.ob_format_pattern,
                                                               date_time_str=event_time_resp,
                                                               ui_format_pattern=ui_format_pattern,
                                                               ss_data=True
                                                               )
        self.assertEqual(event_time_ui, event_time_resp_converted,
                         msg=f'Event time on UI "{event_time_ui}" is not the same as got '
                         f'from response "{event_time_resp_converted}"')

    def test_007_verify_live_label_or_score(self):
        """
        DESCRIPTION: Verify 'LIVE' label or Score
        EXPECTED: 'LIVE'/Score is displayed if event is live now:
        EXPECTED: 1.  rawIsOffCode="Y"
        EXPECTED: 2.  rawIsOffCode="-" AND isStarted="true"
        EXPECTED: **For mobile/tablet view:**
        EXPECTED: It is displayed next to the Event Start Time
        EXPECTED: **For desktop view:**
        EXPECTED: It is displayed before Event Start Time
        """
        self.assertTrue(self.event_details_page.event_title_bar.is_live_now_event, msg='No "LIVE" label on the event\'s page')
        if not self.brand == 'ladbrokes':
            live_now_icon_location = self.event_details_page.event_title_bar.live_now_icon.location.get('x')
            event_time_icon_location = self.event_details_page.event_title_bar.event_time_icon.location.get('x')
            if self.device_type == 'mobile' and not self.is_scoreboard_sport:
                self.assertTrue(live_now_icon_location > event_time_icon_location,
                                msg='"LIVE" label is not displayed after Event Start Time')
            else:
                self.assertTrue(live_now_icon_location < event_time_icon_location,
                                msg='"LIVE" label is not displayed before Event Start Time')
        else:
            if self.device_type == 'mobile':
                self.assertRegexpMatches(self.event_details_page.event_title_bar.event_time,
                                         r'^\d+:\d+, \d+ \w+',
                                         msg='Live/time format does not match expected')

    def test_008_verify_watch_live_icon_and_label(self):
        """
        DESCRIPTION: Verify 'Watch Live' icon and label
        EXPECTED: 'Watch Live' icon and label are shown if drilldownTagNames attribute is available and contains one or more of following flags:
        EXPECTED: EVFLAG_AVA
        EXPECTED: EVFLAG_IVM
        EXPECTED: EVFLAG_PVM
        EXPECTED: EVFLAG_RVA
        EXPECTED: EVFLAG_RPM
        EXPECTED: EVFLAG_GVM
        EXPECTED: EVFLAG_BL
        """
        if self.device_type == 'desktop':
            self.assertTrue(self.event_details_page.has_watch_live_button(),
                            msg='No "Watch Live" label on the event\'s page')
        else:
            if not self.is_scoreboard_sport:
                event_user_tabs = self.event_details_page.event_user_tabs_list.items_as_ordered_dict
                self.assertTrue(event_user_tabs, msg='User Tabs are not found')
                self.assertIn(vec.sb.WATCH_LIVE_LABEL.title(), event_user_tabs.keys())
            else:
                self.assertTrue(self.event_details_page.has_watch_live_icon,
                                msg='No "Watch Live" label on the event\'s page')
        self.assertTrue(self.event_details_page.event_title_bar.is_live_now_event,
                        msg='No "Watch Live" icon on the event\'s page')

    def test_009_verify_market_tabs(self):
        """
        DESCRIPTION: Verify Market tabs
        EXPECTED: * They are displayed below the event details
        EXPECTED: * It is possible to navigate between all market tabs
        EXPECTED: * Order of market tabs is the same as in EDP-Markets response from CMS
        EXPECTED: * Collection with 'lastItem: true' is displayed the last one
        EXPECTED: * In case some collection is not added in CMS it is displayed before collection with 'lastItem: true' value
        EXPECTED: * In case there are several not added to CMS collections they are displayed before collection with 'lastItem: true' value, displayed in the order they are received
        """
        markets_tabs = self.event_details_page.markets_tabs_list.items_as_ordered_dict

        for tab in markets_tabs.keys():
            self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=tab)
            self.assertEqual(tab, self.site.sport_event_details.markets_tabs_list.current,
                             msg=f'"{tab}" tab is not opened')
        tab_name = self.expected_market_tabs.all_markets

        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=tab_name)

        self.verify_edp_market_tabs_order(edp_market_tabs=markets_tabs.keys())

    def test_010_verify_markets_filtering_within_in_play_event_details_page_for_all_available_collections_on_event_details_page(
            self):
        """
        DESCRIPTION: Verify Markets filtering within In-Play Event Details Page for all available Collections on Event Details Page
        EXPECTED: Only Markets with attribute **isMarketBetInRun="true"** on the market level are displayed
        """
        markets = self.event_resp[0]['event']['children'] if 'event' in self.event_resp[0] and 'children' in \
                                                             self.event_resp[0]['event'] else []
        market = markets[0]['market']
        self.assertIn(ATTRIBUTES.IS_MARKET_BET_IN_RUN, market.keys(),
                      msg=f'There\'s no property "{ATTRIBUTES.IS_MARKET_BET_IN_RUN}" in SS response. '
                      f'See all available properties: {market.keys()}')
        self.assertEquals(market[ATTRIBUTES.IS_MARKET_BET_IN_RUN], 'true',
                          msg=f'Incorrect value for "{ATTRIBUTES.IS_MARKET_BET_IN_RUN}" in SS response.\nActual: '
                          f'"{market[ATTRIBUTES.IS_MARKET_BET_IN_RUN]}"\nExpected: "true"')

    def test_011_verify_long_names_of_selections_for_markets_which_have_list_view_of_selections(self):
        """
        DESCRIPTION: Verify long names of selections for Markets, which have list view of selections
        EXPECTED: * Long names of selections are NOT TRUNCATED
        EXPECTED: * Long names of selections are wrapped into lines
        """
        markets = self.event_details_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No events found on Football page')

        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
        expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

        market = markets.get(expected_market_name)
        self.assertTrue(market, msg=f'Could not find market "{vec.siteserve.EXPECTED_MARKETS_NAMES.match_result}" in "{markets.keys()}"')
        selections = market.outcomes.items_as_ordered_dict
        self.assertTrue(selections, msg='No selections found')

        for selection_name, selection in selections.items():
            actual_selection_name = selection.outcome_name.upper() if self.brand == 'ladbrokes' else selection.outcome_name
            expected_result = [self.team1.upper(), self.team2.upper(), self.draw.upper()] if self.brand == 'ladbrokes' \
                else [self.team1, self.team2, self.draw]
            self.assertIn(actual_selection_name, expected_result,
                          msg=f'Selection name: "{actual_selection_name}" is not '
                          f'present in : "{expected_result}"')
            self.assertFalse(selection.is_truncated(),
                             msg=f'Selection name "{selection_name}" is truncated')
