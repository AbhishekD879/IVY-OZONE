import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.lad_tst2  # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C9701468_Verify_availability_of_Races_pages_for_a_non_german_user(BaseFeaturedTest):
    """
    TR_ID: C9701468
    NAME: Verify availability of <Races> pages for a non-german user
    DESCRIPTION: This test case verifies displaying 'Races' in Sports Ribbon (mobile), A-Z page, Header & Sub Header (desktop) & having access to 'Races' pages via url for a non German user
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    """
    keep_browser_open = True

    def validating_hr(self, keys):
        items_to_check = [vec.racing.HORSE_RACING_TAB_NAME.capitalize(), vec.sb.HORSERACING.title()]
        self.assertTrue(any(i in keys for i in items_to_check), msg='Horse Racing or Horses is not present in the list')

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. Horse Racing/Greyhounds/International Totes is configured in CMS for:
        DESCRIPTION: - Sport Pages > Sport Categories > Lotto > General Sport Configuration:  "Show in Sports Ribbon", "Show in AZ", "Is Top Sport" are checked; "Target URi": "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: - Menus > Header Menus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: - Header SubMenus > Horse Racing/Greyhounds/International Totes: "Target URi:" "/horse-racing", "/greyhound-racing", "/tote"
        DESCRIPTION: 2. Ensure that there are GH, International Totes, and HR Featured with different 'Select Events by' drop-down items available:
        DESCRIPTION: * EventsModule  (CMS > Featured Tab Modules > Active Featured Modules)
        DESCRIPTION: * SurfaceBetModule (CMS > Main Navigation > Homepage > Surface Bet Module > Active Surface Bets)
        DESCRIPTION: 3. A German user is registered (with "signupCountryCode: "DE" - select Germany as a country during registration)
        DESCRIPTION: 4. A non-german user is registered
        """
        sport_categories_list = self.cms_config.get_sport_categories()
        greyhound_id = self.ob_config.greyhound_racing_config.category_id
        greyhounds = list(filter(lambda param: param['categoryId'] == greyhound_id, sport_categories_list))
        greyhounds_name = greyhounds[0].get('imageTitle', None)

        horse_racing_id = self.ob_config.horseracing_config.category_id
        horse_racing = list(filter(lambda param: param['categoryId'] == horse_racing_id, sport_categories_list))
        horse_racing_name = horse_racing[0].get('imageTitle', None)

        try:
            tote_id = self.ob_config.tote_config.category_id
            international_tote = list(filter(lambda param: param['categoryId'] == tote_id, sport_categories_list))
            international_tote_name = international_tote[0].get('imageTitle', None)
        except IndexError:
            international_tote_name = None
            self._logger.error(f'*** Can not get "categoryId" or International tote is not configured on prod')

        self.assertTrue(sport_categories_list, msg='No events on sports categories')
        for sport in sport_categories_list:
            sport_name = sport['imageTitle']
            if sport_name in (greyhounds_name, horse_racing_name, international_tote_name):
                if not sport['showInAZ']:
                    raise CmsClientException(f'"Show in AZ" is not enabled or not configured in CMS for "{sport_name}"')
                if not sport['isTopSport']:
                    raise CmsClientException(
                        f'"Is Top Sport" is not enabled or not configured in CMS for "{sport_name}"')
                if not sport['showInHome']:
                    raise CmsClientException(
                        f'"Show in home" is not enabled or not configured in CMS for "{sport_name}"')

        event_list = [greyhounds_name, horse_racing_name, international_tote_name]

        # Header
        cms_header_menu_items = self.cms_config.get_cms_header_menu_items()
        header_list = [item['linkTitle'] for item in cms_header_menu_items]

        for sport in event_list:
            if sport not in header_list:
                raise CmsClientException(f'CMS Header does not have or not configured in CMS "{sport}"')

        for sport in cms_header_menu_items:
            sport_name = sport['linkTitle']
            if sport['linkTitle'] in event_list:
                self.assertTrue(sport['targetUri'],
                                msg=f'"targetUri" field is not configured for "{sport_name}" in CMS')

        # Submenu
        cms_header_submenu_items = self.cms_config.get_header_submenus()
        sub_header_list = [item['linkTitle'] for item in cms_header_submenu_items]
        for sport in event_list:
            if sport not in sub_header_list:
                raise CmsClientException(f'CMS Header Sub menu does not have "{sport}"')

        for sport in cms_header_submenu_items:
            sport_name = sport['linkTitle']
            if sport['linkTitle'] in event_list:
                self.assertTrue(sport['targetUri'],
                                msg=f'"targetUri" field is not configured for "{sport_name}" in CMS')

        if tests.settings.backend_env == 'prod':
            event = self.get_active_event_for_category(
                category_id=self.ob_config.backend.ti.greyhound_racing.category_id)
            self.__class__.type_id_GH = event['event']['typeId']

            event = self.get_active_event_for_category(
                category_id=self.ob_config.backend.ti.horse_racing.category_id)
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

            prices = {0: '1/2', 1: '1/3'}
            event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2, lp_prices=prices, is_live=True)
            self.__class__.selection_ids = event_params1.selection_ids

            event_params2 = self.ob_config.add_UK_greyhound_racing_event(number_of_runners=2, lp_prices=prices,
                                                                         is_live=True)
            self.__class__.selection_ids2 = event_params2.selection_ids

    def test_001_log_in_as_a_german_user__log_out(self):
        """
        DESCRIPTION: Log in as a german user > Log out
        EXPECTED: - German user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        self.site.login(username=tests.settings.german_betplacement_user)
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match '
                         f'expected result "DE". Actual value of "OX.countryCode" is "{key_value}"')
        self.site.logout()

    def test_002_log_in_as_a_non_german_user(self):
        """
        DESCRIPTION: Log in as a non german user
        EXPECTED: - Non german user is logged in
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        self.site.login()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "GB". '
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_003_verify_availability_of_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Verify availability of 'Next Races' tab on Home page
        EXPECTED: 'Next Races' tab is available
        """
        if self.device_type in ['mobile', 'tablet']:
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        else:
            tabs = self.site.home.desktop_modules.items_as_ordered_dict

        self.assertTrue(tabs, msg='No sections on Home page')
        self.assertIn(vec.racing.RACING_NEXT_RACES_NAME, tabs, msg='Next Races section is not available')

    def test_004_verify_availability_of_hr__gh_in_the_featured_module_on_homepage(self):
        """
        DESCRIPTION: Verify availability of HR & GH in the Featured module on Homepage
        EXPECTED: HR & GH are available in the Featured module
        """
        if self.device_type in ['mobile', 'tablet']:
            self.__class__.home_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEqual(current_tab, self.home_featured_tab_name,
                             msg=f'Actual Module Ribbon tab selected by default: "{current_tab}", '
                             f'Expected: "{self.home_featured_tab_name}"')
            featured_module_content = self.site.home.get_module_content(self.home_featured_tab_name)
            featured_section = featured_module_content.accordions_list.items_as_ordered_dict
        else:
            self.site.contents.scroll_to_bottom()
            home_page_modules = self.site.home.get_module_content(vec.racing.RACING_FEATURED_TAB_NAME)
            self.assertTrue(home_page_modules, msg='No module found on Home Page')
            featured_section = home_page_modules.accordions_list.items_as_ordered_dict

        self.assertTrue(featured_section, msg='No Sections found on Featured module')

        self.softAssert(self.assertIn, self.module_name_HR, featured_section,
                        msg=f'"{self.module_name_HR}" Horse Race not found in Featured module found')
        self.softAssert(self.assertIn, self.module_name_GH, featured_section,
                        msg=f'"{self.module_name_GH}" Greyhounds not found in Featured module found')

    def test_005_open_in_play_page(self):
        """
        DESCRIPTION: Open 'In-Play' Page
        DESCRIPTION: For Mobile/Tablet
        DESCRIPTION: Tap 'In-Play' icon on the Sports Menu Ribbon on the homepage
        DESCRIPTION: For Desktop
        DESCRIPTION: Click 'In-Play' icon on the Header Menus/SubHeader Menus
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are available
        """
        if self.device_type in ['mobile', 'tablet']:
            self.site.home.menu_carousel.click_item(vec.sb.IN_PLAY)
            menu_items = wait_for_result(lambda: self.site.home.menu_carousel.items_as_ordered_dict, timeout=5,
                                         bypass_exceptions=(NoSuchElementException,
                                                            StaleElementReferenceException,
                                                            VoltronException),
                                         name='In Play items on menu carousel')
            self.assertTrue(menu_items, msg='No Sports Menu Ribbon in "In-play"')
            self.validating_hr(menu_items.keys())
            self.assertIn(vec.sb.GREYHOUND.capitalize(), menu_items, msg='Greyhounds is not present in Header menu')
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No menu items on Home page')
            in_play_tab = menu_items[vec.sb.IN_PLAY.upper()]
            in_play_tab.click()
            in_play_items = wait_for_result(lambda: self.site.home.menu_carousel.items_as_ordered_dict, timeout=5,
                                            name='In Play items on menu carousel')
            self.assertTrue(in_play_items, msg='No Header Menus/SubHeader Menus in "In-Play"')
            self.validating_hr(in_play_items.keys())
            self.assertIn(vec.sb.GREYHOUND.capitalize(), in_play_items,
                          msg='Greyhounds is not present in Header Menus/SubHeader Menus')

    def test_006_mobiletabletopen_in_play_module_on_the_featured_tabdesktopclick_upcoming_tab_in_in_play_module(self):
        """
        DESCRIPTION: For mobile/Tablet
        DESCRIPTION: Open 'In Play' module on the 'Featured' tab
        DESCRIPTION: For Desktop
        DESCRIPTION: Click 'Upcoming' tab in 'In-Play' module
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are available
        """
        self.navigate_to_page(name='/')
        if self.device_type in ['mobile', 'tablet']:
            in_play_module = self.site.home.tab_content.in_play_module
            in_play_module_items = in_play_module.items_as_ordered_dict
            self.assertTrue(in_play_module_items, msg='Cannot find any module items')
            try:
                self.assertIn(vec.sb.HORSERACING.upper(), in_play_module_items,
                              msg='Horse Racing is not present in Upcoming tab')
                self.assertIn('GREYHOUND RACING', in_play_module_items,
                              msg='Greyhounds is not present in Upcoming tab')
            except VoltronException:
                self._logger.error('*** No Horse Racing or Greyhounds In Play module on the Featured tab')
        else:
            menu_items = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='No menu items on Home page')
            in_play_tab = menu_items[vec.sb.IN_PLAY.upper()]
            in_play_tab.click()
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
            upcoming_list = self.site.inplay.tab_content.upcoming
            if upcoming_list is None:
                self._logger.info('*** No events found in Upcoming tab')
            else:
                self.assertIn(vec.sb.HORSERACING.upper(), upcoming_list,
                              msg='Horse Racing is not present in Upcoming tab')
                self.assertIn('GREYHOUND RACING', upcoming_list,
                              msg='Greyhounds is not present in Upcoming tab')

    def test_007_in_play_tab_on_the_homepage(self):
        """
        DESCRIPTION: For Mobile/Tablet
        DESCRIPTION: Open 'In-Play' tab on the Homepage
        DESCRIPTION: For Desktop
        DESCRIPTION: Find 'In-play and live stream' tab on the Homepage
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are available
        EXPECTED: * 'View all in-play [racing]' button is displayed
        """
        if self.device_type in ['mobile', 'tablet']:
            self.site.home.get_module_content(
                module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play))
            live_now = self.site.home.tab_content.live_now.items_as_ordered_dict
            self.assertTrue(live_now, msg='No Live events')
            upcoming = self.site.home.tab_content.upcoming.items_as_ordered_dict
            if upcoming is None:
                self._logger.info('*** No Upcoming events')
            else:
                self.assertTrue(upcoming, msg='No Upcoming events')
            result_list = [*live_now, *upcoming]
            self.assertIn(vec.sb.HORSERACING.upper(), result_list,
                          msg='Horse Racing is not available in In-Play tab on the Homepage')
            self.assertIn('GREYHOUND RACING', result_list,
                          msg='Grey Hound is not available in In-Play tab on the Homepage')
        else:
            self.navigate_to_page(name='/')
            home_module_items = self.site.home.desktop_modules.inplay_live_stream_module.menu_carousel.items_as_ordered_dict
            self.assertTrue(home_module_items, msg='No items "In-play and live stream" tab on the Homepage')
            self.validating_hr(home_module_items.keys())
            self.assertIn(vec.sb.GREYHOUND, home_module_items,
                          msg='Greyhounds is not present in In-play and live stream')

    def test_008_mobiletabletfooter_menu__menu_item__tap_on_in_playdesktophomepage__a_z_sports_left_hand_menu__in_play(
            self):
        """
        DESCRIPTION: For Mobile/Tablet
        DESCRIPTION: Footer menu > 'Menu' item > Tap on ‘In Play’
        DESCRIPTION: For Desktop
        DESCRIPTION: Homepage > 'A-Z sports' left-hand menu > 'In-Play'
        EXPECTED: * The page is opened
        EXPECTED: * GH and HR are available
        """
        self.navigate_to_page(name='/')
        if self.device_type in ['mobile', 'tablet']:
            item = self.site.navigation_menu.items_as_ordered_dict
            self.assertTrue(item, msg='No items in Footer menu')
            item.get('Menu').click()
            self.site.all_sports.click_item(vec.sb.IN_PLAY)
            events_in_play = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(events_in_play, msg='No items in "In-Play"')
            self.validating_hr(events_in_play.keys())
            self.assertIn(vec.sb.GREYHOUND, events_in_play,
                          msg='Greyhounds is not present in Footer menu>In-Play')
        else:
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertTrue(sports, msg='No items in "Homepage > A-Z sports left-hand menu"')
            sports.get(vec.sb.IN_PLAY).click()
            events_in_play = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(events_in_play, msg='No items in "In-Play"')
            self.validating_hr(events_in_play.keys())
            self.assertIn(vec.sb.GREYHOUND, events_in_play,
                          msg='Greyhounds is not present in A-Z sports left-hand menu>In-Play')

    def test_009_tap_on_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Tap on 'Next Races' tab on Home page
        EXPECTED: 'Next Races' tab is opened
        """
        self.navigate_to_page(name='/')
        if self.device_type in ['mobile', 'tablet']:
            next_races = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races)
            self.site.home.module_selection_ribbon.tab_menu.click_button(next_races)
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.assertEquals(current_tab, vec.racing.RACING_NEXT_RACES_NAME,
                              msg=f'Actual tab opened: "{current_tab}" is not equal to '
                              f'Expected tab: "{vec.racing.RACING_NEXT_RACES_NAME}"')

    def test_010_verify_availability_of_horse_racing_greyhounds__international_tote_inmobilesports_menu_ribbondesktopheader_and_subheader_menus(
            self):
        """
        DESCRIPTION: Verify availability of 'Horse Racing', 'Greyhounds' & 'International Tote' in
        DESCRIPTION: For Mobile
        DESCRIPTION: Sports Menu Ribbon
        DESCRIPTION: For Desktop
        DESCRIPTION: Header and subheader menus
        EXPECTED: 'Horse Racing', 'Greyhounds' & 'International Tote' are available
        """
        self.navigate_to_page(name='/')
        if self.device_type in ['mobile', 'tablet']:
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(all_items, msg='Sports Menu Ribbon does not have any items')
            self.validating_hr(all_items.keys())
            self.assertIn(vec.sb.GREYHOUND, all_items, msg='Greyhounds is not present in Sports Menu Ribbon')
            self.assertIn(vec.tote.TOTE_TITLE.title(), all_items,
                          msg='International Tote is not present in Sports Menu Ribbon')
        else:
            # Header menu
            sports = self.site.header.top_menu.items_as_ordered_dict
            self.assertTrue(sports, msg=' Header menu has no items')
            self.assertIn(vec.sb.HORSERACING.upper(), sports,
                          msg='Horse Racing is not present in Sports Menu Ribbon')
            self.assertIn(vec.sb.GREYHOUND.upper(), sports,
                          msg='Greyhounds is not present in Sports Menu Ribbon')
            self.assertIn(vec.tote.TOTE_TITLE.upper(), sports,
                          msg='International Tote is not present in Sports Menu Ribbon')

            # Header sub menu
            sports = self.site.header.sport_menu.items_as_ordered_dict
            self.assertTrue(sports, msg=' Header sub menu has no items')
            self.assertIn(vec.sb.HORSERACING.upper(), sports,
                          msg='Horse Racing is not present in subheader Menu ')
            self.assertIn(vec.sb.GREYHOUND.upper(), sports,
                          msg='Greyhounds is not present in subheader Menu')
            self.assertIn(vec.tote.TOTE_TITLE.upper(), sports,
                          msg='International Tote is not present in subheader Menu')

    def test_011_navigate_to_horse_racing_pages_eg_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Horse Racing' pages e.g. landing page
        EXPECTED: 'Horse Racing' pages are opened
        """
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horse Racing')

    def test_012_navigate_to_greyhounds_pages_eg_landing_page(self):
        """
        DESCRIPTION: Navigate to 'Greyhounds' pages e.g. landing page
        EXPECTED: 'Greyhounds' pages are opened
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')

    def test_013_navigate_to_international_totes_page(self):
        """
        DESCRIPTION: Navigate to 'International Totes' page
        EXPECTED: 'International Totes' page is opened
        """
        self.navigate_to_page(name='/tote')
        self.site.wait_content_state('TOTE')

    def test_014_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: - Non german user is logged out
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="[e.g. GB]"
        """
        self.site.logout()
        key_value = self.get_local_storage_cookie_value_as_dict('OX.countryCode')
        self.assertEqual(key_value, 'GB',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "GB". '
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_015_repeat_steps_3_13(self):
        """
        DESCRIPTION: Repeat steps 3-13
        """
        self.test_003_verify_availability_of_next_races_tab_on_home_page()
        self.test_004_verify_availability_of_hr__gh_in_the_featured_module_on_homepage()
        self.test_005_open_in_play_page()
        self.test_006_mobiletabletopen_in_play_module_on_the_featured_tabdesktopclick_upcoming_tab_in_in_play_module()
        self.test_007_in_play_tab_on_the_homepage()
        self.test_008_mobiletabletfooter_menu__menu_item__tap_on_in_playdesktophomepage__a_z_sports_left_hand_menu__in_play()
        self.test_009_tap_on_next_races_tab_on_home_page()
        self.test_010_verify_availability_of_horse_racing_greyhounds__international_tote_inmobilesports_menu_ribbondesktopheader_and_subheader_menus()
        self.test_011_navigate_to_horse_racing_pages_eg_landing_page()
        self.test_012_navigate_to_greyhounds_pages_eg_landing_page()
        self.test_013_navigate_to_international_totes_page()
