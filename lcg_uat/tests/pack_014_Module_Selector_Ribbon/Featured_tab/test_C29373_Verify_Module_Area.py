import pytest
from faker import Faker

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.helpers import normalize_name
import voltron.environments.constants as vec


# @pytest.mark.prod cannot test Featured on prod endpoints
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.featured
@pytest.mark.module_ribbon
@pytest.mark.desktop
@pytest.mark.medium
@vtest
class test_C29373_Verify_Module_Area(BaseFeaturedTest):
    """
    TR_ID: C29373
    NAME: Verify Module Area
    DESCRIPTION: This test case verifies Module area on the Feature tab (mobile/tablet) Featured section (desktop)
    PRECONDITIONS: 1. There are more than one event in the module section
    PRECONDITIONS: 2. Oxygen application is loaded on Mobile/Tablet device or Desktop
    PRECONDITIONS: **NOTE:** For creating modules use CMS (https://coral-cms-<endpoint>.symphony-solutions.eu) -> 'Featured Tab Modules' -> 'Create Featured Tab Module'
    """
    keep_browser_open = True
    expected_footer_text = None
    fake = Faker()

    @staticmethod
    def set_module_index(modules: dict, module_name: str) -> int:
        """
        Set module displayed order index
        :param modules: All displayed modules
        :param module_name: Expected module name
        :return: Displayed order index, -1 if module not found
        """
        for i, (name, module) in enumerate(modules.items()):
            if module_name.upper() in name.upper():
                return i
        return -1

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create featured tested module
        """
        custom_title = self.fake.city()
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.event_name = normalize_name(event['event']['name'])
            type_id = event['event']['typeId']
        else:
            type_id = self.ob_config.football_config.autotest_class.featured_autotest_league.type_id
            start_time = self.get_date_time_formatted_string(hours=3)
            event_params = self.ob_config.add_football_event_to_featured_autotest_league(start_time=start_time)
            self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'

        self.__class__.module_name = self.cms_config.add_featured_tab_module(
            select_event_by='Type', id=type_id, title=custom_title, show_expanded=True)['title'].upper()

        self.__class__.is_mobile = self.device_type == 'mobile'
        text = f'footer text for {custom_title}'
        self.__class__.expected_footer_text = text if self.is_mobile else text.upper()
        self.site.wait_content_state('HomePage')
        self.wait_for_featured_module(name=self.module_name)

    def test_001_scroll_the_homepage_to_the_module_ribbon_tabs_section(self):
        """
        DESCRIPTION: Scroll the Homepage to the 'Module Ribbon Tabs' section
        EXPECTED: For mobile/tablet:
        EXPECTED:  * 'Featured' tab is selected by default in the 'Module Ribbon Tabs' section
        EXPECTED: For desktop:
        EXPECTED:  * Module Ribbon Tabs are transformed into sections displayed in the following order:
        EXPECTED:     1) Enhanced multiples carousel
        EXPECTED:     2) In-Play & Live Stream
        EXPECTED:     3) Next Races Carousel
        EXPECTED:     4) Featured area
        """
        home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        if self.is_mobile:
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(current_tab, home_featured_tab_name,
                             msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                                 f'expected: "{home_featured_tab_name}"')
            featured_module_content = self.site.home.get_module_content(home_featured_tab_name)
            self.__class__.featured_modules = featured_module_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.featured_modules, msg='No one FEATURED module found')
        else:
            home_page_modules = self.site.home.desktop_modules.items_as_ordered_dict
            home_inplay_live_stream_tab_name = vec.inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME  # it is hardcoded for Desktop
            home_next_races_tab_name = self.get_ribbon_tab_name(internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races,
                                                                raise_exceptions=False)
            home_enhanced_tab_name = self.get_ribbon_tab_name(internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.multiples,
                                                              raise_exceptions=False)
            self.assertTrue(home_page_modules, msg='No one module found on Home Page')
            enhanced_index = self.set_module_index(home_page_modules, home_enhanced_tab_name)
            in_play_live_stream_index = self.set_module_index(home_page_modules, home_inplay_live_stream_tab_name)
            next_races_index = self.set_module_index(home_page_modules, home_next_races_tab_name)
            featured_index = self.set_module_index(home_page_modules, home_featured_tab_name)
            self.assertLessEqual(enhanced_index, in_play_live_stream_index,
                                 msg=f'"{home_inplay_live_stream_tab_name}" '
                                     f'module displayed before: "{home_enhanced_tab_name}"')
            self.assertLessEqual(in_play_live_stream_index, next_races_index,
                                 msg=f'"{home_next_races_tab_name}" '
                                     f'module displayed before: '
                                     f'"{home_inplay_live_stream_tab_name}"')
            self.assertLessEqual(next_races_index, featured_index,
                                 msg=f'"{home_featured_tab_name}" '
                                     f'module displayed before: "{home_next_races_tab_name}"')
            featured_section = home_page_modules.get(home_featured_tab_name)
            self.assertTrue(featured_section, msg='FEATURED section not found')
            self.__class__.featured_modules = featured_section.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(self.featured_modules, msg='No one FEATURED module found')

    def test_002_verify_module_area(self):
        """
        DESCRIPTION: Verify 'Module Area'
        EXPECTED: 'Module Area' contains **Modules**
        """
        self.__class__.test_module = self.featured_modules.get(self.module_name)
        self.assertTrue(self.test_module, msg=f'Featured module: "{self.module_name}" '
                                              f'not found among modules "{self.featured_modules.keys()}"')
        self.assertTrue(self.test_module.is_expanded(),
                        msg=f'Module: "{self.module_name}" not expanded')

    def test_003_verify_collapsing_expanding_of_module_header_using_down_chevron(self):
        """
        DESCRIPTION: Verify collapsing/expanding of Module header using 'Down' chevron
        EXPECTED: *   It is possible to expand the Module section using 'Down' chevrons
        EXPECTED: *   No chevron is displayed if the section is expanded
        EXPECTED: *   'Down' chevron is displayed if the section is collapsed
        """
        self.test_module.collapse()
        self.assertFalse(self.test_module.is_expanded(expected_result=False),
                         msg=f'Module: "{self.module_name}" not collapsed')
        if not self.brand == 'ladbrokes':
            self.assertTrue(self.test_module.is_chevron_down(),
                            msg='Chevron arrow is not in collapsed state (facing the bottom)')
            self.test_module.chevron_arrow.click()
            self.assertTrue(self.test_module.is_expanded(timeout=2),
                            msg=f'Module: "{self.module_name}" not expanded')
            self.assertFalse(self.test_module.is_chevron_down(),
                             msg='Chevron arrow is shown')

    def test_004_verify_collapsing_expanding_by_tapping_clicking_on_any_part_of_the_module_header(self):
        """
        DESCRIPTION: Verify collapsing/expanding by tapping/clicking on any part of the Module header
        EXPECTED: *   It is possible to collapse/expand Module section by tapping/clicking on any part of the Module header
        EXPECTED: *   No chevron is displayed if the section is expanded
        EXPECTED: *   'Down' chevron is displayed if the section is collapsed
        """
        if not self.brand == 'ladbrokes':
            self.test_module.collapse()
            self.assertFalse(self.test_module.is_expanded(expected_result=False),
                             msg=f'Module: "{self.module_name}" not collapsed')
            self.assertTrue(self.test_module.is_chevron_down(),
                            msg='Chevron arrow is not in collapsed state (facing the bottom)')
            self.test_module.expand()
            self.assertTrue(self.test_module.is_expanded(),
                            msg=f'Module: "{self.module_name}" not expanded')
            self.assertFalse(self.test_module.is_chevron_down(),
                             msg='Chevron arrow is shown')
