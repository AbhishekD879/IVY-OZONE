import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.prod
@pytest.mark.hl
# @pytest.mark.tst2  Results and Standings usually are not available on
# @pytest.mark.stg2
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.sanity
@vtest
@pytest.mark.timeout(1200)
class Test_C874358_Verify_navigation_on_Football_Competitions_tab(BaseSportTest):
    """
    TR_ID: C874358
    NAME: Verify navigation on Football Competitions tab
    DESCRIPTION: This test case verifies 'Competitions' tab on the Football sport page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Click/Tap on the 'Competition' tab
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Football' and put class ID's in 'InitialClassIDs' and/or 'A-ZClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. IDs that are typically set in **'A-ZClassIDs'** field: 115,592,591,595,100,109,104,103,102,101,108,106,105,136,137,134,135,138,139,548,133,132,131,130,145,146,147,148,149,140,142,141,144,143,118,119,116,117,114,112,113,111,110,127,128,129,123,124,125,126,120,652,122,121,584,179,178,172,173,170,171,176,177,174,175,587,586,589,181,182,183,180,159,158,157,154,155,152,153,150,151,168,167,169,163,164,165,166,160,161,162,69,68,715,73,74,71,72,70,724,79,76,75,78,77,82,83,84,85,80,81,730,89,88,87,86,739,91,92,90,95,96,93,94,743,744,745,740,741,742,98,97,99,603,16291
    PRECONDITIONS: 5. IDs that are typically set in **'InitialClassIDs'** field:
    PRECONDITIONS: * International (Class ID = 115)
    PRECONDITIONS: * UEFA Club Comps (Class ID = 165)
    PRECONDITIONS: * England (Class ID = 97)
    PRECONDITIONS: * Scotland (Class ID=158)
    PRECONDITIONS: * Spain (Class ID=166)
    PRECONDITIONS: * Italy (Class ID=120)
    PRECONDITIONS: * Germany (Class ID=105)
    PRECONDITIONS: * France (Class ID=102)
    PRECONDITIONS: * Netherlands (Class ID=140)
    PRECONDITIONS: * USA (Class ID=176)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and league
        """
        event = self.get_competition_with_results_and_standings_tabs(
            category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
        sport_name = event.class_name.upper().split(" ")
        if sport_name[0] == vec.siteserve.FOOTBALL_TAB.upper():
            self.__class__.section_name_list = sport_name[1]
        else:
            self.__class__.section_name_list = sport_name[0]
        self.__class__.league = event.league_name
        self.__class__.type_id = event.type_id

        self.__class__.is_mobile = self.device_type == 'mobile'

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: Football sport page is shown. 'Matches' tab is opened by default and highlighted
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')

        current_tab_name = self.site.football.tabs_menu.current
        matches_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                                   self.ob_config.football_config.category_id)
        self.assertEqual(current_tab_name, matches_tab_name,
                         msg=f'Default tab is "{current_tab_name}", it is not "{matches_tab_name}"')

    def test_002_tap_click_competitions_tab(self):
        """
        DESCRIPTION: Tap/click 'Competitions' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: **For Desktop:**
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: * The sub-categories (Classes) accordions are ordered according to settings in the CMS
        """
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.football_config.category_id)
        query_builder = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, self.ob_config.football_config.category_id))\
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE))\
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M'))\
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))

        response = ss_req.ss_class(class_id='', query_builder=query_builder)

        competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
        if not competitions_countries:
            competitions_countries = self.get_system_configuration_item('CompetitionsFootball')
        cms_az_class_ids = competitions_countries['A-ZClassIDs'].split(',')
        cms_initial_class_ids = competitions_countries.get('InitialClassIDs', '')
        cms_initial_class_ids_ = cms_initial_class_ids.split(',')

        expected_az_class_names = []
        expected_initial_class_names = []

        for ss_class in response:
            for cms_az_class in cms_az_class_ids:
                if ss_class['class']['id'] == cms_az_class:
                    expected_az_class_names.append(ss_class['class']['name'])
            for cms_initial_class in cms_initial_class_ids_:
                if ss_class['class']['id'] == cms_initial_class:
                    expected_initial_class_names.append(ss_class['class']['name'])

        competitions_tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
                                                        self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')

        football = self.site.football.tab_content

        if self.is_mobile:
            self.__class__.sections = football.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(self.sections, msg=f'No A-Z sections found on "{competitions_tab_name}" tab')

            self.__class__.initial_sections = football.competitions_categories.items_as_ordered_dict
            if cms_initial_class_ids:
                self.assertTrue(self.initial_sections, msg=f'No Initial sections found on "{competitions_tab_name}" tab')
            else:
                self.assertFalse(self.initial_sections, msg=f'Initial sections found on "{competitions_tab_name}" tab')

            expected_az_class_names = [name.upper().replace('FOOTBALL ', '') for name in expected_az_class_names]
            expected_initial_class_names = [name.upper().replace('FOOTBALL ', '') for name in expected_initial_class_names]

            expected_az_class_names = list(set(expected_az_class_names))
            expected_initial_class_names = list(set(expected_initial_class_names))

            self.assertListEqual(sorted(expected_az_class_names), sorted(self.sections),
                                 msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                     f'are not the same as on ui {sorted(self.sections)}')
            self.assertListEqual(sorted(expected_initial_class_names), sorted(self.initial_sections),
                                 msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                     f'are not the same as on ui {sorted(self.initial_sections)}')
        else:
            tabs_menu_location = self.site.football.tabs_menu.location.get('y')
            ql_location = football.quick_link_container.location.get('y')
            self.assertTrue(ql_location > tabs_menu_location, msg='Quick links are displayed above tabs')
            grouping_buttons = football.grouping_buttons
            expected_tab_name = vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper() if self.brand == 'bma' else vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME
            self.assertEqual(grouping_buttons.current, expected_tab_name,
                             msg=f'"{expected_tab_name}" is not selected by default. '
                                 f'Default is "{grouping_buttons.current}"')
            if cms_initial_class_ids:
                self.__class__.initial_sections = football.accordions_list.items_as_ordered_dict
                self.assertTrue(self.initial_sections, msg=f'No Initial sections found on "{competitions_tab_name}" tab')
            else:
                self.assertTrue(football.has_no_events_label(), msg='No events label is not shown')
                self.__class__.initial_sections = {}

            grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
            self.__class__.sections = football.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg='Sections not found')

            self.assertTrue(grouping_buttons.items_as_ordered_dict, msg='No grouping buttons found')
            if self.brand == 'bma':
                self.assertListEqual(list(grouping_buttons.items_as_ordered_dict.keys()),
                                     [vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper(), vec.sb_desktop.COMPETITIONS_SPORTS.upper()],
                                     msg=f'Grouping buttons are not the same as expected')
            else:
                self.assertListEqual(list(grouping_buttons.items_as_ordered_dict.keys()),
                                     [vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME,
                                      vec.sb_desktop.COMPETITIONS_SPORTS],
                                     msg=f'Grouping buttons are not the same as expected')

            if self.brand == 'bma':
                football_name_to_replace = 'FOOTBALL '
                expected_az_class_names = [name.upper() for name in expected_az_class_names]
                expected_initial_class_names = [name.upper() for name in expected_initial_class_names]
            else:
                football_name_to_replace = 'Football '

            expected_az_class_names = [name.replace(football_name_to_replace, '') for name in expected_az_class_names]
            expected_initial_class_names = [name.replace(football_name_to_replace, '') for name in expected_initial_class_names]

            expected_az_class_names = list(set(expected_az_class_names))
            expected_initial_class_names = list(set(expected_initial_class_names))

            self.assertListEqual(sorted(expected_az_class_names), sorted(self.sections),
                                 msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                     f'are not the same as on ui {sorted(self.sections)}')
            self.assertListEqual(sorted(expected_initial_class_names), sorted(self.initial_sections),
                                 msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                     f'are not the same as on ui {sorted(self.initial_sections)}')

    def test_003_tapclick_on_sub_category_class_id_with_type_ids(self):
        """
        DESCRIPTION: Tap/click on sub-category (Class ID) with Type ID's
        EXPECTED: List of Competitions (Type ID) displayed
        """
        section_name_list = self.section_name_list.title() if not self.is_mobile and self.brand == 'ladbrokes' else self.section_name_list

        section = self.sections.get(section_name_list)
        self.assertTrue(section, msg=f'"{section_name_list}" was not found')
        section.expand()
        self.assertTrue(section.is_expanded(), msg=f'Section "{section_name_list}" is not expanded')
        self.__class__.leagues = section.items_as_ordered_dict
        self.assertTrue(self.leagues, msg=f'No leagues found in the "{section_name_list}" section')

    def test_004_tapclick_on_any_competition_name_type(self):
        """
        DESCRIPTION: Tap/click on any Competition name (Type)
        EXPECTED: * 'Competition Details' page is opened
        EXPECTED: * Events from the relevant league (Type) are displayed
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * There are 4 tabs (navigation buttons) on the page: 'Matches', 'Outrights', 'Results', 'Standings' (when available)
        EXPECTED: * 'Matches' tab is default
        EXPECTED: **For Desktop:**
        EXPECTED: * There are 'Matches and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * "Results' are presented in a separate widget
        """
        league = self.leagues.get(self.league)
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

        self.__class__.tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(self.tabs_menu, msg='Tabs menu was not found')

        if self.is_mobile:
            for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
                self.assertIn(tab_name, vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values(),
                              msg=f'Market switcher tab {tab_name} is not present in the list')
            if vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches in [tab_name.upper() for tab_name in self.tabs_menu.items_as_ordered_dict.keys()]:
                current_tab = self.tabs_menu.current
                self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')
        else:
            self.__class__.desktop_tabs = list(vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()) \
                if self.brand == 'bma' else [tab.title() for tab in vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()]
            for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
                self.assertIn(tab_name, self.desktop_tabs,
                              msg=f'Market switcher tab {tab_name} is not present in the list')

            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, self.desktop_tabs[0],
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{self.desktop_tabs[0]}"')
            self.__class__.results_widget = self.site.competition_league.results_widget
            wait_for_result(lambda: self.results_widget.is_displayed(), timeout=3)
            self.assertTrue(self.results_widget.is_displayed(), msg='Results widget is not displayed')

    def test_005_check_results_section_widget_content(self):
        """
        DESCRIPTION: Check Results section/widget content
        EXPECTED: - Latest results for events are displayed
        EXPECTED: - Tab is not shown - In case results are absent for whole section **for Mobile/tablet**
        EXPECTED: - 'Results' widget is not shown in case results are absent **for Desktop**
        """
        if self.is_mobile:
            self.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.results)
            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.results,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.results}"')

            if not self.site.competition_league.tab_content.has_no_events_label():
                events = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
                self.assertTrue(events, msg=f'No events found on "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.results}" tab')
        else:
            events = self.results_widget.items_as_ordered_dict
            self.assertTrue(events, msg='No results found in the Results widget')

    def test_006_check_outrights_section_content(self):
        """
        DESCRIPTION: Check Outrights section content
        EXPECTED: - A list of Outright events available for the selected competition is shown
        EXPECTED: - Tab is not shown - In case events are absent for whole section
        """
        query_builder = self.ss_query_builder\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                      vec.siteserve.OUTRIGHT_EVENT_SORT_CODES))\
            .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, self.end_date))
        ss_outright_events = self.ss_req.ss_event_to_outcome_for_type(type_id=self.type_id, query_builder=query_builder, raise_exceptions=False)

        outright_tab_ui_title = vec.sb.COMPETITION_DETAILS_PAGE_TABS.outrights if self.is_mobile else self.desktop_tabs[1]

        if ss_outright_events:
            tabs_on_ui = list(self.tabs_menu.items_as_ordered_dict.keys())
            self.assertTrue(outright_tab_ui_title in tabs_on_ui, msg=f'"{outright_tab_ui_title}" tab is not present in {tabs_on_ui}')
            self.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.outrights)
            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, outright_tab_ui_title,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" expected "{outright_tab_ui_title}"')
            if self.is_mobile:
                self.assertTrue(self.site.competition_league.tab_content.event_league, msg='Event league was not found')
            else:
                self.assertTrue(self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict,
                                msg='Outright events were not found')
        else:
            tabs_on_ui = list(self.tabs_menu.items_as_ordered_dict.keys())
            self.assertTrue(outright_tab_ui_title not in tabs_on_ui,
                            msg=f'"{outright_tab_ui_title}" tab is present in {tabs_on_ui}')

    def test_007_check_standings_tab_mobiletablet_for_desktop_standings_are_presented_on_league_table_widget_that_is_shown_on_matches_and_outrights(self):
        """
        DESCRIPTION: Check Standings tab (mobile/tablet)
        DESCRIPTION: * for Desktop Standings are presented on League Table widget that is shown on Matches and Outrights
        EXPECTED: - Statistics table is shown for the selected league for current season
        EXPECTED: - There is a possibility to navigate between seasons (e.g. Premier League 2018/2019 > Premier League 2017/2018 ) using navigation arrows
        EXPECTED: - Tab is not shown when statistics are not received
        """
        if self.is_mobile:
            self.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings)
            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.standings}"')

            competition_name = self.site.competition_league.title_section.type_name.text
            self.assertEqual(competition_name, self.league,
                             msg=f'Competition header with competition name is not same '
                                 f'Actual: "{competition_name}" '
                                 f'Expected: "{self.league}"')
            tab_content = self.site.competition_league.tab_content
            self.assertTrue(tab_content.previous_arrow.is_displayed(),
                            msg='Arrow to switch to previous season is not shown')

            self.assertTrue(tab_content.results_table.is_displayed(),
                            msg='Table with result was not found')
        else:
            self.__class__.standings_widget = self.site.competition_league.standings_widget
            self.assertTrue(self.standings_widget.season_name, msg='Season name is not displayed')

            self.assertTrue(self.standings_widget.previous_arrow.is_displayed(), msg='Previous arrow is not displayed')

    def test_008_check_matches_tab(self):
        """
        DESCRIPTION: Check 'Matches' tab
        EXPECTED: - A list of MATCH events available for selected competition is shown
        EXPECTED: - 'No events found' message - in case events are absent for selected competition for **Desktop**
        EXPECTED: * 'Matches' tab is not shown in case events are absent for selected competition for **Mobile**
        """
        self.__class__.is_matches_tab_present = True if vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches in [tab_name.upper() for tab_name in self.tabs_menu.items_as_ordered_dict.keys()] else False
        if self.is_mobile:
            self.softAssert(self.assertTrue, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches in
                            list(self.tabs_menu.items_as_ordered_dict.keys()),
                            msg=f'"{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}" tab is not present')

            self.tabs_menu.click_button(vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches)
            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')

            self.__class__.sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections,
                            msg=f'No sections found on "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}" tab')
        else:
            self.softAssert(self.assertTrue, self.desktop_tabs[0] in
                            list(self.tabs_menu.items_as_ordered_dict.keys()),
                            msg=f'"{self.desktop_tabs[0]}" tab is not present')

            self.tabs_menu.click_button(self.desktop_tabs[0])
            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, self.desktop_tabs[0],
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{self.desktop_tabs[0]}"')

            self.__class__.sections = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
            self.softAssert(self.assertTrue,self.sections, msg=f'No sections found on "{self.desktop_tabs[0]}" tab')

    def test_009_verify_matches_section_content(self):
        """
        DESCRIPTION: Verify 'Matches' section content
        EXPECTED: - Market selector with list of markets which are available for events is displayed
        EXPECTED: - Events with selected market is displayed
        """
        if self.is_matches_tab_present:
            section_name, section = list(self.sections.items())[0]
            self.softAssert(self.assertTrue,section.items_as_ordered_dict, msg=f'No events found in the "{section_name}" section on '
                                                           f'"{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}" tab')

            self.softAssert(self.assertTrue,self.site.competition_league.tab_content.has_dropdown_market_selector(),
                        msg='Market selector is not present')
