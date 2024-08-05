import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.pages.shared.components.grouping_buttons import  GroupingSelectionButtons

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C9337874_Verify_Basketball_Competitions_Landing_Page_Functionality(BaseSportTest):
    """
    TR_ID: C9337874
    NAME: Verify Basketball Competitions Landing Page Functionality
    DESCRIPTION: This test case verified Basketball Competitions Landing Page Functionality
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to the Basketball Landing page
    PRECONDITIONS: 3. Make sure that the 'Competition' tab is available
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The Class accordions on Competitions page are CMS configurable
    PRECONDITIONS: 2. To set classes in CMS navigate to 'System-configuration' -> 'Competitions Basketball' and put class ID's in 'InitialClassIDs' and/or 'A-ZClassIDs' field
    PRECONDITIONS: 3. To verify the availability of events in class please use the following link:
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?translationLang=en&simpleFilter=class.categoryId:equals:6&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: 4. To verify types that are available in the class please use the following link: https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForClass/XXX?translationLang=en&simpleFilter=type.hasOpenEvent:isTrue
    PRECONDITIONS: * X.XX - currently supported version of OpenBet release
    PRECONDITIONS: * XXX - class id
    PRECONDITIONS: **(!)** 'CompetitionsBasketball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True

    def sort_by_disp_order(self, sports_list: list):

        """
        :param sports_list: list of dict
        :return: sorted list by DisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['className']} - {sport['event']['typeName']}": int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get events
        """
        self.__class__.is_mobile = self.device_type == 'mobile'
        if tests.settings.backend_env != 'prod':
            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsBasketball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsBasketball')
            if str(self.ob_config.basketball_config.basketball_autotest.class_id) not in competitions_countries.get('A-ZClassIDs').split(','):
                raise CmsClientException('Basketball competition class is not configured on Competitions tab')
            self.ob_config.add_basketball_event_to_autotest_league()
            self.ob_config.add_basketball_outright_event_to_autotest_league(ew_terms=self.ew_terms)
            self.__class__.section_name_list = 'Basketball Auto Test' if self.brand == 'ladbrokes' else "BASKETBALL AUTO TEST"

        else:
            event = self.get_active_events_for_category(category_id=self.ob_config.basketball_config.category_id)[0]
            self._logger.info(f'*** Found event: {event}')
            self.__class__.section_name_list = event['event']['className']

        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')
        self.__class__.competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.basketball_config.category_id)
        self.assertTrue(self.competitions_tab_name, msg='competition tab is not available')

    def test_001_clicktap_on_competition_tab(self):
        """
        DESCRIPTION: Click/Tap on 'Competition' tab
        EXPECTED: **For Mobile/Tablet:**
        EXPECTED: * 'Popular' label is NOT displayed above the 'Popular' class accordions
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        EXPECTED: * 'A-Z COMPETITIONS' label is displayed above the 'A-Z' class accordions
        EXPECTED: * The A-Z' class accordions are loaded based on settings in 'A-ZClassIDs' field at CMS
        EXPECTED: **For Desktop:**
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * The 'Popular' class accordions are loaded based on settings in 'InitialClassIDs' field at CMS
        """
        self.site.basketball.tabs_menu.click_button(self.competitions_tab_name.upper())
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
        competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsBasketball')
        if not competitions_countries:
            competitions_countries = self.get_system_configuration_item('CompetitionsBasketball')
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

        class_ids = self.get_class_ids_for_category(category_id=self.ob_config.basketball_config.category_id)
        sports_list = ss_req.ss_event_to_outcome_for_class(query_builder=query_builder,
                                                           class_id=class_ids)
        sorted_leagues = self.sort_by_disp_order(sports_list)
        self.__class__.expected_leagues_order_upper = [
            item if not self.is_mobile and self.brand == 'ladbrokes' else item.upper() for item in
            sorted_leagues]

        competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.basketball_config.category_id)
        self.site.basketball.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.basketball.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')
        self.__class__.basketball = self.site.basketball.tab_content
        if self.is_mobile:
            a_z_competition_name_loc = self.basketball.a_z_competition_label.location.get('y')
            a_z_section_loc = self.basketball.all_competitions_categories.location.get('y')
            self.assertTrue(a_z_competition_name_loc > a_z_section_loc,
                            msg='"A-Z COMPETITIONS" label is not displayed above the "A-Z" class accordions')
            self.__class__.sections = self.basketball.all_competitions_categories.items_as_ordered_dict
            self.assertTrue(self.sections, msg=f'No A-Z sections found on "{competitions_tab_name}" tab')
            self.assertTrue(self.basketball.a_z_competition_label, msg='A-Z label is not displayed')

            initial_sections = self.basketball.competitions_categories.items_as_ordered_dict
            if cms_initial_class_ids:
                self.assertTrue(initial_sections,
                                msg=f'No Initial sections found on "{competitions_tab_name}" tab')
            else:
                self.assertFalse(initial_sections, msg=f'Initial sections found on "{competitions_tab_name}" tab')

            expected_az_class_names = [name.upper() for name in expected_az_class_names]
            expected_initial_class_names = [name.upper() for name in expected_initial_class_names]

            expected_az_class_names = list(set(expected_az_class_names))
            expected_initial_class_names = list(set(expected_initial_class_names))

            self.assertListEqual(sorted(expected_az_class_names), sorted(self.sections),
                                 msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                     f'are not the same as on ui {sorted(self.sections)}')
            self.assertListEqual(sorted(expected_initial_class_names), sorted(initial_sections),
                                 msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                     f'are not the same as on ui {sorted(initial_sections)}')
        else:
            tabs_menu_location = self.site.basketball.tabs_menu.location.get('y')
            ql_location = self.basketball.quick_link_container.location.get('y')
            self.assertTrue(ql_location > tabs_menu_location, msg='Quick links are displayed above tabs')
            grouping_buttons = self.basketball.grouping_buttons
            expected_tab_name = vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper() if self.brand == 'bma' else vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME
            self.assertEqual(grouping_buttons.current, expected_tab_name,
                             msg=f'"{expected_tab_name}" is not selected by default. '
                                 f'Default is "{grouping_buttons.current}"')
            if cms_initial_class_ids:
                initial_sections = self.basketball.accordions_list.items_as_ordered_dict
                self.assertTrue(initial_sections,
                                msg=f'No Initial sections found on "{competitions_tab_name}" tab')

                first_accordian = list(initial_sections.values())[0]
                self.assertTrue(initial_sections, msg=f'No Initial sections found on "{competitions_tab_name}" tab')
                self.assertTrue(first_accordian.is_expanded(), msg='First accordian is not expanded by default')
            else:
                self.assertTrue(self.basketball.has_no_events_label(), msg='No events label is not shown')

            grouping_buttons.click_item(vec.sb_desktop.COMPETITIONS_SPORTS)
            self.__class__.sections = self.basketball.accordions_list.items_as_ordered_dict
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
        # covered in step 1

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
            a_z_sections = list(self.basketball.all_competitions_categories.items_as_ordered_dict.values())
            self.assertTrue(a_z_sections, msg='No A-Z sections found on competitons tab')
            accordions_list_length = len(a_z_sections)
            for i in range(accordions_list_length):
                self.assertFalse(a_z_sections[i].is_expanded(expected_result=False),
                                 msg=f'Event "{a_z_sections[i]}" is not collapsed')
            self.assertListEqual(list(self.basketball.all_competitions_categories.items_as_ordered_dict.keys()),
                                 sorted(self.sections), msg='"A-Z" class accordions are not ordered alphabetically')

        else:
            grouping_buttons = self.basketball.grouping_buttons
            self.assertTrue(grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].is_selected(),
                            msg='"A-Z" switcher is not not selected and highlighted')
            a_z_firstsection = list(self.basketball.accordions_list.items_as_ordered_dict.values())[0]
            self.assertTrue(a_z_firstsection, msg='No A-Z sections found on competitons tab')
            self.assertTrue(a_z_firstsection.is_expanded(), msg=f'The First accordion is not expanded by default')
            self.assertListEqual(list(self.basketball.accordions_list.items_as_ordered_dict.keys()),
                                 sorted(self.sections), msg='"A-Z" class accordions are not ordered alphabetically')

    def test_004_expand_any_class_accordion_with_available_competitions(self):
        """
        DESCRIPTION: Expand any Class accordion with available competitions
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * The leagues (types) are displayed in the list view
        EXPECTED: * Type ID's are ordered by OpenBet display order (lowest display order at the top)
        EXPECTED: **For Desktop:**
        EXPECTED: * The leagues (types) are displayed in Horizontal position
        EXPECTED: * Type ID's are ordered by OpenBet display order (starting with lowest one)
        """
        type_order_list = []
        section_name_list = self.section_name_list.title() if not self.is_mobile and self.brand == 'ladbrokes' else self.section_name_list.upper()
        if self.device_type == 'mobile':
            section = self.basketball.all_competitions_categories.items_as_ordered_dict[section_name_list]
        else:
            section = self.basketball.accordions_list.items_as_ordered_dict[section_name_list]
        self.assertTrue(section, msg=f'Competitions page does not have any "{section_name_list}" section')
        section.expand()
        order = [item if not self.is_mobile and self.brand == 'ladbrokes' else item.upper() for item in
                 list(section.items_as_ordered_dict.keys())]
        for item in self.expected_leagues_order_upper:
            if section_name_list in item:
                type_order_list.append(item.split("-")[1].strip())
        self.assertEqual(order, type_order_list,
                         msg='Type IDs are not ordered by OpenBet display order (lowest display order at the top)')

    def test_005_clicktap_on_any_league_type_from_the_list(self):
        """
        DESCRIPTION: Click/Tap on any League (Type) from the list
        EXPECTED: **For mobile/Tablet:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 3 tabs (navigation buttons) on the page: 'Matches', 'Outrights'
        EXPECTED: * 'Matches' tab is selected by default
        EXPECTED: **For Desktop:**
        EXPECTED: * User navigates to the 'Competition Details' page
        EXPECTED: * Events from the relevant league (type) are displayed
        EXPECTED: * There are 'Matches and 'Outrights' switchers
        EXPECTED: * 'Matches' switcher is selected by default
        """
        section_name_list = self.section_name_list.title() if not self.is_mobile and self.brand == 'ladbrokes' else self.section_name_list.upper()
        section = self.sections.get(section_name_list)
        self.assertTrue(section, msg=f'"{section_name_list}" was not found')
        section.expand()
        self.assertTrue(section.is_expanded(), msg=f'Section "{self.section_name_list}" is not expanded')
        leagues = section.items_as_ordered_dict
        self.assertTrue(leagues, msg=f'No leagues found in the "{self.section_name_list}" section')
        leagues.get(list(leagues.keys())[0]).click()
        self.site.wait_content_state('CompetitionLeaguePage')
        if self.is_mobile:
            if self.site.competition_league.has_tabs_menu() :
                tabs_menu = self.site.competition_league.tabs_menu
                for tab_name, tab in tabs_menu.items_as_ordered_dict.items():
                    self.assertIn(tab_name, vec.sb.COMPETITION_DETAILS_PAGE_TABS._asdict().values(),
                                  msg=f'Market switcher tab {tab_name} is not present in the list')
                current_tab = tabs_menu.current
                self.assertEqual(current_tab, vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches,
                                 msg=f'Relevant tab is not opened, Actual "{current_tab}" '
                                     f'expected "{vec.sb.COMPETITION_DETAILS_PAGE_TABS.matches}"')
        else:
            tabs_menu = self.site.competition_league.tabs_menu
            self.assertIsInstance(tabs_menu,GroupingSelectionButtons, msg='Tabs menu was not found')
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
