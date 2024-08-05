import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.slow
@vtest
class Test_C9346564_Verify_Football_Competitions_Landing_Page_Functionality(BaseSportTest):
    """
    TR_ID: C9346564
    NAME: Verify Football Competitions Landing Page Functionality
    DESCRIPTION: This test case verified Football Competitions Landing Page Functionality
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to Football Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
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
    PRECONDITIONS: **(!)** 'CompetitionsFootball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    PRECONDITIONS: 6. When user navigates to ant type (Competitions Detailed page), events data is received in EventToOutcomeForType request to SS which should include only markets listed in request. For example:
    PRECONDITIONS: https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventToOutcomeForType/500?simpleFilter=event.eventSortCode:notIntersects:TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20&simpleFilter=market.templateMarketName:intersects:|Match%20Betting|,|Over/Under%20Total%20Goals|,|Both%20Teams%20to%20Score|,|To%20Qualify|,|Draw%20No%20Bet|,|First-Half%20Result|,|Next%20Team%20to%20Score|,|Extra-Time%20Result|,Match%20Betting,Over/Under%20Total%20Goals,Both%20Teams%20to%20Score,To%20Qualify,Draw%20No%20Bet,First-Half%20Result,Next%20Team%20to%20Score,Extra-Time%20Result,Match%20Result%20and%20Both%20Teams%20To%20Score,|Match%20Result%20and%20Both%20Teams%20To%20Score|&translationLang=en&responseFormat=json&prune=event&prune=market&childCount=event
    """
    keep_browser_open = True

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by DisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['className']} - {sport['event']['typeName']}":
                                int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get event and league
        """
        if tests.settings.backend_env != 'prod':

            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsFootball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsFootball')
            if str(self.ob_config.football_config.autotest_class.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.football_autotest_competition} class '
                                         f'is not configured on Competitions tab')

            self.ob_config.add_autotest_premier_league_football_event(selections_number=1)
            self.ob_config.add_autotest_premier_league_football_outright_event(ew_terms=self.ew_terms)
            self.__class__.section_name_list = 'Auto Test' if self.brand == 'ladbrokes' else tests.settings.football_autotest_competition
            self.__class__.league = tests.settings.football_autotest_competition_league.title()
        else:
            event = self.get_competition_with_results_and_standings_tabs(
                category_id=self.ob_config.football_config.category_id, raise_exceptions=True)
            sport_name = event.class_name.upper().split(" ")
            if sport_name[0] == vec.siteserve.FOOTBALL_TAB.upper():
                self.__class__.section_name_list = sport_name[1]
            else:
                self.__class__.section_name_list = sport_name[0]
            self.__class__.league = event.league_name
        self.__class__.is_mobile = self.device_type == 'mobile'

    def test_001_verify_layout_of_competitions_tab(self):
        """
        DESCRIPTION: Verify layout of 'Competitions' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        EXPECTED: * The A-Z' class accordions are loaded based on settings in 'A-ZClassIDs' field at CMS
        EXPECTED: * 'A-Z COMPETITIONS' label is displayed above the 'A-Z' class accordions
        EXPECTED: **For Desktop:**
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' fields at CMS
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')

        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.football_config.category_id)
        query_builder = self.ss_query_builder \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                      self.ob_config.football_config.category_id)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE)) \
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, 'M')) \
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

        class_ids = self.get_class_ids_for_category(category_id=self.ob_config.football_config.category_id)
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query_builder,
                                                           class_id=class_ids)
        sorted_leagues = self.sort_by_disp_order(sports_list)
        self.__class__.expected_leagues_order_upper = [item.upper() if self.brand == 'bma' else item for item in
                                                       sorted_leagues]

        competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')

        self.__class__.football = self.site.football.tab_content

        if self.is_mobile:
            a_z_competition_name = self.football.a_z_competition_label.name
            self.assertTrue(a_z_competition_name,
                            msg=f'A-Z competition name label is not found on "{competitions_tab_name}" tab')
            a_z_competition_name_loc = self.football.a_z_competition_label.location.get('y')
            a_z_section_loc = self.football.all_competitions_categories.location.get('y')
            self.assertTrue(a_z_competition_name_loc > a_z_section_loc,
                            msg='"A-Z COMPETITIONS" label is not displayed above the "A-Z" class accordions')
            self.__class__.sections = self.football.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(self.sections, msg=f'No A-Z sections found on "{competitions_tab_name}" tab')

            initial_sections = self.football.competitions_categories.items_as_ordered_dict
            if cms_initial_class_ids:
                self.assertTrue(initial_sections,
                                msg=f'No Initial sections found on "{competitions_tab_name}" tab')
            else:
                self.assertFalse(initial_sections, msg=f'Initial sections found on "{competitions_tab_name}" tab')

            expected_az_class_names = [name.upper().replace('FOOTBALL ', '') for name in expected_az_class_names]
            expected_initial_class_names = [name.upper().replace('FOOTBALL ', '') for name in
                                            expected_initial_class_names]

            expected_az_class_names = list(set(expected_az_class_names))
            expected_initial_class_names = list(set(expected_initial_class_names))

            self.assertListEqual(sorted(expected_az_class_names), sorted(self.sections),
                                 msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                     f'are not the same as on ui {sorted(self.sections)}')
            self.assertListEqual(sorted(expected_initial_class_names), sorted(initial_sections),
                                 msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                     f'are not the same as on ui {sorted(initial_sections)}')
        else:
            tabs_menu_location = self.site.football.tabs_menu.location.get('y')
            ql_location = self.football.quick_link_container.location.get('y')
            self.assertTrue(ql_location > tabs_menu_location, msg='Quick links are displayed above tabs')
            grouping_buttons = self.football.grouping_buttons
            expected_tab_name = vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper() if self.brand == 'bma' else vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME
            self.assertEqual(grouping_buttons.current, expected_tab_name,
                             msg=f'"{expected_tab_name}" is not selected by default. '
                                 f'Default is "{grouping_buttons.current}"')
            if cms_initial_class_ids:
                initial_sections = self.football.accordions_list.items_as_ordered_dict
                first_accordian = list(initial_sections.values())[0]
                self.assertTrue(initial_sections,
                                msg=f'No Initial sections found on "{competitions_tab_name}" tab')
                self.assertTrue(first_accordian.is_expanded(),
                                msg='First accordian is not expanded by default')

            else:
                self.assertTrue(self.football.has_no_events_label(), msg='No events label is not shown')
                initial_sections = {}

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

            if self.brand == 'bma':
                football_name_to_replace = 'FOOTBALL '
                expected_az_class_names = [name.upper() for name in expected_az_class_names]
                expected_initial_class_names = [name.upper() for name in expected_initial_class_names]
            else:
                football_name_to_replace = 'Football '

            expected_az_class_names = [name.replace(football_name_to_replace, '') for name in expected_az_class_names]
            expected_initial_class_names = [name.replace(football_name_to_replace, '') for name in
                                            expected_initial_class_names]

            expected_az_class_names = list(set(expected_az_class_names))
            expected_initial_class_names = list(set(expected_initial_class_names))

            self.assertListEqual(sorted(expected_az_class_names), sorted(self.sections),
                                 msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                     f'are not the same as on ui {sorted(self.sections)}')
            self.assertListEqual(sorted(expected_initial_class_names), sorted(initial_sections),
                                 msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                     f'are not the same as on ui {sorted(initial_sections)}')

    def test_002_for_mobiletabletcheck_popular_class_accordionsfor_desktopcheck_popular_class_accordions_when_popular_switcher_is_selected(
            self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Check 'Popular' class accordions
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Check 'Popular' class accordions when 'Popular' switcher is selected
        EXPECTED: * 'Popular' accordions for classes that are set in 'InitialClassIDs' at CMS are displayed
        EXPECTED: * The First accordion is expanded by default
        EXPECTED: * 'Popular' class accordions  are ordered according to settings is CMS
        """
        # Covered in step 1

    def test_003_for_mobiletabletcheck_a_z_class_accordionsfor_desktopcheck_a_z_class_accordions_when_a_z_switcher_is_selected(
            self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Check 'A-Z' class accordions
        DESCRIPTION: **For Desktop:**
        DESCRIPTION: Check 'A-Z' class accordions when 'A-Z' switcher is selected
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * 'A-Z' accordions are loaded based on settings in 'A-ZClassIDs' at CMS
        EXPECTED: * All accordions are collapsed by default
        EXPECTED: * 'A-Z' class accordions are ordered alphabetically
        EXPECTED: **For Desktop:**
        EXPECTED: * 'A-Z' switcher is selected and highlighted
        EXPECTED: * 'A-Z' accordions are loaded based on settings in 'A-ZClassIDs' at CMS
        EXPECTED: * The First accordion is expanded by default
        EXPECTED: * 'A-Z' class accordions are ordered alphabetically
        """
        if self.is_mobile:
            a_z_sections = list(self.football.all_competitions_categories.items_as_ordered_dict.values())
            self.assertTrue(a_z_sections, msg='No A-Z sections found on competitons tab')
            accordions_list_length = len(a_z_sections)
            for i in range(accordions_list_length):
                self.assertFalse(a_z_sections[i].is_expanded(expected_result=False),
                                 msg=f'Event "{a_z_sections[i]}" is not collapsed')
            self.assertListEqual(list(self.football.all_competitions_categories.items_as_ordered_dict.keys()),
                                 sorted(self.sections), msg='"A-Z" class accordions are not ordered alphabetically')
        # grouping button are only applicable in desktop mode
        else:
            grouping_buttons = self.football.grouping_buttons
            self.assertTrue(grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].is_selected(),
                            msg='"A-Z" switcher is not not selected and highlighted')
            section_dict = self.football.accordions_list.items_as_ordered_dict
            a_z_firstsection = list(section_dict.values())[0]
            self.assertTrue(a_z_firstsection, msg='No A-Z sections found on competitons tab')
            self.assertTrue(a_z_firstsection.is_expanded(),
                            msg=f'The First accordion is not expanded by default')
            # to campare the order of the frontend in coral it converted to upper but from backend its in title casing
            # also usa and uefa are abbreviation they should in capital
            self.ui_sections = list(section_dict.keys())
            self.ui_sections = [section.title() for section in self.ui_sections] if self.brand == "bma" else self.ui_sections
            if self.brand == "bma" and "Usa" in self.ui_sections:
                self.ui_sections[self.ui_sections.index("Usa")] = "USA"
            if self.brand == "bma" and "Uefa Club Competitions" in self.ui_sections:
                self.ui_sections[self.ui_sections.index("Uefa Club Competitions")] = "UEFA Club Competitions"
            self.assertListEqual(self.ui_sections,
                                 sorted(self.ui_sections), msg='"A-Z" class accordions are not ordered alphabetically')

    def test_004_expand_any_class_accordion_with_available_competitions(self):
        """
        DESCRIPTION: Expand any class accordion with available competitions
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: * Type ID's are ordered by OpenBet display order (lowest display order at the top)
        EXPECTED: **For Desktop:**
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        EXPECTED: * Type ID's are ordered by OpenBet display order (starting with lowest one)
        """
        type_order_list = []
        if self.is_mobile:
            section_name_list = self.section_name_list if self.brand == 'bma' else self.section_name_list.upper()
            section = self.football.all_competitions_categories.items_as_ordered_dict[section_name_list]
        else:
            section_name_list = self.section_name_list if self.brand == 'bma' else self.section_name_list.title()
            section = self.football.accordions_list.items_as_ordered_dict[section_name_list]
        self.assertTrue(section, msg=f'Competitions page does not have any "{self.section_name_list}" section')
        section.expand()
        order = [item.upper() if self.brand == 'bma' else item for item in list(section.items_as_ordered_dict.keys())]
        for item in self.expected_leagues_order_upper:
            if self.section_name_list.lower() in item.lower() and item != 'Featured Autotest League':
                type_order_list.append(item.split("-")[1].strip())
        self.assertEqual(order, type_order_list,
                         msg=f'Type IDs "{order}"are not ordered by OpenBet display order "{type_order_list}" (lowest display order at the top)')

    def test_005_clicktap_on_league_type(self):
        """
        DESCRIPTION: Click/Tap on League (Type)
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 3 tabs (navigation buttons) on the page: 'Matches', 'Results', 'Outrights'
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: **For Desktop:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 'Matches and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default
        EXPECTED: * 'Results' and 'League Table' widgets are displayed if available
        """
        section_name_list = self.section_name_list if self.brand == 'bma' else self.section_name_list.title()
        if self.is_mobile and self.brand == 'ladbrokes':
            section_name_list = self.section_name_list.title().upper()
        section = self.sections.get(section_name_list)
        self.assertTrue(section, msg=f'"{section_name_list}" was not found')
        section.expand()
        self.assertTrue(section.is_expanded(), msg=f'Section "{section_name_list}" is not expanded')
        leagues = section.items_as_ordered_dict
        self.assertTrue(leagues, msg=f'No leagues found in the "{section_name_list}" section')

        league = leagues.get(self.league)
        league.click()
        self.site.wait_content_state('CompetitionLeaguePage')

        self.__class__.tabs_menu = self.site.competition_league.tabs_menu
        self.assertTrue(self.tabs_menu, msg='Tabs menu was not found')

        if self.is_mobile:
            for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
                self.assertIn(tab_name, vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values(),
                              msg=f'Market switcher tab {tab_name} is not present in the list')

            current_tab = self.tabs_menu.current
            self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')
        else:
            desktop_tabs = list(vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()) \
                if self.brand == 'bma' else [tab.title() for tab in
                                             vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values()]
            for tab_name, tab in self.tabs_menu.items_as_ordered_dict.items():
                self.assertIn(tab_name, desktop_tabs,
                              msg=f'Market switcher tab {tab_name} is not present in the list')
            self.site.wait_content_state_changed()
            current_tab = self.tabs_menu.current
            expected_tab = vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches if self.brand == 'bma' else vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches.capitalize()
            self.assertEqual(current_tab, expected_tab,
                             msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                 f'expected "{desktop_tabs[0]}"')
            try:
                self.__class__.results_widget = self.site.competition_league.results_widget
                self.assertTrue(self.results_widget.is_displayed(), msg='Results widget is not displayed')
            except Exception:
                self._logger.info(f'The result widget is not displayed')
