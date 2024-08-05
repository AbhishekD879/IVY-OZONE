import tests
import time
import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create outrights events
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28524_Verify_Primary_Market_for_Football(BaseSportTest):
    """
    TR_ID: C28524
    NAME: Verify Primary Market for Football
    DESCRIPTION: This test case verifies Primary Market for 'Football' Sport
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Outright events are NOT shown on 'Today', 'Tomorrow', 'Future' tabs
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * Go to Football landing page
    """
    keep_browser_open = True
    expected_events = []
    outright_events = []

    def displayed_market_betting_events_list(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: events with name="Match Betting", dispSortName="MR"
        """
        sports_list = [item for item in sports_list]
        market_betting_list = []
        for sport in sports_list:
            try:
                if sport['event']['children'][0]['market']['name'] == 'Match Betting':
                    if sport['event']['children'][0]['market']['dispSortName'] == 'MR':
                        market_betting_list.append(sport['event']['name'])
            except KeyError:
                continue
        return market_betting_list

    def displayed_outright_events_list(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: event with name="Outright",  eventSortCode
        """
        sports_list = [item for item in sports_list]
        outright_list = []
        for sport in sports_list:
            try:
                if sport['event']['children'][0]['market']['name'] == 'Outright':
                    if sport['event']['eventSortCode'] == 'TNMT':
                        outright_list.append(sport['event']['name'])
            except KeyError:
                continue
        return outright_list

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football events
        """
        self.__class__.football_category_id = self.ob_config.backend.ti.football.category_id
        self.__class__.section_name = tests.settings.football_autotest_league
        event1 = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.market_pattern = self.ob_config.backend.ti.football.autotest_class.autotest_premier_league.market_name
        self.__class__.eventID = event1.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.autotest_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Football event "{self.autotest_event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0],
                                                                                in_play_tab_slp=True)

        self.__class__.expected_events.append(self.autotest_event_name)

        event2 = self.ob_config.add_football_event_to_special_league()
        self.__class__.expected_events.append(f'{event2.team1} v {event2.team2}')

        event3 = self.ob_config.add_football_event_to_england_premier_league()
        self.__class__.expected_events.append(f'{event3.team1} v {event3.team2}')

        event_params = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=1))
        self.__class__.expected_events.append(f'{event_params.team1} v {event_params.team2}')
        self.__class__.event_params_eventID = event_params.event_id

        event_params2 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=1), is_live=True)
        self.__class__.expected_events.append(f'{event_params2.team1} v {event_params2.team2}')

        event_params3 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=36))
        self.__class__.expected_events.append(f'{event_params3.team1} v {event_params3.team2}')

        event_params4 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        self.__class__.expected_events.append(f'{event_params4.team1} v {event_params4.team2}')

        for outright in range(0, 1):
            self.__class__.outright_name = f'Outright {int(time.time())}'
            self.ob_config.add_autotest_premier_league_football_outright_event(event_name=self.outright_name,
                                                                               start_time=self.get_date_time_formatted_string(hours=0.5), )
            self.__class__.outright_events.append(self.outright_name)

        self.__class__.ss_req_football = SiteServeRequests(env=tests.settings.backend_env,
                                                           brand=self.brand,
                                                           category_id=self.football_category_id)
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      str(self.football_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.DISP_SORT_NAME, OPERATORS.INTERSECTS, 'MR')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE))

        class_ids = self.get_class_ids_for_category(category_id=self.football_category_id)
        sports_list = self.ss_req.ss_event_to_outcome_for_class(query_builder=query,
                                                                class_id=class_ids)

        self.__class__.displayed_market_betting_event_list = \
            [item for item in self.displayed_market_betting_events_list(sports_list)]
        self.__class__.displayed_outright_event_list = \
            [item for item in self.displayed_outright_events_list(sports_list)]

    def test_001_verify_todays_matches_page_for_desktop(self):
        """
        DESCRIPTION: Verify Today's Matches page for **Desktop**
        EXPECTED: * Today's Matches page is opened
        EXPECTED: * Events are grouped by **classId** and typeId
        EXPECTED: * First **three** accordions are expanded by default
        EXPECTED: * The remaining accordions are collapsed by default
        EXPECTED: * If no events to show, the message No events found is displayed
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
        if self.device_type == 'mobile':
            football_sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(football_sections, msg='No section found on Football page')
        else:
            current_tab = self.site.contents.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                             msg=f'Default tab: "{current_tab}" opened '
                                 f'is not as expected: "{self.expected_sport_tabs.events}"')
            self.verify_section_collapse_expand()

    def test_002_verify_list_of_events__on_matches___today_tab_for_desktop__on_matches_tab_on_mobile(self):
        """
        DESCRIPTION: Verify list of events
        DESCRIPTION: - on Matches -> Today tab for **Desktop**
        DESCRIPTION: - on Matches tab on **Mobile**
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: or
        EXPECTED: *   **name="Match Result"
        EXPECTED: *   **dispSortName="MR"**
        """
        self.__class__.football_sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.football_sections, msg='No sections on Football page')
        for section_name, section in self.football_sections.items():
            if not section.is_expanded():
                section.expand()
                section = self.get_section(section_name=section_name)
            sections = section.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No events in section "{section_name}"')
            for event_name, event in sections.items():
                if not event_name.startswith("Outright"):
                    self.assertIn(event_name, self.displayed_market_betting_event_list,
                                  msg=f'Events with required attributes are not displayed {event_name} {self.displayed_market_betting_event_list}')

    def test_003_verify_priceodds_button_for_3_way_market(self):
        """
        DESCRIPTION: Verify Price/Odds button for 3-Way Market
        EXPECTED: For **Match Betting/Match Result** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home **'Win'**
        EXPECTED: *   outcomeMeaningMinorCode="D" is a **'Draw'**
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'Win'**
        """
        event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        self.assertTrue(event, msg=f'Event "{self.autotest_event_name}" not found on football page')
        actual_selections = event.template.items_as_ordered_dict.keys()
        expected_selection = self.prices.values()
        self.assertListEqual(list(actual_selections), list(expected_selection), msg=f'Price/Odds buttons are not same'
                                                                                    f'Actual: "{actual_selections}"'
                                                                                    f'Expected "{expected_selection}"')

    def test_004_tap_in_play_tab(self):
        """
        DESCRIPTION: Tap 'In-Play' tab
        EXPECTED: **'In-Play'** tab is opened
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('sport/football/live')
            in_play_module = self.site.inplay.tab_content
            self.assertTrue(in_play_module, msg='There is no "In Play" module on the page')
        if self.device_type == 'desktop':
            modules = self.cms_config.get_initial_data().get('modularContent', [])
            modules_name = [module.get('id') for module in modules]
            if self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play in modules_name:
                in_play_tab = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play)
                self.site.contents.tabs_menu.click_button(in_play_tab)
                current_tab = self.site.contents.tabs_menu.current
                self.assertEqual(current_tab, in_play_tab,
                                 msg=f'Current tab: "{current_tab}" opened is not as expected: "{in_play_tab}"')
            else:
                self._logger.warning('In-play tab isn\'t shown on Homepage')

    def test_005_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: 1) Events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: or
        EXPECTED: *   **name="Match Result"
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        #  1. Done in the scope of step 2
        football_sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(football_sections, msg='No sections on Football page')
        for section_name, section in football_sections.items():
            if not section.is_expanded():
                section.expand()
                section = self.get_section(section_name=section_name)
            sections = section.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No events in section "{section_name}"')
            for event_name, event in sections.items():
                if event_name.startswith("Outright"):
                    self.assertIn(event_name, self.displayed_outright_event_list,
                                  msg='Events with required attributes are not displayed')
