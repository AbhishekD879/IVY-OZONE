import time

import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter, SiteServeRequests

import tests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.helpers import normalize_name


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.hockey
@vtest
class Test_C28675_Verify_Primary_Market_for_Hockey(BaseSportTest):
    """
    TR_ID: C28675
    NAME: Verify Primary Market for Hockey
    DESCRIPTION: This test case verifies Primary Market for 'Hockey' Sport.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note:** Outright events are NOT shown on 'Today', 'Tomorrow', 'Future' tabs (for desktop) and 'Matches' tab for mobile
    PRECONDITIONS: * Load Oxygen app
    """
    keep_browser_open = True
    expected_events = []
    outright_events = []
    prices = {0: '1/2', 1: '6/4', 2: '4/1'}

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
        DESCRIPTION: Create Hockey event
        """
        self.__class__.hockey_category_id = self.ob_config.backend.ti.hockey.category_id
        self.check_sport_configured(self.hockey_category_id)
        self.__class__.section_name = tests.settings.hockey_all_hockey
        event1 = self.ob_config.add_hockey_event_to_womens_olympics(lp_prices=self.prices)
        self.__class__.market_pattern = self.ob_config.backend.ti.hockey.hockey_all_hockey.womens_olympics.name_pattern
        self.__class__.eventID = event1.event_id
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        self.__class__.womens_olympics_event_name = normalize_name(event_resp[0]['event']['name'])
        self._logger.info(f'*** Created Hockey event "{self.womens_olympics_event_name}"')

        self.__class__.section_name = self.get_accordion_name_for_event_from_ss(event=event_resp[0], in_play_tab_slp=True)

        self.__class__.expected_events.append(self.womens_olympics_event_name)

        event2 = self.ob_config.add_hockey_event_to_olympics_specials()
        self.__class__.expected_events.append(f'{event2.team1} v {event2.team2}')

        event3 = self.ob_config.add_hockey_event_to_mens_olympics()
        self.__class__.expected_events.append(f'{event3.team1} v {event3.team2}')

        event_params = self.ob_config.add_hockey_event_to_super_league(
            start_time=self.get_date_time_formatted_string(hours=1), lp_prices=self.prices)
        self.__class__.expected_events.append(f'{event_params.team1} v {event_params.team2}')
        self.__class__.event_params_eventID = event_params.event_id

        event_params2 = self.ob_config.add_hockey_event_to_super_league(
            start_time=self.get_date_time_formatted_string(hours=1), is_live=True)
        self.__class__.expected_events.append(f'{event_params2.team1} v {event_params2.team2}')

        event_params3 = self.ob_config.add_hockey_event_to_super_league(
            start_time=self.get_date_time_formatted_string(hours=36))
        self.__class__.expected_events.append(f'{event_params3.team1} v {event_params3.team2}')

        event_params4 = self.ob_config.add_hockey_event_to_super_league(is_live=True)
        self.__class__.expected_events.append(f'{event_params4.team1} v {event_params4.team2}')

        for outright in range(0, 1):
            self.__class__.outright_name = f'Outright {int(time.time())}'
            self.ob_config.add_hockey_event_outright_event(event_name=self.outright_name,
                                                           start_time=self.get_date_time_formatted_string(hours=0.5),)
            self.__class__.outright_events.append(self.outright_name)

        self.__class__.ss_req_hockey = SiteServeRequests(env=tests.settings.backend_env,
                                                         brand=self.brand,
                                                         category_id=self.hockey_category_id)
        query = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      str(self.hockey_category_id))) \
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE))

        class_ids = self.get_class_ids_for_category(category_id=self.hockey_category_id)
        sports_list = self.ss_req.ss_event_to_outcome_for_class(query_builder=query,
                                                                class_id=class_ids)

        self.__class__.displayed_market_betting_event_list = \
            [item for item in self.displayed_market_betting_events_list(sports_list)]
        self.__class__.displayed_outright_event_list = \
            [item for item in self.displayed_outright_events_list(sports_list)]

    def test_001_taphockey_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Hockey' icon on the Sports Menu Ribbon
        EXPECTED: Desktop:
        EXPECTED: * Hockey Landing Page is opened
        EXPECTED: * '**Events**' tab is opened by default
        EXPECTED: * First **three **sections are expanded by default
        EXPECTED: * The remaining sections are collapsed by default
        EXPECTED: * It is possible to collapse/expand all of the sections by clicking the section's header
        EXPECTED: Mobile:
        EXPECTED: * Hockey Landing Page (single view) is opened
        EXPECTED: * All available events for this sport are displayed on 1 page
        EXPECTED: * Available modules (in-play/upcoming) and sections (outrights/specials) are displayed one below another
        """
        self.navigate_to_page(name='sport/hockey')
        self.site.wait_content_state('Hockey')
        if self.device_type == 'mobile':
            hockey_sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(hockey_sections, msg='No section found on Hockey page')
        else:
            current_tab = self.site.contents.tabs_menu.current
            self.assertEqual(current_tab, self.expected_sport_tabs.matches,
                             msg=f'Default tab: "{current_tab}" opened '
                                 f'is not as expected: "{self.expected_sport_tabs.events}"')
            self.verify_section_collapse_expand()

    def test_002_verify_list_of_events(self):
        """
        DESCRIPTION: Verify list of events
        EXPECTED: Just events that have Market with following attributes and outcomes are displayed:
        EXPECTED: *   **name="Match Betting"**
        EXPECTED: *   **dispSortName="MR"**
        """
        self.__class__.hockey_sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.hockey_sections, msg='No sections on Hockey page')
        for section_name, section in self.hockey_sections.items():
            if not section.is_expanded():
                section.expand()
                section = self.get_section(section_name=section_name)
            sections = section.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No events in section "{section_name}"')
            for event_name, event in sections.items():
                if not event_name.startswith("Outright"):
                    self.assertIn(event_name, self.displayed_market_betting_event_list,
                                  msg='Events with required attributes are not displayed')

    def test_003_verify_order_of_priceodds_buttons(self):
        """
        DESCRIPTION: Verify order of Price/Odds buttons
        EXPECTED: For **Match Betting** primary market selections are shown in one row next to the Event name and are ordered by the rule:
        EXPECTED: *   outcomeMeaningMinorCode="H" is a Home ***'Win'***
        EXPECTED: *   outcomeMeaningMinorCode="D" is a ***'Draw'***
        EXPECTED: *   outcomeMeaningMinorCode="A" is an Away **'*Win'***
        """
        event = self.get_event_from_league(event_id=self.eventID, section_name=self.section_name)
        self.assertTrue(event, msg=f'Event "{self.womens_olympics_event_name}" not found on hockey page')
        actual_selections = event.template.items_as_ordered_dict.keys()
        expected_selection = self.prices.values()
        self.assertListEqual(list(actual_selections), list(expected_selection), msg=f'Price/Odds buttons are not same'
                                                                                    f'Actual: "{actual_selections}"'
                                                                                    f'Expected "{expected_selection}"')

    def test_004_tap_in_play_tab_for_desktop_only_note_for_mobile_in_play_module_on_single_view_page(self):
        """
        DESCRIPTION: Tap 'In-Play' tab (For desktop only)
        DESCRIPTION: Note: for mobile: In-Play module on single view page
        EXPECTED: **'In-Play' **tab is opened
        """
        if self.device_type == 'mobile':
            in_play_module = self.site.home.tab_content.in_play_module
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
        EXPECTED: *   **name="Match Betting"**
        EXPECTED: *   **dispSortName="MR"**
        EXPECTED: 2) Outright events with attribute '**eventSortCode="TNMT"/"TRxx"**(xx - numbers from 01 to 20)' are shown
        EXPECTED: *   **templateMarketName / name = "Outright"**
        EXPECTED: *   **dispSortName = "--" or any positive code (e.g. "3W")**
        """
        #  1. Done in the scope of step 2
        hockey_sections = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(hockey_sections, msg='No sections on Hockey page')
        for section_name, section in hockey_sections.items():
            if not section.is_expanded():
                section.expand()
                section = self.get_section(section_name=section_name)
            sections = section.items_as_ordered_dict
            self.assertTrue(sections, msg=f'No events in section "{section_name}"')
            for event_name, event in sections.items():
                if event_name.startswith("Outright"):
                    self.assertIn(event_name, self.displayed_outright_event_list,
                                  msg='Events with required attributes are not displayed')

    def test_006_repeat_step_4_for_events_that_are_not_outrights(self):
        """
        DESCRIPTION: Repeat step №4 for events that are not Outrights
        """
        self.test_004_tap_in_play_tab_for_desktop_only_note_for_mobile_in_play_module_on_single_view_page()

    def test_007_repeat_steps_2_3(self):
        """
        DESCRIPTION: Repeat steps №2-3 for:
        DESCRIPTION: * 'Tomorrow' tab (for desktop only)
        DESCRIPTION: * 'Future' tab (for desktop only)
        DESCRIPTION: * 'Competition' tab (mobile only)
        DESCRIPTION: * 'Competition Detailed' page (mobile, where applicable)
        DESCRIPTION: * 'Live Stream' page/tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * 'Highlights carousel' module created on Homepage/ Landing page
        DESCRIPTION: * Featured tab module created by typeID
        DESCRIPTION: * Live Stream widget
        """
        # Not scripting as agreed
        self._logger.warning('** skipped step ')
        pass

    def test_008_repeat_steps_2_3_and_5_6(self):
        """
        DESCRIPTION: Repeat steps №2-3 and №5-6 for:
        DESCRIPTION: * In-Play tab -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play Sport page -> 'Live Now' and 'Upcoming 'filters
        DESCRIPTION: * In Play widget on Desktop
        EXPECTED:
        """
        # Not scripting as agreed
        self._logger.warning('** skipped step ')
        pass
