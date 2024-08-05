import pytest
import tests
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from tests.base_test import vtest
from datetime import datetime, timedelta
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C1053929_Verify_Matches_and_Outrights_switchers_functionality_on_Competitions_page_for_Desktop(BaseSportTest):
    """
    TR_ID: C1053929
    NAME: Verify 'Matches' and 'Outrights' switchers functionality on Competitions page for Desktop
    DESCRIPTION: This test case verifies 'Matches' and 'Outrights' switchers functionality on Competitions page for Desktop.
    DESCRIPTION: Need to run test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The sub-categories (Classes) are CMS configurable on Competitions page and are ordered according to settings in the CMS.
    PRECONDITIONS: 2. Types (Competitions) are ordered by OpenBet display order (lowest display order at the top)
    PRECONDITIONS: For setting sub-categories in CMS navigate to 'System-configuration' -> 'Competitions' and put class ID's in 'InitialClassIDs' or 'A-ZClassIDs' field.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by DisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {
            f"{sport['event']['className']} - {sport['event']['typeName']}": int(sport['event']['typeDisplayOrder']) for
            sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get events
        """
        self.__class__.is_mobile = self.device_type == 'mobile'
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException('Football competition class is not configured on Competitions tab')
            self.ob_config.add_autotest_premier_league_football_event()
            self.ob_config.add_autotest_premier_league_football_outright_event(ew_terms=self.ew_terms)
            self.__class__.section_name_list = 'Auto Test' if self.brand == 'ladbrokes' else tests.settings.football_autotest_competition

        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self._logger.info(f'*** Found event: {event}')
            self.__class__.section_name_list = event['event']['className']

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        self.__class__.competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.football_config.category_id)
        self.assertTrue(self.competitions_tab_name, msg='competition tab is not available')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        # covered in above step

    def test_002_navigate_to_football_landing_page___competitions_tab(self):
        """
        DESCRIPTION: Navigate to Football Landing page -> 'Competitions' tab
        EXPECTED: Competitions Landing page is opened
        """
        self.site.football.tabs_menu.click_button(
            button_name=self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                category_id=self.ob_config.football_config.category_id))
        self.__class__.competitions = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.competitions, msg='No competitions are present on page')

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.basketball_config.category_id)
        query_builder = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.basketball_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))

        response = ss_req.ss_class(class_id='', query_builder=query_builder)
        competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
        if not competitions_countries:
            competitions_countries = self.get_system_configuration_item('CompetitionsFootball')
        cms_az_class_ids = competitions_countries['A-ZClassIDs'].split(',')
        self.__class__.cms_initial_class_ids = competitions_countries.get('InitialClassIDs', '')
        cms_initial_class_ids_ = self.cms_initial_class_ids.split(',')

        expected_az_class_names = []
        expected_initial_class_names = []
        for ss_class in response:
            for cms_az_class in cms_az_class_ids:
                if ss_class['class']['id'] == cms_az_class:
                    expected_az_class_names.append(ss_class['class']['name'])
            for cms_initial_class in cms_initial_class_ids_:
                if ss_class['class']['id'] == cms_initial_class:
                    expected_initial_class_names.append(ss_class['class']['name'])

        class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query_builder,
                                                           class_id=class_ids)
        sorted_leagues = self.sort_by_disp_order(sports_list)
        self.__class__.expected_leagues_order_upper = [
            item if not self.is_mobile and self.brand == 'ladbrokes' else item.upper() for item in
            sorted_leagues]

        competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')
        self.__class__.football = self.site.football.tab_content

        tabs_menu_location = self.site.football.tabs_menu.location.get('y')
        ql_location = self.football.quick_link_container.location.get('y')
        self.assertTrue(ql_location > tabs_menu_location, msg='Quick links are displayed above tabs')
        grouping_buttons = self.football.grouping_buttons
        expected_tab_name = vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper() if self.brand == 'bma' else vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME
        self.assertEqual(grouping_buttons.current, expected_tab_name,
                         msg=f'"{expected_tab_name}" is not selected by default. '
                             f'Default is "{grouping_buttons.current}"')
        if self.cms_initial_class_ids:
            self.__class__.initial_sections = self.football.accordions_list.items_as_ordered_dict
            self.assertTrue(self.initial_sections,
                            msg=f'No Initial sections found on "{competitions_tab_name}" tab')

            first_accordian = list(self.initial_sections.values())[0]
            self.assertTrue(self.initial_sections, msg=f'No Initial sections found on "{competitions_tab_name}" tab')
            self.assertTrue(first_accordian.is_expanded(), msg='First accordian is not expanded by default')
        else:
            self.assertTrue(self.football.has_no_events_label(), msg='No events label is not shown')

            grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
            self.__class__.sections = self.football.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='Sections not found')

            self.assertTrue(grouping_buttons.items_as_ordered_dict, msg='No grouping buttons found')
            if self.brand == 'bma':
                self.assertListEqual(list(grouping_buttons.items_as_ordered_dict.keys()),
                                     [vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper(),
                                      vec.sb_desktop.COMPETITIONS_SPORTS.upper()],
                                     msg=f'Grouping buttons are not the same as expected')
            else:
                self.assertListEqual(list(grouping_buttons.items_as_ordered_dict.keys()),
                                     [vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME,
                                      vec.sb_desktop.COMPETITIONS_SPORTS],
                                     msg=f'Grouping buttons are not the same as expected')

            expected_az_class_names = [name.upper() if self.brand == 'bma' else name for name in
                                       expected_az_class_names]
            expected_initial_class_names = [name.upper() if self.brand == 'bma' else name for name in
                                            expected_initial_class_names]

            expected_az_class_names = list(set(expected_az_class_names))
            expected_initial_class_names = list(set(expected_initial_class_names))
            self.assertListEqual(sorted(expected_az_class_names), sorted(self.sections),
                                 msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                     f'are not the same as on ui {sorted(self.sections)}')
            self.assertListEqual(sorted(expected_initial_class_names), sorted(self.initial_sections),
                                 msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                     f'are not the same as on ui {sorted(self.initial_sections)}')

    def test_003_expand_any_classes_accordion_and_select_any_type_competition(self):
        """
        DESCRIPTION: Expand any Classes accordion and select any Type (Competition)
        EXPECTED: * Competition Details page is opened
        EXPECTED: * 'Matches' and 'Outrights' switchers are displayed below Competitions header and Breadcrumbs trail in the same row as 'Market Selector'
        EXPECTED: * 'Matches' switcher is selected by default and highlighted
        EXPECTED: * List of events is loaded on the page
        """
        if tests.settings.backend_env == 'prod':
            competition_league = vec.siteserve.PREMIER_LEAGUE_NAME
            if tests.settings.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = vec.siteserve.ENGLAND.title()
            else:
                league = vec.siteserve.ENGLAND
        else:
            if tests.settings.brand == 'ladbrokes' and self.device_type == 'desktop':
                league = 'Auto Test'
            else:
                league = 'AUTO TEST'
            competition_league = vec.siteserve.AUTO_TEST_PREMIER_LEAGUE_NAME
        competition = self.competitions[league]
        competition.expand()
        leagues = wait_for_result(lambda: competition.items_as_ordered_dict,
                                  name='Leagues list is loaded',
                                  timeout=2)
        self.assertTrue(leagues, msg='No leagues are present on page')
        self.assertIn(competition_league, leagues.keys(),
                      msg=f'League "{competition_league}" is not found in "{list(leagues.keys())}"')
        self.__class__.league = leagues[competition_league]
        self.league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

        tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(tabs_menu, msg='Tabs menu was not found')

        desktop_tabs = list(vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()) \
            if self.brand == 'bma' else [tab.title() for tab in
                                         vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()]
        for tab_name, tab in tabs_menu.items_as_ordered_dict.items():
            self.assertIn(tab_name, desktop_tabs,
                          msg=f'Market switcher tab {tab_name} is not present in the list')
        current_tab = tabs_menu.current
        if self.brand == "bma":
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{desktop_tabs[0]}"')
        else:
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches.title(),
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{desktop_tabs[0]}"')

    def test_004_verify_navigation_between_matches_and_outrights_switchers(self):
        """
        DESCRIPTION: Verify navigation between 'Matches' and 'Outrights' switchers
        EXPECTED: * The User must be able to select 'Matches' and 'Outrights' switchers
        EXPECTED: * Selected switcher is highlighted by red line
        EXPECTED: * If user selects 'Matches'/'Outrights' switcher they will be redirected to 'Matches'/'Outrights' page
        """
        self.__class__.tabs_menu = self.site.competition_league.tabs_menu.items_as_ordered_dict
        for tab_name, tab in self.tabs_menu.items():
            tab.click()
            self.assertTrue(tab.is_selected(), msg='Selected switcher is not highlighted by red line')
            result = wait_for_result(lambda: self.site.competition_league.tabs_menu.current == tab_name,
                                     timeout=2,
                                     name='Navigation to next tab')
            self.assertTrue(result,
                            msg=f'Relevant tab is not opened. Actual: "{self.site.competition_league.tabs_menu.current}".'
                                f' Expected: "{tab_name}"')

    def test_005_verify_content_of_page_when_matches_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'Matches' switcher is selected
        EXPECTED: * List of events grouped by days is displayed
        EXPECTED: * Events are ordered by start time
        """
        tabs = self.site.competition_league.tabs_menu.items_as_ordered_dict
        tabs.get(vec.SB.TABS_NAME_MATCHES.upper()).click() if self.brand == 'bma' else tabs.get(
            vec.SB.TABS_NAME_MATCHES).click()
        matches_events = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(matches_events, msg=f' "{matches_events}"List of events grouped by days is not displayed')
        event_time_list = []
        for item in list(matches_events.keys()):
            event_time_list.append(item[:6])
        # this if block is written to convert the today string received from u.i to the date formate
        if 'Today' in event_time_list:
            today = datetime.today()
            date_str = today.strftime('%d %b')
            event_time_list[event_time_list.index('Today')] = date_str
        # this if block is written to convert the tomorr string received from u.i to the date formate
        if 'Tomorr' in event_time_list:
            today = datetime.today()
            tomorrow = today + timedelta(days=1)
            date_str = tomorrow.strftime('%d %b')
            event_time_list[event_time_list.index("Tomorr")] = date_str
        # we have written the below key= to convert date and month formate into date month and year and
        # sort the data according to the total string
        self.assertEqual(event_time_list, sorted(event_time_list, key=lambda date_str:datetime.strptime(date_str + f' {datetime.now().year}', "%d %b %Y")),
                         msg='Events are not in start time order')

    def test_006_verify_content_of_page_when_outrights_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'Outrights' switcher is selected
        EXPECTED: * The Events accordions are loaded on the page
        EXPECTED: * The first Events accordion is expanded by default the rest are collapsed
        EXPECTED: * The Markets sub-accordions are displayed within expanded Event accordion
        EXPECTED: * The first Markets sub-accordion is expanded by default the rest are collapsed
        EXPECTED: * The selections are displayed in Horizontal position within expanded Markets sub-accordion
        """
        tabs = self.site.competition_league.tabs_menu.items_as_ordered_dict
        tabs.get(vec.SB.TABS_NAME_OUTRIGHTS.upper()).click() if self.brand == 'bma' else tabs.get(
            vec.SB.TABS_NAME_OUTRIGHTS).click()
        initial_sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        if not initial_sections:
            initial_sections = self.site.competition_league.tab_content.accordions_list_for_competitions.items_as_ordered_dict
        self.assertTrue(initial_sections, msg=f'Outright selections are not available in {vec.SB.TABS_NAME_OUTRIGHTS}')
        first_accordian = list(initial_sections.values())[0]
        if 'Lucky Dip' in list(initial_sections)[0]:
            first_accordian = list(initial_sections.values())[1]
            first_accordian.click()
        selections = first_accordian.outright_selections
        self.assertTrue(selections, msg='selections are not displayed')
        self.assertTrue(first_accordian.is_expanded(),
                        msg='First accordian is not expanded by default')

    def test_007_verify_content_of_page_when_matchesoutrights_switcher_is_selected_and_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of page when 'Matches'/'Outrights' switcher is selected and there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on 'Matches'/'Outrights' pages
        """
        # covered in step 2
