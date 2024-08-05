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
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.reg156_fix
@vtest
class Test_C9608114_Verify_Popular_and_A_Z_switchers_functionality_for_Desktop(BaseSportTest):
    """
    TR_ID: C9608114
    NAME: Verify 'Popular' and 'A-Z' switchers functionality for Desktop
    DESCRIPTION: This test case verifies 'Popular' and 'A-Z' switchers functionality for Desktop
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1. The sub-categories (Classes) are CMS configurable on Competitions page and are ordered according to settings in the CMS.
    PRECONDITIONS: 2. Types (Competitions) are ordered by OpenBet display order (lowest display order at the top)
    PRECONDITIONS: For setting sub-categories in CMS navigate to 'System-configuration' -> 'Competitions' and put class ID's in 'InitialClassIDs' or 'A-ZClassIDs' field.
    PRECONDITIONS: **(!)** 'CompetitionsBasketball' request is sent each time Competitions page(tab) is loaded(opened). Values from JSON response on this request are used to get the Class Accordion data from Openbet TI.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

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

            competitions_countries = self.get_initial_data_system_configuration().get('CompetitionsBasketball')
            if not competitions_countries:
                competitions_countries = self.cms_config.get_system_configuration_item('CompetitionsBasketball')
            if str(self.ob_config.basketball_config.basketball_autotest.class_id) not in competitions_countries.get(
                    'A-ZClassIDs').split(','):
                raise CmsClientException(f'{tests.settings.basketball_autotest_league} class '
                                         f'is not configured on Competitions tab')

            self.ob_config.add_basketball_event_to_autotest_league(selections_number=1)
            self.ob_config.add_basketball_outright_event_to_autotest_league(ew_terms=self.ew_terms)
            self.__class__.section_name_list = 'Auto Test' if self.brand == 'ladbrokes' else tests.settings.basketball_autotest_league
            self.__class__.league = tests.settings.basketball_autotest_league.title()
        else:
            event = self.get_active_events_for_category(
                category_id=self.ob_config.basketball_config.category_id, raise_exceptions=True)
            self.__class__.section_name_list = event[0]['event']['className'] if self.brand == 'ladbrokes' else event[0]['event']['className'].upper()
            self.__class__.league = event[0]['event']['typeName']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='Basketball')

    def test_002_navigate_to_basketball_landing_page(self):
        """
        DESCRIPTION: Navigate to Basketball Landing page
        EXPECTED: Basketball Landing page is loaded
        """
        # covered in step 1

    def test_003_click_on_competitions_tab(self):
        """
        DESCRIPTION: Click on 'Competitions' tab
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: * The first Classes accordion is expanded by default the rest are collapsed
        EXPECTED: * The leagues (Types) are displayed in Horizontal position within expanded Classes accordion
        """
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
        self.__class__.expected_leagues_order_upper = [item.upper() if self.brand == 'bma' else item for item in
                                                       sorted_leagues]

        competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.basketball_config.category_id)
        self.site.basketball.tabs_menu.click_button(competitions_tab_name.upper())
        active_tab = self.site.basketball.tabs_menu.current
        self.assertEqual(active_tab, competitions_tab_name, msg=f'"{competitions_tab_name}" tab is not active, '
                                                                f'active is "{active_tab}"')

        self.__class__.basketball = self.site.basketball.tab_content
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
            first_accordian = list(initial_sections.values())[0]
            self.assertTrue(initial_sections,
                            msg=f'No Initial sections found on "{competitions_tab_name}" tab')
            self.assertTrue(first_accordian.is_expanded(),
                            msg='First accordian is not expanded by default')

        else:
            self.assertTrue(self.basketball.has_no_events_label(), msg='No events label is not shown')
            initial_sections = {}

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

        if self.brand == 'bma':
            basketball_name_to_replace = 'BASKETBALL '
            expected_az_class_names = [name.upper() for name in expected_az_class_names]
            expected_initial_class_names = [name.upper() for name in expected_initial_class_names]
        else:
            basketball_name_to_replace = 'Basketball '
        # if self.brand == "ladbrokes":
        #     expected_az_class_names = [name.replace(basketball_name_to_replace, '') for name in expected_az_class_names]
        #     expected_initial_class_names = [name.replace(basketball_name_to_replace, '') for name in
        #                                     expected_initial_class_names]
        # else:
        #     expected_az_class_names = [name for name in expected_az_class_names]
        #     expected_initial_class_names = [name for name in
        #                                     expected_initial_class_names]

        expected_az_class_names = list(set(expected_az_class_names))
        expected_initial_class_names = list(set(expected_initial_class_names))

        self.assertListEqual(sorted(expected_az_class_names), sorted(self.sections),
                             msg=f'Expected classes {sorted(expected_az_class_names)} in A-Z part '
                                 f'are not the same as on ui {sorted(self.sections)}')
        self.assertListEqual(sorted(expected_initial_class_names), sorted(initial_sections),
                             msg=f'Expected classes {sorted(expected_initial_class_names)} in initial part '
                                 f'are not the same as on ui {sorted(initial_sections)}')

    def test_004_verify_navigation_between_popular_and_a_z_switchers(self):
        """
        DESCRIPTION: Verify navigation between 'Popular' and 'A-Z' switchers
        EXPECTED: * The User must be able to select 'Popular' and 'A-Z' switchers
        EXPECTED: * Selected switcher is highlighted by red line
        EXPECTED: * If user selects 'Popular'/'A-Z' switcher they will be redirected to 'Popular'/'A-Z' page
        """
        # covered in step 3

    def test_005_verify_content_of_page_when_popular_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'Popular' switcher is selected
        EXPECTED: * List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: * The first Classes accordion is expanded by default the rest are collapsed
        EXPECTED: * All Classes accordion are collapsible/expandable
        EXPECTED: * The sub-categories (Classes) accordions are ordered according to settings in the CMS
        EXPECTED: * The leagues (Types) are displayed in Horizontal position within expanded Classes accordion
        EXPECTED: * The leagues (Types) are ordered by OpenBet display order
        """
        # covered in step 3

    def test_006_verify_content_of_page_when_a_z_switcher_is_selected(self):
        """
        DESCRIPTION: Verify content of page when 'A-Z' switcher is selected
        EXPECTED: * List of sub-categories (Classes) is loaded according to set ID's in CMS
        EXPECTED: * The first Classes accordion is expanded by default the rest are collapsed
        EXPECTED: * All Classes accordion are collapsible/expandable
        EXPECTED: * The leagues (Types) are displayed in Horizontal position within expanded Classes accordion
        EXPECTED: * The sub-categories (Classes) accordion are displayed in Alphabetical order
        EXPECTED: * The leagues (Types) are ordered by OpenBet display order
        """
        type_order_list = []
        grouping_buttons = self.basketball.grouping_buttons
        self.assertTrue(grouping_buttons.items_as_ordered_dict[vec.sb_desktop.COMPETITIONS_SPORTS].is_selected(),
                        msg='"A-Z" switcher is not not selected and highlighted')
        a_z_firstsection = list(self.basketball.accordions_list.items_as_ordered_dict.values())[0]
        self.assertTrue(a_z_firstsection, msg='No A-Z sections found on competitons tab')
        self.assertTrue(a_z_firstsection.is_expanded(),
                        msg=f'The First accordion is not expanded by default')
        # Sort the accordion keys alphabetically, excluding the unwanted string
        accordion_keys_sorted = sorted(key for key in self.basketball.accordions_list.items_as_ordered_dict.keys())
        # Assert that the sorted accordion keys match the sorted self.sections list
        self.assertListEqual(accordion_keys_sorted, sorted(self.sections),
                             msg='"A-Z" class accordions are not ordered alphabetically')
        section = self.basketball.accordions_list.items_as_ordered_dict[self.section_name_list]
        self.assertTrue(section, msg=f'Competitions page does not have any "{self.section_name_list}" section')
        section.expand()
        order = [item.upper() if self.brand == 'bma' else item for item in list(section.items_as_ordered_dict.keys())]
        for item in self.expected_leagues_order_upper:
            if self.section_name_list in item and item != 'Featured Autotest League':
                type_order_list.append(item.split("-")[1].strip())
        self.assertEqual(order, type_order_list,
                         msg=f'Type IDs "{order}"are not ordered by OpenBet display order "{type_order_list}" (lowest display order at the top)')

    def test_007_verify_content_of_page_when_populara_z_switcher_is_selected_and_there_are_no_available_events(self):
        """
        DESCRIPTION: Verify content of page when 'Popular'/'A-Z' switcher is selected and there are no available events
        EXPECTED: "No events found" is displayed in case there are no available events on 'Popular'/'A-Z' pages
        """
        # cannot verify this steps as events are always present
