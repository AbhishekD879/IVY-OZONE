import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


# @pytest.mark.lad_tst2  # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_hl
# # @pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.homepage_featured
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9647797_Verify_blocking_of_access_to_GH__HR_for_Featured_page_widget(BaseRacing, BaseFeaturedTest):
    """
    TR_ID: C9647797
    NAME: Verify blocking of access to GH & HR for Featured page/widget
    """
    keep_browser_open = True
    type_id_HR = None
    type_id_GH = None
    module_name = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: This test case verifies that German user doesn't have access to Greyhound (GH) and Horse Racing (HR) in Featured page/widget
        PRECONDITIONS: 1. Ensure that there are GH, International Totes, and HR Featured with different 'Select Events by' drop-down items is configured in CMS:
        PRECONDITIONS: * EventsModule  (CMS > Featured Tab Modules > Active Featured Modules)
        PRECONDITIONS: * SurfaceBetModule (CMS > Main Navigation > Homepage > Surface Bet Module > Active Surface Bets)
        PRECONDITIONS: 2. Featured with categoryId in (19, 21, 161) are not displayed for german users  (Console > Network > WS > find '?EIO=3&transport=websoket' > Frames > 42/0,["FEATURED_STRUCTURE_CHANGED",…]
        PRECONDITIONS: 3. German user is logged in
        """
        # creating HR/GH Featured tab module
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.backend.ti.greyhound_racing.category_id)[0]
            self.__class__.type_id_GH = event['event']['typeId']

            event = self.get_active_events_for_category(
                category_id=self.ob_config.backend.ti.horse_racing.category_id)[0]
            self.__class__.type_id_HR = event['event']['typeId']
        else:
            event_params = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2)
            self.__class__.type_id_GH = self.ob_config.backend.ti.greyhound_racing.greyhounds_live.autotest.type_id
            self.__class__.eventID = event_params.event_id
            self.__class__.name_pattern = self.greyhound_autotest_name_pattern

            self.ob_config.add_UK_racing_event(number_of_runners=1)
            self.__class__.type_id_HR = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        self.__class__.module_name_GH = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=self.type_id_GH, show_expanded=True)['title'].upper()

        self.__class__.module_name_HR = self.cms_config.add_featured_tab_module(
            select_event_by='RaceTypeId', id=self.type_id_HR)['title'].upper()

        self.site.wait_content_state(state_name='Homepage')
        self.wait_for_featured_module(name=self.module_name_GH)
        self.wait_for_featured_module(name=self.module_name_HR)
        self.__class__.home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        if self.device_type == 'mobile':
            self.__class__.sections = self.site.home.get_module_content(module_name=self.home_featured_tab_name).accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections, msg=f'Section "{self.module_name_HR, self.module_name_GH}" is not found on Featured tab in sections list')
        else:
            home_page_modules1 = self.site.home.get_module_content(vec.racing.RACING_FEATURED_TAB_NAME)
            self.assertTrue(home_page_modules1, msg='No module found on Home Page')
            featured_section = home_page_modules1.accordions_list.items_as_ordered_dict
            self.assertTrue(featured_section, msg=f'Section "{self.module_name_HR, self.module_name_GH}" is not found on Featured tab in section list')
        self.site.login(username=tests.settings.german_betplacement_user)

    def test_001_open_featured_section_for_mobiletabletthe_featured_tab_is_opened_by_default_on_the_homepagefor_desktopscroll_down_the_homepage_to_find_featured(self):
        """
        DESCRIPTION: Open 'Featured' section :
        DESCRIPTION: **For Mobile/Tablet: **
        DESCRIPTION: The 'Featured' tab is opened by default on the Homepage
        DESCRIPTION: **For Desktop: **
        DESCRIPTION: Scroll down the homepage to find Featured
        EXPECTED: * The section is displayed
        EXPECTED: * GH and HR are not available in any of Featured Modules
        """
        if self.device_type in ['mobile', 'tablet']:
            self.__class__.home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(current_tab, self.home_featured_tab_name,
                             msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                                 f'expected: "{self.home_featured_tab_name}"')
            featured_module_content = self.site.home.get_module_content(self.home_featured_tab_name)
            featured_modules = featured_module_content.accordions_list.items_as_ordered_dict
            self.assertNotIn(self.module_name_HR, featured_modules, msg=f'"{self.module_name_HR}" Featured module found')
            self.assertNotIn(self.module_name_GH, featured_modules, msg=f'"{self.module_name_HR}" Featured module found')
        else:
            self.site.contents.scroll_to_bottom()
            home_page_modules1 = self.site.home.get_module_content(vec.racing.RACING_FEATURED_TAB_NAME)
            self.assertTrue(home_page_modules1, msg='No module found on Home Page')
            featured_section = home_page_modules1.accordions_list.items_as_ordered_dict
            self.assertNotIn(self.module_name_HR, featured_section,
                             msg=f'"{self.module_name_HR}" Featured module found')
            self.assertNotIn(self.module_name_GH, featured_section,
                             msg=f'"{self.module_name_HR}" Featured module found')
