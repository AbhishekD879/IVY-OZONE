import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.football
@pytest.mark.competitions
@vtest
class Test_C1158597_Verify_Competition_Quick_Links_functionality(BaseSportTest):
    """
    TR_ID: C1158597
    NAME: Verify Competition Quick Links functionality
    DESCRIPTION: This test case verifies Competition Quick Links functionality
    PRECONDITIONS: *Note:*
    PRECONDITIONS: Be aware that names of competitions (Premier League, Championship, La Liga, Bundesliga, League One)
                   are hardcoded and shouldn't be changed in OpenBet System for correct work on front-end.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    maximized_browser = True

    def sort_by_disp_order(self, sports_list: list):
        """
        :param sports_list: list of dict
        :return: sorted list by DisplayOrder otherwise sort by name
        """
        sports_list = [item for item in sports_list]
        sport_categories = {f"{sport['event']['className']} - {sport['event']['typeName']}":
                                int(sport['event']['typeDisplayOrder']) for sport in sports_list}
        return sorted(sport_categories, key=lambda k: (sport_categories[k], k))

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        self.navigate_to_page('sport/football')
        self.site.wait_content_state(state_name='Football')

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing page
        EXPECTED: Football Landing page is loaded
        """
        # covered in step one

    def test_003_click_on_competitions_tab(self):
        """
        DESCRIPTION: Click on 'Competitions' tab
        EXPECTED: Competitions page is opened with the following elements:
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        EXPECTED: * 'Popular' and 'A-Z' switchers are displayed below Sports Sub Tabs
        EXPECTED: * 'Popular' switcher is selected by default and highlighted
        EXPECTED: * Competitions are displayed in accordions
        """
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

        self.__class__.competitions_tab_name = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.competitions,
            self.ob_config.football_config.category_id)
        self.site.football.tabs_menu.click_button(self.competitions_tab_name.upper())
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.competitions_tab_name,
                         msg=f'"{self.competitions_tab_name}" tab is not active, '
                             f'active is "{active_tab}"')

        self.__class__.football = self.site.football.tab_content

        tabs_menu_location = self.site.football.tabs_menu.location.get('y')
        ql_location = self.football.quick_link_container.location.get('y')
        self.assertTrue(ql_location > tabs_menu_location, msg='Quick links are displayed above tabs')
        grouping_buttons = self.football.grouping_buttons
        expected_tab_name = vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME.upper() if self.brand == 'bma' else \
            vec.sb_desktop.POPULAR_COMPETITIONS_CATEGORIES_NAME
        self.assertEqual(grouping_buttons.current, expected_tab_name,
                         msg=f'"{expected_tab_name}" is not selected by default. '
                             f'Default is "{grouping_buttons.current}"')
        if cms_initial_class_ids:
            initial_sections = self.football.accordions_list.items_as_ordered_dict
            first_accordian = list(initial_sections.values())[0]
            self.assertTrue(initial_sections,
                            msg=f'No Initial sections found on "{self.competitions_tab_name}" tab')
            self.assertTrue(first_accordian.is_expanded(),
                            msg='First accordian is not expanded by default')

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

    def test_004_hover_the_mouse_over_the_competition_quick_link(self):
        """
        DESCRIPTION: Hover the mouse over the Competition Quick Link
        EXPECTED: * The background of the whole section is changing
        EXPECTED: * Pointer is changed view from 'Normal select' to 'Link select' for realizing the possibility
                    to click on particular area
        """
        expected_list = ['PREMIER LEAGUE', 'CHAMPIONSHIP', 'LA LIGA', 'BUNDESLIGA', 'LEAGUE ONE']
        self.__class__.quick_links = self.football.quick_links_wrapper.items_as_ordered_dict
        self.assertTrue(self.quick_links, msg='Quick links are not shown.')
        for link_name, link in list(self.quick_links.items()):
            self.assertIn(link_name.upper(), expected_list,
                          msg=f'Competition Quick link "{link_name.upper()}" is not in'
                              f'expected list "{expected_list}"')
            text_opacity_before = link.opacity_value
            link.mouse_over()
            self.assertEqual(text_opacity_before, '1', msg=f'Hover state is not activated')

    def test_005_click_on_any_competition_quick_link(self):
        """
        DESCRIPTION: Click on any Competition Quick Link
        EXPECTED: * User is redirected to particular Competitions Details page
        EXPECTED: * Respective data is displayed on the page
        """
        quick_link_1 = list(self.quick_links.values())[0]
        quick_link_1.click()
        title = self.site.contents.content_title_text
        expected_title = list(self.quick_links.keys())[0]
        if self.brand == 'ladbrokes':
            title = title.upper()
        self.assertEqual(title, expected_title,
                         msg=f'Actual title : "{title}" is not same as'
                             f'Expected title: "{expected_title}"')
        relevant_data = self.site.contents.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(relevant_data,
                        msg='Relevant data is not shown.')

    def test_006_click_on_the_back_button_on_competitions_header(self):
        """
        DESCRIPTION: Click on the 'Back' button on Competitions header
        EXPECTED: * User is redirected to Competitions Landing page
        EXPECTED: * Competition Quick Links are displayed below Sports Subtabs
        """
        self.site.contents.back_button_click()
        active_tab = self.site.football.tabs_menu.current
        self.assertEqual(active_tab, self.competitions_tab_name,
                         msg=f'"{self.competitions_tab_name}" tab is not active,'
                             f' active is "{active_tab}".')
        quick_links = self.site.football.tab_content.quick_links_wrapper.items_as_ordered_dict
        self.assertTrue(quick_links, msg='Quick links are not shown below Sports tab.')