import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_006_In_Play.In_Play_page.Sports_Menu_Ribbon.BaseSportsMenuRibbonTest import BaseSportsMenuRibbonTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import get_in_play_module_from_ws


# @pytest.mark.lad_tst2  # due to VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C9647727_Verify_blocking_of_access_to_GH__HR_for_In_play_page_widget(BaseSportsMenuRibbonTest):
    """
    TR_ID: C9647727
    NAME: Verify blocking of access to GH & HR for In-play page/widget
    DESCRIPTION: This test case verifies that German user doesn't have access to Greyhound (GH) and Horse Racing (HR) in In-play tab/module
    """
    keep_browser_open = True
    horseracing_events, greyhound_events = [], []

    def test_000_preconditions(self):
        """
        DESCRIPTION: * 'In-Play' module should be enabled in CMS > System configuration > Structure > In-Play module
        DESCRIPTION: * 'In-Play' module should be 'Active' in CMS > Sports Pages > Homepage > In-Play module
        DESCRIPTION: * Some positive value should to be set for 'In-Play Event Count' in CMS > Sports Pages > Homepage > In-Play module
        DESCRIPTION: * 'In-Play' module configuration to display module in needed menus:
        DESCRIPTION: CMS > Sport Pages > Sport Categories > Find 'In-Play' > General Sport Configuration > Check off needed areas (e.g., 'Show in Sports Ribbon') OR
        DESCRIPTION: CMS > Menus > Create menu in Menu (e.g., Header Menus > Create Header Menu > Fill in 'Link Title' with ''In-Play'' and 'Target Uri' with 'in-play' > Save)
        DESCRIPTION: * 'Show In Play' should be checked off for HR and GH, to show these sports events in In-play: CMS > Sports Pages > Sports Categories > Tap needed category (e.g., Horse Racing) > tap 'General Sport Configuration' > Tick 'Show In Play' check-box > Save changes (https://confluence.egalacoral.com/display/SPI/Sportsbook+Configuration+Guide)
        DESCRIPTION: ____________
        DESCRIPTION: * Ensure that there are GH and HR available for not German user in In-play page/widget.
        DESCRIPTION: * German user is logged in
        DESCRIPTION: NOTE:
        DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
        DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
        DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.horseracing_events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                                                    in_play_event=True, raise_exceptions=False)

            self.__class__.greyhound_events = self.get_active_events_for_category(category_id=self.ob_config.greyhound_racing_config.category_id,
                                                                                  in_play_event=True, raise_exceptions=False)
            if not self.greyhound_events and not self.horseracing_events:
                raise SiteServeException('No Live Greyhounds/Horseracing events are found for test')
        else:
            self.__class__.horseracing_events.append(self.ob_config.add_UK_racing_event(number_of_runners=1, is_live=True).event_id)
            self.__class__.greyhound_events.append(self.ob_config.add_UK_greyhound_racing_event(number_of_runners=1, is_live=True).event_id)

        self.site.login(username=tests.settings.german_betplacement_user, async_close_dialogs=False)
        if self.device_type == 'mobile' and not get_in_play_module_from_ws():
            raise CmsClientException('"In play" for featured is disabled in CMS')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_001_mobile_tablet_in_play_icon_on_the_sports_menu_ribbon_desktop_in_play_icon_on_the_header_menussubheader_menus(
            self):
        """
        DESCRIPTION: Open 'In-Play' Page:
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon on the homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'In-Play' icon on the Header Menus/SubHeader Menus
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        in_play_tab_name = self.get_sport_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play)
        if self.device_type == 'desktop':
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='Header menu has no tabs')
            inplay_tab = menu_items.get(in_play_tab_name, None)
            self.assertTrue(inplay_tab, msg='No "In-Play" tab in Header menu')
            inplay_tab.click()
        else:
            self.site.open_sport(name=in_play_tab_name)

        self.site.wait_content_state(state_name='InPlay')
        in_play_sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(in_play_sports, msg='No sports found on "In-Play" tab')
        if self.horseracing_events:
            self.assertNotIn(vec.sb.HORSERACING, in_play_sports, msg='Horse Racing is shown in InPlay for German Users')
        if self.greyhound_events:
            self.assertNotIn(vec.sb.GREYHOUND, in_play_sports, msg='GreyHounds is shown in InPlay for German Users')

    def test_002_mobiletablet_open_in_play_module_on_the_featured_tabdesktopclick_upcoming_tab_in_in_play_module(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'Upcoming' tab in 'In-Play' module
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            upcoming_sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
            self.assertTrue(upcoming_sports, msg='No Sports found in Upcoming tab')
            if self.horseracing_events:
                self.assertNotIn(vec.sb.HORSERACING, upcoming_sports, msg='Horse Racing is present in Upcoming tab')
            if self.greyhound_events:
                self.assertNotIn(vec.sb.GREYHOUND, upcoming_sports, msg='Greyhounds is present in Upcoming tab')
        else:
            self.navigate_to_page(name='/')
            inplay_module_config = self.get_initial_data_system_configuration().get('Inplay Module', {})
            if not inplay_module_config:
                inplay_module_config = self.cms_config.get_system_configuration_item('Inplay Module')
            module_enabled = inplay_module_config.get('enabled')
            self.softAssert(self.assertTrue, module_enabled, msg='"In play Module" module is disabled in system config')
            self.softAssert(self.assertTrue, get_in_play_module_from_ws(),
                            msg='"In play" for Featured is disabled in CMS')

            self.navigate_to_page(name='Home Page')
            self.site.wait_content_state(state_name='Home page')
            in_play_module = self.site.home.tab_content.in_play_module
            in_play_module_items = in_play_module.items_as_ordered_dict
            self.assertTrue(in_play_module_items, msg='Cannot find any module items')
            if self.horseracing_events:
                self.assertNotIn(vec.sb.HORSERACING.upper(), in_play_module_items,
                                 msg='Horse Racing is shown in featured tab, In-play module for German Users')
            if self.greyhound_events:
                self.assertNotIn(vec.sb.GREYHOUND.upper(), in_play_module_items,
                                 msg='GreyHounds is shown in featured tab, In-play module for German Users')

    def test_003_mobiletablet_in_play_tab_homepage_desktop_in_play_and_live_stream_tab_on_the_homepage(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In-Play' tab on the Homepage
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Find 'In-play and live stream' tab on the Homepage.
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * 'View all in-play [racing]' button is not displayed
        EXPECTED: * All other sports but racing are available
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            self.site.wait_content_state('Homepage')
            home_module_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            self.assertTrue(home_module_items, msg='"In-play and live stream" items are not present on Homepage tab')
            if self.horseracing_events:
                self.assertNotIn(vec.sb.HORSERACING, home_module_items,
                                 msg='Horse Racing is present in "In-play and live stream" tab')
            if self.greyhound_events:
                self.assertNotIn(vec.sb.GREYHOUND, home_module_items,
                                 msg='Greyhounds is present in "In-play and live stream" tab')
        else:
            self.navigate_to_page(name='home/in-play')
            self.site.wait_content_state('Homepage')
            inplay_list_live = self.site.home.tab_content.live_now.items_as_ordered_dict.keys()
            inplay_list_upcoming = self.site.inplay.tab_content.upcoming.items_as_ordered_dict.keys()
            if self.horseracing_events:
                self.assertNotIn(vec.sb.HORSERACING.upper(), inplay_list_live,
                                 msg='Horse Race is present in HomePage, "In-Play > Live" tab for German user')
                self.assertNotIn(vec.sb.HORSERACING.upper(), inplay_list_upcoming,
                                 msg='Horse Race is present in HomePage, "In-Play > Upcoming" tab for German user')
            if self.greyhound_events:
                self.assertNotIn(vec.sb.GREYHOUND.upper(), inplay_list_live,
                                 msg='Greyhounds is present in HomePage, "In-Play > Live" tab for German user')
                self.assertNotIn(vec.sb.GREYHOUND.upper(), inplay_list_upcoming,
                                 msg='Greyhounds is present in HomePage, "In-Play > Upcoming" tab for German user')

    def test_004_mobile_Tablet_footer_in_play_desktop_a_z_sports_in_play(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Footer menu > 'Menu' item > Tap on 'In Play'
        DESCRIPTION: OR Sports Menu Ribbon > All sports > 'In Play'
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Homepage > 'A-Z sports' left-hand menu > 'In-Play'
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        if self.device_type == 'desktop':
            self.navigate_to_page(name='in-play')
            self.site.wait_content_state('IN-PLAY')
        else:
            footer_items = self.site.navigation_menu.items_as_ordered_dict
            self.assertTrue(footer_items, msg='No items in Footer menu')
            inplay_tab = footer_items.get(vec.sb.IN_PLAY_FOOTER_ITEM, None)
            self.assertTrue(inplay_tab,
                            msg=f'"{vec.sb.IN_PLAY_FOOTER_ITEM}" tab is not found in "{footer_items.keys()}"')
            inplay_tab.click()
            self.site.wait_content_state(state_name='InPlay')

        in_play_sports = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
        self.assertTrue(in_play_sports, msg='No sports found on "In-Play" tab')
        if self.horseracing_events:
            self.assertNotIn(vec.sb.HORSERACING, in_play_sports, msg='Horse Racing is shown in InPlay for German Users')
        if self.greyhound_events:
            self.assertNotIn(vec.sb.GREYHOUND, in_play_sports, msg='GreyHounds is shown in InPlay for German Users')

    def test_005_log_out__repeat_steps_1_4(self):
        """
        DESCRIPTION: Log out > Repeat steps 1-4
        """
        self.site.logout()
        self.test_001_mobile_tablet_in_play_icon_on_the_sports_menu_ribbon_desktop_in_play_icon_on_the_header_menussubheader_menus()
        self.test_002_mobiletablet_open_in_play_module_on_the_featured_tabdesktopclick_upcoming_tab_in_in_play_module()
        self.test_003_mobiletablet_in_play_tab_homepage_desktop_in_play_and_live_stream_tab_on_the_homepage()
        self.test_004_mobile_Tablet_footer_in_play_desktop_a_z_sports_in_play()
