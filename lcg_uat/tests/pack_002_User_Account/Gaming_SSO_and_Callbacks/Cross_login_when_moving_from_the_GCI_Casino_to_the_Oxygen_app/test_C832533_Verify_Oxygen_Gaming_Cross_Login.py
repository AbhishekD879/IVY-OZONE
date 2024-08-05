import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_journey_gaming_x_sell
@pytest.mark.gaming
@pytest.mark.login
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.login
@pytest.mark.desktop
@vtest
class Test_C832533_Verify_Oxygen_Gaming_Cross_Login(BaseUserAccountTest):
    """
    TR_ID: C832533
    NAME: Verify Oxygen-Gaming Cross Login.
    DESCRIPTION: This test case verifies that cross Login is working after navigation from BMA to Gaming Lobby
    """
    gaming_url = None
    keep_browser_open = True
    blocked_hosts = ['*.goqubit.*']
    device_name = 'iPhone XS' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify gaming URL
        """
        cms_footer_menus = self.cms_config.get_cms_menu_items(menu_types='Footer Menus').get('Footer Menus')
        for menu in cms_footer_menus:
            if '/en/games' in menu['targetUri']:
                self.__class__.gaming_url = menu['targetUri']
                self.__class__.games = menu['linkTitle']
                break
        if not self.gaming_url:
            raise CmsClientException('"Gaming URL" is not configured in CMS')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Home')

    def test_002_log_in_without_remember_me_option(self):
        """
        DESCRIPTION: Log in (without remember me option)
        EXPECTED: Login is successful
        """
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)

    def test_003_select_gaming_from_sports_selector_ribbon(self):
        """
        DESCRIPTION: Select Gaming from Sports Selector Ribbon
        EXPECTED: * Gaming Lobby is opened
        EXPECTED: * User is automatically logged in to Gaming Lobby
        """
        if self.device_type == 'mobile':
            footer_navigation_menu = self.site.navigation_menu.items_as_ordered_dict
            self.assertTrue(footer_navigation_menu, msg='No items on Footer navigation found')
            self.__class__.games = next((menu_name for menu_name in footer_navigation_menu if menu_name.upper().strip() == self.games.upper().strip()), None)
            gaming = footer_navigation_menu.get(self.games)
        else:
            # workaround for appearing Sports Selector Ribbon on beta-sports.ladbrokes.com
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state('HomePage')
            top_items = self.site.header.top_menu.items_as_ordered_dict
            self.assertTrue(top_items, msg=' Header menu has no items')
            self.__class__.games = next((menu_name for menu_name in top_items if menu_name.upper().strip() == self.games.upper().strip()), None)
            gaming = top_items.get(self.games)
        self.assertTrue(gaming, msg='Gaming is not found')
        gaming.click()

        attempts = 5
        while attempts:
            try:
                attempts -= 1
                gaming_opened = wait_for_result(
                    lambda: 'gaming' in self.device.get_current_url() or 'games' in self.device.get_current_url(),
                    timeout=10, poll_interval=1, name='Gaming Lobby to be opened')
                self.assertTrue(
                    gaming_opened, msg=f'Gaming Lobby is not opened, instead page {self.device.get_current_url()} is opened')
                res = self.assertTrue(self.site.gaming_main_page.header.has_right_menu(),
                                msg='User is not automatically logged in to Gaming Lobby') is None
                if res:
                    break
            except Exception as e:
                if attempts:
                    wait_for_haul(5)
                else:
                    raise e

    def test_004_navigate_back_to_oxygen_using_sports_icon_from_gaming_footer(self):
        """
        DESCRIPTION: Navigate back to Oxygen using Sports icon from Gaming Footer
        EXPECTED: * Oxygen app is loaded
        EXPECTED: * User is still logged in
        """
        if self.site.cookie_banner:
            self.site.cookie_banner.ok_button.click()
        footer_menu_item = 'Sports' if self.brand == 'ladbrokes' else 'SPORTS'
        if self.device_type == 'mobile':
            self.site.gaming_main_page.footer.click_item(footer_menu_item)
        else:
            self.site.header.top_menu.click_item(footer_menu_item)
        self.site.wait_splash_to_hide()
        wait_for_result(lambda: tests.HOSTNAME in self.device.get_current_url(),
                        name=f'Url to change to https://{tests.HOSTNAME}/',
                        timeout=2)
        current_url = self.device.get_current_url()
        self.assertIn(tests.HOSTNAME, current_url,
                      msg=f'{tests.HOSTNAME} is not loaded. User is on {current_url}')
        self.site.close_all_banners(async_close=False, timeout=10)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not automatically logged into Oxygen application')

    def test_005_tap_gaming_icon_from_footer(self):
        """
        DESCRIPTION: Tap Gaming icon from Footer
        EXPECTED: * Gaming Lobby is opened
        EXPECTED: * User is logged in to Gaming Lobby
        """
        if self.device_type == 'mobile' and self.site.tutorial_overlay:
            self.site.tutorial_overlay.text_panel.close_button.click()
        self.site.close_all_dialogs(async_close=False, timeout=10)
        self.site.close_all_banners(async_close=False, timeout=10)
        self.test_003_select_gaming_from_sports_selector_ribbon()

    def test_006_log_out_from_gaming_lobby(self):
        """
        DESCRIPTION: Log out from Gaming Lobby
        """
        self.site.gaming_main_page.logout()

    def test_007_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: * Homepage is opened
        EXPECTED: * User is logged out
        """
        self.navigate_to_page(name='/')
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
