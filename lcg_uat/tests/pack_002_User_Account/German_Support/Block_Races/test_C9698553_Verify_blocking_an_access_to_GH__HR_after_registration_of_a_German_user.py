import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.lad_tst2  # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_hl
# # @pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C9698553_Verify_blocking_an_access_to_GH__HR_after_registration_of_a_German_user(BaseFeaturedTest):
    """
    TR_ID: C9698553
    NAME: Verify blocking an access to GH & HR after registration of a German user
    DESCRIPTION: This test case verifies whether just registered German user doesn't have access to Greyhound (GH) and Horse Racing (HR)
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Horse Racing/Greyhounds/International Totes is configured in CMS for:
        DESCRIPTION: - Sport Pages > Sport Categories > Horse Racing/Greyhounds/International Totes > General Sport Configuration:  "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: - Menus > Header Menus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: - Header SubMenus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: 2. Ensure that there are GH, International Totes, and HR Featured with different 'Select Events by' drop-down items available:
        DESCRIPTION: * EventsModule  (CMS > Featured Tab Modules > Active Featured Modules)
        DESCRIPTION: * SurfaceBetModule (CMS > Main Navigation > Homepage > Surface Bet Module > Active Surface Bets)
        DESCRIPTION: 3. Featured with categoryId in (19, 21, 161) are not displayed for german users (Console > Network > WS > find '?EIO=3&transport=websoket' > Frames > 42/0,["FEATURED_STRUCTURE_CHANGED",…]
        DESCRIPTION: 4. devtool > Application tab > Local Storage >  is cleared (so no "OX.countryCode" is available)
        DESCRIPTION: 5. Login pop-up is opened on mobile
        """
        sport_categories_list = self.cms_config.get_sport_categories()
        for sport in sport_categories_list:
            if any((race_sport == sport['imageTitle'] for race_sport in
                    ('Horse Racing', 'Greyhounds', 'International Totes'))):
                if not sport['showInAZ']:
                    raise CmsClientException(f'"Show in AZ" is not enabled in CMS for "{sport["imageTitle"]}"')
                if not sport['isTopSport']:
                    raise CmsClientException(f'"Is Top Sport" is not enabled in CMS for "{sport["imageTitle"]}"')
                if not sport['showInHome']:
                    raise CmsClientException(f'"Show in home" is not enabled in CMS for "{sport["imageTitle"]}"')

        event_list = ['Horse Racing', 'Greyhounds', 'International Totes']

        # Header
        cms_header_menu_items = self.cms_config.get_cms_header_menu_items()
        # Not all events are present in CMS
        result = all(ele in event_list for ele in cms_header_menu_items)
        if not result:
            CmsClientException('CMS Header does not have Horse Racing or Greyhound or International Totes')

        for sport in cms_header_menu_items:
            if ('Horse Racing' or 'Greyhound' or 'International Totes') in sport['linkTitle']:
                self.assertTrue(sport['targetUri'] != "",
                                msg=f'"{sport["targetUri"]}" targetUri is not configured in CMS')

        # Submenu
        cms_header_submenu_items = self.cms_config.get_header_submenus()
        # Not all events are present in CMS
        result = all(ele in event_list for ele in cms_header_submenu_items)
        if not result:
            CmsClientException('CMS Header Sub menu does not have Horse Racing or Greyhound or International Totes')

        for sport in cms_header_submenu_items:
            if ('Horse Racing' or 'Greyhound' or 'International Totes') in sport['linkTitle']:
                self.assertTrue(sport['targetUri'] != "",
                                msg=f'"{sport["targetUri"]}" targetUri is not configured in CMS')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(
                category_id=self.ob_config.backend.ti.greyhound_racing.category_id)[0]
            self.__class__.type_id_GH = event['event']['typeId']

            event = self.get_active_events_for_category(
                category_id=self.ob_config.backend.ti.horse_racing.category_id)[0]
            self.__class__.type_id_HR = event['event']['typeId']
        else:
            self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2)
            self.__class__.type_id_GH = self.ob_config.backend.ti.greyhound_racing.greyhounds_live.autotest.type_id
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
            self.__class__.sections = self.site.home.get_module_content(
                module_name=self.home_featured_tab_name).accordions_list.items_as_ordered_dict
            self.assertTrue(self.sections,
                            msg=f'Section "{self.module_name_HR, self.module_name_GH}" is not found on Featured tab in sections list')
        else:
            home_page_modules1 = self.site.home.get_module_content(vec.racing.RACING_FEATURED_TAB_NAME)
            self.assertTrue(home_page_modules1, msg='No module found on Home Page')
            featured_section = home_page_modules1.accordions_list.items_as_ordered_dict
            self.assertTrue(featured_section,
                            msg=f'Section "{self.module_name_HR, self.module_name_GH}" is not found on Featured tab in section list')

    def test_001__tap_join_now_fill_in_all_necessary_fields_to_register_user_select_country_germany_tap_open_account_save_my_preferences_close_deposit_page(
            self):
        """
        DESCRIPTION: * Tap 'Join now'
        DESCRIPTION: * Fill in all necessary fields to register user
        DESCRIPTION: * **Select Country 'Germany'**
        DESCRIPTION: * Tap 'Open account', 'Save my preferences'
        DESCRIPTION: * Close Deposit page
        EXPECTED: * German user is navigated back to an app
        EXPECTED: * German user is logged in with registered credentials
        EXPECTED: * German user is navigated to Home page
        """
        self.site.register_new_user(country='Germany', state='Hamburg', post_code='60306', city='Hamburg',
                                    currency='EUR')

    def test_002_verify_availability_of_horse_racing_greyhounds__international_tote_inmobilesports_menu_ribbondesktopheader_and_subheader_menus(
            self):
        """
        DESCRIPTION: Verify availability of 'Horse Racing', 'Greyhounds' & 'International Tote' in:
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Sports Menu Ribbon
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Header and subheader menus
        EXPECTED: 'Horse Racing', 'Greyhounds' & 'International Tote' are NOT available
        """
        if self.device_type in ['mobile', 'tablet']:
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='Sports Menu Ribbon does not have any items')
            self.assertNotIn(vec.sb.HORSERACING, all_items, msg='Horse Racing is present in Sports Menu Ribbon')
            self.assertNotIn(vec.sb.GREYHOUND, all_items, msg='Greyhounds is present in Sports Menu Ribbon')
            self.assertNotIn(vec.tote.TOTE_TITLE.title(), all_items,
                             msg='International Tote is present in Sports Menu Ribbon')
        else:
            # Header menu
            sports = self.site.header.top_menu.items_as_ordered_dict
            self.assertTrue(sports, msg='Header menu has no items')
            self.assertNotIn(vec.sb.HORSERACING.upper(), sports,
                             msg='Horse Racing is present in Sports Menu Ribbon')
            self.assertNotIn(vec.sb.GREYHOUND.upper(), sports, msg='Greyhounds is present in Sports Menu Ribbon')
            self.assertNotIn(vec.tote.TOTE_TITLE.upper(), sports,
                             msg='International Tote is present in Sports Menu Ribbon')
            # Header sub menu
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(sports, msg='Header sub menu has no items')
            self.assertNotIn(vec.sb.HORSERACING.upper(), sports, msg='Horse Racing is present in subheader Menu ')
            self.assertNotIn(vec.sb.GREYHOUND.upper(), sports, msg='Greyhounds is present in subheader Menu')
            self.assertNotIn(vec.tote.TOTE_TITLE.upper(), sports,
                             msg='International Tote is present in subheader Menu')

    def test_003_verify_availability_of_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Verify availability of 'Next Races' tab on Home page
        EXPECTED: 'Next Races' tab is NOT available
        """
        if self.device_type in ['mobile', 'tablet']:
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(tabs, msg='Tabs on home page are not found')
            self.assertNotIn(vec.racing.RACING_NEXT_RACES_NAME, tabs, msg='Next Races tab is available')
        else:
            sections = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(sections, msg='No tab sections on Home page')
            self.assertNotIn(vec.racing.RACING_NEXT_RACES_NAME, sections, msg='Next Races tab is available')

    def test_004_verify_availability_of_ghhr_in_featured_tab_on_home_page(self):
        """
        DESCRIPTION: Verify availability of GH/HR in Featured tab on Home page
        EXPECTED: GH/HR is NOT available in Featured tab
        """
        if self.device_type in ['mobile', 'tablet']:
            self.__class__.home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(current_tab, self.home_featured_tab_name,
                             msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                             f'expected: "{self.home_featured_tab_name}"')
            featured_module_content = self.site.home.get_module_content(self.home_featured_tab_name)
            featured_modules = featured_module_content.accordions_list.items_as_ordered_dict
            self.softAssert(self.assertNotIn, self.module_name_HR, featured_modules,
                            msg=f'"{self.module_name_HR}" Horse Race is found in Featured module')
            self.softAssert(self.assertNotIn, self.module_name_GH, featured_modules,
                            msg=f'"{self.module_name_GH}" Greyhounds is found in Featured module')
        else:
            self.site.contents.scroll_to_bottom()
            home_page_modules = self.site.home.get_module_content(vec.racing.RACING_FEATURED_TAB_NAME)
            self.assertTrue(home_page_modules, msg='No module found on Home Page')
            featured_section = home_page_modules.accordions_list.items_as_ordered_dict
            self.softAssert(self.assertNotIn, self.module_name_HR, featured_section,
                            msg=f'"{self.module_name_HR}" Horse Race is found in Featured module')
            self.softAssert(self.assertNotIn, self.module_name_GH, featured_section,
                            msg=f'"{self.module_name_GH}" Greyhounds is found in Featured module')

    def test_005_open_in_play_pagemobiletablettap_in_play_icon_on_the_sports_menu_ribbon_on_the_homepagedesktopclick_in_play_icon_on_the_header_menussubheader_menus(
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
        if self.device_type in ['mobile', 'tablet']:
            self.site.home.menu_carousel.click_item(vec.sb.IN_PLAY)
            self.site.wait_content_state(vec.sb.IN_PLAY)
            menu_items = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No Sports Menu Ribbon in "In-play"')
            self.assertNotIn(vec.sb.HORSERACING, menu_items, msg='Horse Race is present in Header menu')
            self.assertNotIn(vec.sb.GREYHOUND, menu_items, msg='Greyhounds is present in Header menu')
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No menu items on Home page')
            in_play_tab = menu_items[vec.sb.IN_PLAY.upper()]
            in_play_tab.click()
            self.site.wait_content_state(vec.sb.IN_PLAY)
            list_l = self.site.inplay.inplay_sport_menu.items_as_ordered_dict
            self.assertTrue(list_l, msg='No Header Menus/SubHeader Menus in "In-Play"')
            self.assertNotIn(vec.sb.HORSERACING, list_l,
                             msg='Horse Race is present in Header Menus/SubHeader Menus')
            self.assertNotIn(vec.sb.GREYHOUND, list_l,
                             msg='Greyhounds is present in Header Menus/SubHeader Menus')

    def test_006_mobiletablet_open_in_play_module_on_the_featured_tab_desktop_click_upcoming_tab_in_in_play_module(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        DESCRIPTION: **Desktop: **
        DESCRIPTION: Click 'Upcoming' tab in 'In-Play' module
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        self.navigate_to_page(name='/')
        if self.device_type in ['mobile', 'tablet']:
            modules_inplay = self.site.home.get_module_content(
                module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play)
            ).accordions_list.items_as_ordered_dict
            self.assertNotIn(vec.sb.HORSERACING, modules_inplay,
                             msg='Horse Racing available in In-Play on featured tab')
            self.assertNotIn(vec.sb.GREYHOUND, modules_inplay,
                             msg='Grey Hound is available in In-Play on featured tab')
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No menu items on Home page')
            in_play_tab = menu_items[vec.sb.IN_PLAY.upper()]
            in_play_tab.click()
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            upcoming = self.site.inplay.tab_content.upcoming
            if not upcoming:
                self._logger.info('*** No events found in Upcoming tab')
            else:
                upcoming_list = upcoming.items_as_ordered_dict
                if not upcoming_list:
                    self._logger.info('*** No events found in Upcoming tab')
                else:
                    self.assertNotIn(vec.sb.HORSERACING, upcoming_list,
                                     msg='Horse Racing is present in Upcoming tab')
                    self.assertNotIn(vec.sb.GREYHOUND, upcoming_list,
                                     msg='Greyhounds is present in Upcoming tab')

    def test_007_mobiletabletopen_in_play_tab_on_the_homepagedesktopfind_in_play_and_live_stream_tab_on_the_homepage(self):
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
        # For mobile: Done in scope of 5
        if self.device_type not in ['mobile', 'tablet']:
            self.navigate_to_page(name='/')
            home_module_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            self.assertTrue(home_module_items, msg='No items "In-play and live stream" tab on the Homepage')
            self.assertNotIn(vec.sb.HORSERACING, home_module_items,
                             msg='Horse Racing is present in In-play and live stream')
            self.assertNotIn(vec.sb.GREYHOUND, home_module_items,
                             msg='Greyhounds is present in In-play and live stream')

    def test_008_mobiletabletfooter_menu__menu_item__tap_on_in_playdesktophomepage__a_z_sports_left_hand_menu__in_play(
            self):
        """
        DESCRIPTION: **Mobile/Tablet**
        DESCRIPTION: Footer menu > 'Menu' item > Tap on ‘In Play’
        DESCRIPTION: **Desktop**
        DESCRIPTION: Homepage > 'A-Z sports' left-hand menu > 'In-Play'
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        if self.device_type in ['mobile', 'tablet']:
            item = self.site.navigation_menu.items_as_ordered_dict
            self.assertTrue(item, msg='No items in Footer menu')
            menu_item = item.get(vec.sb.MENU_FOOTER_ITEM, None)
            self.assertTrue(menu_item, msg=f'No {vec.sb.MENU_FOOTER_ITEM} in Footer menu items "{item.keys()}"')
            menu_item.click()
            self.site.all_sports.click_item(vec.sb.IN_PLAY)
            events_in_play = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(events_in_play, msg='No items in "In-Play"')
            self.assertNotIn(vec.sb.HORSERACING, events_in_play,
                             msg='Horse Race is present in Footer menu>In-Play')
            self.assertNotIn(vec.sb.GREYHOUND, events_in_play,
                             msg='Greyhounds is present in Footer menu>In-Play')
        else:
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(sports, msg='No items in "Homepage > A-Z sports left-hand menu"')
            sports.get(vec.sb.IN_PLAY).click()
            events_in_play = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(events_in_play, msg='No items in "In-Play"')
            self.assertNotIn(vec.sb.HORSERACING, events_in_play,
                             msg='Horse Race is present in A-Z sports left-hand menu>In-Play')
            self.assertNotIn(vec.sb.GREYHOUND, events_in_play,
                             msg='Greyhounds is present in A-Z sports left-hand menu>In-Play')
