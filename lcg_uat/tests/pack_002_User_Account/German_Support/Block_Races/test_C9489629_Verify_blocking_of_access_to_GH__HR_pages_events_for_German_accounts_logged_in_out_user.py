import pytest
from selenium.common.exceptions import StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException


# @pytest.mark.lad_tst2  # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_hl
# # @pytest.mark.lad_prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C9489629_Verify_blocking_of_access_to_GH__HR_pages_events_for_German_accounts_logged_in_out_user(BaseFeaturedTest):
    """
    TR_ID: C9489629
    NAME: Verify blocking of access to GH & HR pages/events for German accounts (logged-in/out user)
    DESCRIPTION: This test case verifies whether the German user doesn't have access to Greyhound (GH) and Horse Racing (HR) nevertheless he is a logged-in or logged-out user
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True
    name = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Horse Racing/Greyhounds/International Totes is configured in CMS for:
        DESCRIPTION: - Sport Pages > Sport Categories > Horse Racing/Greyhounds/International Totes: > General Sport Configuration:  "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: - Menus > Header Menus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: - Header SubMenus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: 2. Ensure that there are GH, International Totes, and HR Featured with different 'Select Events by' drop-down items available:
        DESCRIPTION: * EventsModule  (CMS > Featured Tab Modules > Active Featured Modules)
        DESCRIPTION: * SurfaceBetModule (CMS > Main Navigation > Homepage > Surface Bet Module > Active Surface Bets)
        DESCRIPTION: 4. devtool > Application tab > Local Storage >  is cleared (so no "OX.countryCode" is available)
        DESCRIPTION: 5. Login pop-up is opened on mobile
        """
        sport_categories_list = self.cms_config.get_sport_categories()
        for sport in sport_categories_list:
            if any((race_sport == sport['imageTitle'] for race_sport in ('Horse Racing', 'Greyhounds', 'International Totes'))):
                if not sport['showInAZ']:
                    raise CmsClientException(f'"Show in AZ" is not enabled in CMS for "{sport["imageTitle"]}"')
                if not sport['isTopSport']:
                    raise CmsClientException(f'"Is Top Sport" is not enabled in CMS for "{sport["imageTitle"]}"')
                if not sport['showInHome']:
                    raise CmsClientException(f'"Show in home" is not enabled in CMS for "{sport["imageTitle"]}"')

        event_list = ['Horse Racing', 'Greyhounds', 'International Totes']

        # Header
        cms_header_menu_items = self.cms_config.get_cms_header_menu_items()
        # Not all events are present in HL - CMS
        result = all(ele in event_list for ele in cms_header_menu_items)
        if not result:
            CmsClientException('CMS Header does not have Horse Racing or Greyhound or International Totes')

        for sport in cms_header_menu_items:
            if ('Horse Racing' or 'Greyhounds' or 'International Totes') in sport['linkTitle']:
                self.assertTrue(sport['targetUri'] != "",
                                msg=f'"{sport["targetUri"]}" targetUri is not configured in CMS')

        # Submenu
        cms_header_submenu_items = self.cms_config.get_header_submenus()
        # Not all events are present in HL-CMS
        result = all(ele in event_list for ele in cms_header_submenu_items)
        if not result:
            CmsClientException('CMS Header Sub menu does not have Horse Racing or Greyhound or International Totes')

        for sport in cms_header_submenu_items:
            if ('Horse Racing' or 'Greyhounds' or 'International Totes') in sport['linkTitle']:
                self.assertTrue(sport['targetUri'] != "",
                                msg=f'"{sport["targetUri"]}" targetUri is not configured in CMS')

        # creating HR/GH featured tab
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
            sections = self.site.home.get_module_content(
                module_name=self.home_featured_tab_name).accordions_list.items_as_ordered_dict
        else:
            home_page_modules = self.site.home.get_module_content(vec.racing.RACING_FEATURED_TAB_NAME)
            self.assertTrue(home_page_modules, msg='No module found on Home Page')
            sections = home_page_modules.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg=f'"{self.module_name_HR}" Featured module not found')

    def test_001_log_in_to_the_app_as_german_user(self):
        """
        DESCRIPTION: Log in to the app as German user
        EXPECTED: - German user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.login(username=tests.settings.german_betplacement_user, async_close_dialogs=False)
        self.site.wait_content_state('Homepage')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_002_verify_availability_of_horse_racing_greyhounds__international_tote_inmobilesports_menu_ribbondesktopheader_and_subheader_menus(self):
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
            sports_menu_items = self.site.header.top_menu.items_as_ordered_dict
            self.assertTrue(sports_menu_items, msg='Header menu has no items')
            self.assertNotIn(vec.sb.HORSERACING.upper(), sports_menu_items, msg='Horse Racing is present in Sports Menu Ribbon')
            self.assertNotIn(vec.sb.GREYHOUND.upper(), sports_menu_items, msg='Greyhounds is present in Sports Menu Ribbon')
            self.assertNotIn(vec.tote.TOTE_TITLE.upper(), sports_menu_items, msg='International Tote is present in Sports Menu Ribbon')

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
            self.assertTrue(sections, msg='Tabs on home page are not found')
            self.assertNotIn(vec.racing.RACING_NEXT_RACES_NAME, sections, msg='Next Races tab is available')

    def test_004_mobiletap_all_sports__a_z_menu_in_the_header_ribbonortap_menu_item_in_the_footerdesktopfind_a_z_sports_on_the_left_hand_side_of_the_homepage(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Tap 'All Sports'  (A-Z menu) in the header ribbon
        DESCRIPTION: OR
        DESCRIPTION: Tap 'Menu' item in the footer
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Find 'A-Z Sports' on the left-hand side of the Homepage
        EXPECTED: 'Horse Racing', 'Greyhounds' & 'International Tote' are NOT available
        """
        if self.device_type in ['mobile', 'tablet']:
            # Top Sports
            self.site.open_sport(name='ALL SPORTS')
            sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
            self.assertNotIn(vec.sb.HORSERACING.upper(), sports, msg='Horse Racing is present in subheader Menu')
            self.assertNotIn(vec.sb.GREYHOUND.upper(), sports, msg='Greyhounds is present in subheader Menu')
            self.assertNotIn(vec.tote.TOTE_TITLE.upper(), sports,
                             msg='International Tote is present in subheader Menu')

        else:
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(sports, msg='No items in "Homepage > A-Z sports left-hand menu"')
            self.assertNotIn(vec.sb.HORSERACING.upper(), sports, msg='Horse Racing is present in subheader Menu')
            self.assertNotIn(vec.sb.GREYHOUND.upper(), sports, msg='Greyhounds is present in subheader Menu')
            self.assertNotIn(vec.tote.TOTE_TITLE.upper(), sports,
                             msg='International Tote is present in subheader Menu')

    def test_005_verify_availability_horse_racing_greyhounds__international_tote_on_featured_tab_on_home_page(self):
        """
        DESCRIPTION: Verify availability 'Horse Racing', 'Greyhounds' & 'International Tote' on 'Featured' tab on Home page
        EXPECTED: 'Horse Racing', 'Greyhounds'& 'International Tote' are NOT available
        """
        self.navigate_to_page(name='/')
        if self.device_type in ['mobile', 'tablet']:
            self.__class__.home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(current_tab, self.home_featured_tab_name,
                             msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                             f'expected: "{self.home_featured_tab_name}"')
            featured_module_content = self.site.home.get_module_content(self.home_featured_tab_name)
            featured_modules = featured_module_content.accordions_list.items_as_ordered_dict
            self.assertNotIn(self.module_name_HR, featured_modules,
                             msg=f'"{self.module_name_HR}" Featured module found')
            self.assertNotIn(self.module_name_GH, featured_modules,
                             msg=f'"{self.module_name_GH}" Featured module found')
        else:
            self.site.contents.scroll_to_bottom()
            try:
                home_page_modules = self.site.home.get_module_content(vec.racing.RACING_FEATURED_TAB_NAME)
            except VoltronException as e:
                self._logger.error(e)
            else:
                self.assertTrue(home_page_modules, msg='No module found on Home Page')
                featured_section = home_page_modules.accordions_list.items_as_ordered_dict
                self.assertNotIn(self.module_name_HR, featured_section,
                                 msg=f'"{self.module_name_HR}" Featured module found')
                self.assertNotIn(self.module_name_GH, featured_section,
                                 msg=f'"{self.module_name_GH}" Featured module found')

    def test_006_open_in_play_pagemobiletablettap_in_play_icon_on_the_sports_menu_ribbon_on_the_homepagedesktopclick_in_play_icon_on_the_header_menussubheader_menus(self):
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
            self.device.driver.implicitly_wait(2)
            try:
                menu_items = self.site.home.menu_carousel.items_as_ordered_dict
            except (VoltronException, StaleElementReferenceException):
                menu_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.device.driver.implicitly_wait(0)
            self.assertTrue(menu_items, msg='No Sports Menu Ribbon in "In-play"')
            self.assertNotIn(vec.sb.HORSERACING, menu_items, msg='Horse Race is present in Header menu')
            self.assertNotIn(vec.sb.GREYHOUND, menu_items, msg='Greyhounds is present in Header menu')
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No menu items on Home page')
            in_play_tab = menu_items[vec.sb.IN_PLAY.upper()]
            in_play_tab.click()
            self.device.driver.implicitly_wait(2)
            menu_carousel_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.device.driver.implicitly_wait(0)
            self.assertTrue(menu_carousel_items, msg='No Header Menus/SubHeader Menus in "In-Play"')
            self.assertNotIn(vec.sb.HORSERACING, menu_carousel_items,
                             msg='Horse Race is present in Header Menus/SubHeader Menus')
            self.assertNotIn(vec.sb.GREYHOUND, menu_carousel_items,
                             msg='Greyhounds is present in Header Menus/SubHeader Menus')

    def test_007_mobiletabletopen_in_play_module_on_the_featured_tab(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are not shown
        EXPECTED: * All other sports but racing are available
        """
        self.navigate_to_page(name='/')
        if self.device_type in ['mobile', 'tablet']:
            modules_inplay = self.site.home.tab_content.in_play_module.items_as_ordered_dict
            self.assertTrue(modules_inplay, msg='In Play module is not present on Homepage tab')
            self.assertNotIn(vec.sb.HORSERACING, modules_inplay,
                             msg='Horse Racing is available in In-Play on featured tab')
            self.assertNotIn(vec.sb.GREYHOUND, modules_inplay,
                             msg='Grey Hound is available in In-Play on featured tab')

    def test_008_mobiletabletopen_in_play_tab_on_the_homepagedesktopfind_in_play_and_live_stream_tab_on_the_homepage(self):
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
        # Mobile: Its covered in step 6
        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
            home_module_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            self.assertTrue(home_module_items, msg='"In-play and live stream" items are not present on Homepage tab')
            self.assertNotIn(vec.sb.HORSERACING, home_module_items,
                             msg='Horse Racing is present in In-play and live stream')
            self.assertNotIn(vec.sb.GREYHOUND, home_module_items,
                             msg='Greyhounds is present in In-play and live stream')

    def test_009_mobiletabletfooter_menu__menu_item__tap_on_in_playdesktophomepage__a_z_sports_left_hand_menu__in_play(self):
        """
        DESCRIPTION: **Mobile/Tablet: **
        DESCRIPTION: Footer menu > 'Menu' item > Tap on ‘In Play’
        DESCRIPTION: **Desktop: **
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
            self.assertTrue(events_in_play, msg='No items are in "In-Play"')
            self.assertNotIn(vec.sb.HORSERACING, events_in_play,
                             msg='Horse Race is present in Footer menu > In-Play')
            self.assertNotIn(vec.sb.GREYHOUND, events_in_play,
                             msg='Greyhounds is present in Footer menu > In-Play')
        else:
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(sports, msg='No items in "Homepage > A-Z sports left-hand menu"')
            sports.get(vec.sb.IN_PLAY).click()
            events_in_play = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(events_in_play, msg='No items in "In-Play"')
            self.assertNotIn(vec.sb.HORSERACING, events_in_play,
                             msg='Horse Race is present in A-Z sports left-hand menu > In-Play')
            self.assertNotIn(vec.sb.GREYHOUND, events_in_play,
                             msg='Greyhounds is present in A-Z sports left-hand menu > In-Play')

    def test_010___add_horse_racing_route_to_the_url__press_enter(self, target_url='/horse-racing'):
        """
        DESCRIPTION: - Add "/horse-racing" route to the url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: * Homepage is opened
        EXPECTED: * The standard error popup is displayed with:
        EXPECTED: Header: 'Country Restriction'
        EXPECTED: Text: 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
        """
        self.device.navigate_to(url=f'{tests.HOSTNAME}{target_url}')
        dialog = self.site.wait_for_dialog(dialog_name=vec.bma.COUNTRY_RESTRICTION.header)
        self.assertTrue(dialog, msg='Country Restriction dialog is not shown')
        actual_text = dialog.text
        expected_text = vec.bma.COUNTRY_RESTRICTION.racing_message_body
        self.assertEquals(actual_text, expected_text,
                          msg=f'Actual error message: "{actual_text}" is not equal to expected: "{expected_text}"')
        self.assertTrue(dialog.ok_button.is_displayed(), msg='"OK" button is not displayed')
        dialog.close_dialog()
        self.assertTrue(dialog.wait_dialog_closed(), msg=f'"{vec.bma.COUNTRY_RESTRICTION.header}" Dialog is not closed')

    def test_011___add_greyhound_racing_route_to_the_url__press_enter(self):
        """
        DESCRIPTION: - Add "/greyhound-racing" route to the url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: * Homepage is opened
        EXPECTED: * The standard error popup is displayed with:
        EXPECTED: Header: 'Country Restriction'
        EXPECTED: Text: 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
        """
        self.test_010___add_horse_racing_route_to_the_url__press_enter(target_url='/greyhound-racing')

    def test_012___add_tote_route_to_the_url__press_enter(self):
        """
        DESCRIPTION: - Add "tote" route to the url
        DESCRIPTION: - Press 'Enter'
        EXPECTED: * Homepage is opened
        EXPECTED: * The standard error popup is displayed with:
        EXPECTED: Header: 'Country Restriction'
        EXPECTED: Text: 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
        """
        self.test_010___add_horse_racing_route_to_the_url__press_enter(target_url='/tote')

    def test_013___add_homenext_races__press_enter(self):
        """
        DESCRIPTION: - Add "home/next-races"
        DESCRIPTION: - Press 'Enter'
        EXPECTED: * Homepage is opened
        EXPECTED: * The standard error popup is displayed with:
        EXPECTED: Header: 'Country Restriction'
        EXPECTED: Text: 'We are unable to offer Horse Racing or Greyhound betting in your jurisdiction.'
        """
        if self.device_type != 'desktop':
            self.test_010___add_horse_racing_route_to_the_url__press_enter(target_url='/home/next-races')

    def test_014_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.logout(timeout=0.5)
        self.site.wait_content_state('Homepage')
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE', msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                                              f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_015_repeat_steps_2_8(self):
        """
        DESCRIPTION: Repeat steps 2-8
        """
        self.test_002_verify_availability_of_horse_racing_greyhounds__international_tote_inmobilesports_menu_ribbondesktopheader_and_subheader_menus()
        self.test_003_verify_availability_of_next_races_tab_on_home_page()
        self.test_004_mobiletap_all_sports__a_z_menu_in_the_header_ribbonortap_menu_item_in_the_footerdesktopfind_a_z_sports_on_the_left_hand_side_of_the_homepage()
        self.test_005_verify_availability_horse_racing_greyhounds__international_tote_on_featured_tab_on_home_page()
        self.test_006_open_in_play_pagemobiletablettap_in_play_icon_on_the_sports_menu_ribbon_on_the_homepagedesktopclick_in_play_icon_on_the_header_menussubheader_menus()
        self.test_007_mobiletabletopen_in_play_module_on_the_featured_tab()
        self.test_008_mobiletabletopen_in_play_tab_on_the_homepagedesktopfind_in_play_and_live_stream_tab_on_the_homepage()
