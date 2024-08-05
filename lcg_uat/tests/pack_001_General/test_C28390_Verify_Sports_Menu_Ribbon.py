import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.smoke
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.navigation
@pytest.mark.menu_ribbon
@pytest.mark.back_button
@pytest.mark.mobile_only
@pytest.mark.safari
@pytest.mark.slow
@pytest.mark.timeout(800)
@pytest.mark.login
@vtest
class Test_C28390_Verify_Sports_Menu_Ribbon(BaseUserAccountTest):
    """
    TR_ID: C28390
    VOL_ID: C9697593
    NAME: Verify Sports Menu Ribbon
    DESCRIPTION: This test case verifies Sports Menu Ribbon
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-12042 CMS - Ability to Hide/Show Mobile Ribbon Tabs on Mobile/Tablet
    DESCRIPTION: BMA-12043 Client - Module Ribbon Tabs
    DESCRIPTION: BMA-16183 Amend Breakpoints on Landscape for Oxygen Mobile
    PRECONDITIONS: CMS: https://**CMS_ENDPOINT**/keystone//keystone/sport-categories
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    allow_dict = {
        'ALL SPORTS': 'AllSports',
        'CRICKET': 'CRICKET',
        'HORSE RACING': 'Horseracing',
        'FOOTBALL': 'FOOTBALL',
        'LOTTO': 'LOTTO',
        'IN-PLAY': 'INPLAY',
        'TENNIS': 'TENNIS',
        'VIRTUAL': 'VirtualSports',
        'GREYHOUNDS': 'GREYHOUNDRACING',
        'AUSSIERULES': 'AUSSIERULES',
        'BASKETBALL': 'BASKETBALL'
    }

    keep_browser_open = True
    icon_formats_list = ['.png', '.jpg', '.jpeg', '']

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: *   Homepage is opened
        EXPECTED: *   Sports Menu Ribbon is displayed
        """
        self.assertTrue(self.site.home.menu_carousel.is_displayed(),
                        msg='Sports Ribbon is not displayed for non-logged user')

    def test_002_verify_presence_of_sports_menu_ribbon(self):
        """
        DESCRIPTION: Verify presence of Sports Menu Ribbon
        EXPECTED: *   Sports Menu Ribbon is applicable only to Homepage
        EXPECTED: *   Sports Menu Ribbon is applicable to both logged in and logged out customers
        EXPECTED: *   It is left and right scrolling Ribbon
        EXPECTED: *   Every item is tappable icon with label
        """
        self.site.login(username=tests.settings.betplacement_user)
        self.assertTrue(self.site.home.menu_carousel.is_displayed(),
                        msg='Sports Ribbon is not displayed for logged user')
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        for item_name, item in all_items.items():
            if item_name.strip() not in self.allow_dict.keys():
                self._logger.debug('*** Item "%s" skipped' % item_name)
                continue
            self.site.wait_content_state('HomePage')
            self._logger.info('*** Navigating to [%s]' % item_name)
            self.site.home.menu_carousel.click_item(item_name)
            self.site.wait_content_state(self.allow_dict[item_name])
            self.site.sports_page.back_button_click()
            self.site.wait_content_state('HomePage')

    def test_003_verify_height_of_sports_menu_ribbon_on_mobile_tablet_in_portrait_and_landscape_modes(self):
        """
        DESCRIPTION: Verify height of Sports Menu Ribbon On Mobile, Tablet in Portrait and Landscape Modes
        EXPECTED: Sports Menu Ribbon height is as following:
        EXPECTED: * Device CSS Screen Width from 360 to 460 px  - Menu height 60 px
        EXPECTED: * Device CSS Screen Width from 461 to 1023 px - Menu height 90 px
        EXPECTED: * Device CSS Screen Width from 1023 px  - Menu is not displayed
        """
        device_screen_width = self.device.driver.get_window_size().get('width')
        menu_height = None
        if 360 <= device_screen_width <= 460:
            menu_height = 60
        elif 461 <= device_screen_width <= 1023:
            menu_height = 90 if self.brand != 'ladbrokes' else 64
        else:
            self._logger.debug('*** Menu is not displayed')
        if menu_height:
            actual_height = self.site.home.menu_carousel.size['height']
            self.assertEqual(menu_height, actual_height,
                             msg=f"Actual carousel height {actual_height} does not match expected {menu_height}")

    def test_004_verify_menu_item_names(self):
        """
        DESCRIPTION: Verify Menu item names
        EXPECTED: Menu item names correspond to the names set in CMS
        """
        items_from_the_ui = [*self.site.home.menu_carousel.items_as_ordered_dict]
        if self.brand != 'ladbrokes':
            sport_titles = [sport['imageTitle'].upper().strip() for sport in self.cms_config.get_show_in_sports_ribbon() if
                            sport['showInHome'] and not sport['disabled']]
        else:
            sport_titles = [sport['imageTitle'].strip() for sport in self.cms_config.get_show_in_sports_ribbon() if
                            sport['showInHome'] and not sport['disabled']]
            if "Fanzone"in sport_titles or "Fanzone" in items_from_the_ui:
                sport_titles.remove("Fanzone")
                if "Fanzone" in items_from_the_ui:
                    items_from_the_ui.remove("Fanzone")

        self.assertListEqual(sport_titles, items_from_the_ui,
                             msg='Sports from the UI does not match sports from the response.'
                             f'\nActual: "{items_from_the_ui}". \nExpected: "{sport_titles}"')

    def test_005_verify_end_point_after_tapping_menu_items(self):
        """
        DESCRIPTION: Verify end point after tapping Menu items
        EXPECTED: Tapping Menu items redirect to the pages, path for which were set in 'Target Uri' field in CMS (e.g. football/today)
        """
        target_uri = {item['imageTitle'].upper(): item['targetUri'].strip()
                      for item in self.cms_config.get_sport_categories() if item['showInHome']}
        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        for item_name, item in all_items.items():
            if item_name.strip() not in self.allow_dict.keys():
                self._logger.info(f'*** Item "{item_name}" skipped')
                continue
            self.site.wait_content_state('HomePage')
            self._logger.info(f'*** Navigating to [{item_name}]')
            self.site.home.menu_carousel.click_item(item_name)
            self.site.wait_content_state(self.allow_dict[item_name])
            url = self.device.get_current_url()
            expected_tab_url = target_uri[item_name]
            self.assertIn(expected_tab_url, url, msg=f'Url of tab on Oxygen "{url}" '
                          f'is not the same as the one configured in CMS {expected_tab_url}')
            self.site.sports_page.back_button_click()
            self.site.wait_content_state('HomePage')

    def test_006_verify_menu_item_if_there_are_no_events_available_for_particular_sport(self):
        """
        DESCRIPTION: Verify Menu item if there are no events available for particular sport
        EXPECTED: Menu item is still visible in the Sports Menu Ribbon
        EXPECTED: <Sport> landing page is shown after tapping Menu item
        """
        if self.brand != 'ladbrokes':
            sport_titles = [sport['imageTitle'].upper() for sport in self.cms_config.get_sport_categories()
                            if (sport['showInHome'] and sport['hasEvents'] is False and sport['disabled'] is False)]
        else:
            sport_titles = [sport['imageTitle'] for sport in self.cms_config.get_sport_categories()
                            if (sport['showInHome'] and sport['hasEvents'] is False and sport['disabled'] is False)]

        all_items = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(all_items, msg='No items on MenuCarousel found')
        self.assertTrue(set(all_items).issuperset(set(sport_titles)),
                        msg='Menu item without events is not visible in the Sports Menu Ribbon')
        for sport in sport_titles:
            if sport not in self.allow_dict.keys():
                continue
            self.site.wait_content_state('HomePage')
            self._logger.info(f'*** Navigating to [{sport}]')
            self.site.home.menu_carousel.click_item(sport)
            self.site.wait_content_state(self.allow_dict[sport])
            self.site.sports_page.back_button_click()
            self.site.wait_content_state('HomePage')

    def test_007_verify_menu_items_visibility(self):
        """
        DESCRIPTION: Verify Menu items' visibility
        EXPECTED: *   Show in Menu (selected/unselected) - determines whether the menu item should be visible in the Sports Menu Ribbon (default - unselected)
        EXPECTED: *   Disabled (selected/unselected) - determines whether the menu item should be/should not be untappable and grayed out
        EXPECTED: *   Show Item On (Home, In-Play, Both) - determines whether the menu item should be shown in Homepage Sport Selector Ribbon, In-Play Sport Selector Ribbon or in both locations
        """
        # verified in step # 6
        pass

    def test_008_verify_menu_item_icons_format(self):
        """
        DESCRIPTION: Verify Menu item icons' format
        EXPECTED: *   'Filename' support only PNG or JPEG format
        EXPECTED: *   It is possible not to upload an icon image
        """
        expected_items_icons_formats = [sport['uriSmall'] for sport in self.cms_config.get_sport_categories()
                                        if (sport['showInHome'] and sport['uriSmall'] is not None)]
        for item in expected_items_icons_formats:
            self.assertTrue(item.endswith(('.png', '.jpg', '.jpeg', '')),
                            msg=f'Actual icon format: "{item}" is not expected one: "{self.icon_formats_list}"')

    def test_009_verify_menu_item_displaying_on_mobile_tablet(self):
        """
        DESCRIPTION: Verify Menu item displaying on Mobile, Tablet
        EXPECTED: *   'Show Ribbon Tab' dropdown (Mobile/Tablet, Desktop and Both) determines possibility to show sports ribbon tab for mobile/tablet users, desktop users or all of them.
        EXPECTED: *   If nothing is selected then 'Both' option will be set by default.
        """
        # verified in step # 6
        pass
