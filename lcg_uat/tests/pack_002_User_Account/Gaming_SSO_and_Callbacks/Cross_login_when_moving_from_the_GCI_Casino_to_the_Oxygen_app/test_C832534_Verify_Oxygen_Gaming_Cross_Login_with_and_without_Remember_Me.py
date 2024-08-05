import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_journey_gaming_x_sell
@pytest.mark.gaming
@pytest.mark.login
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.reg165_fix
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C832534_Verify_Oxygen_Gaming_Cross_Login_with_and_without_Remember_Me(BaseUserAccountTest):
    """
    TR_ID: C832534
    NAME: Verify Oxygen-Gaming Cross Login with and without Remember Me
    DESCRIPTION: This test case verifies that cross Login is working after navigation from BMA to Gaming Lobby with and without Remember Me
    """
    keep_browser_open = True
    gaming_url = None
    blocked_hosts = ['*.goqubit.*']
    device_name = 'iPhone XS'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify gaming URL
        """
        self.__class__.game_menu = vec.sb.GAMING_HEADER_ITEM if self.brand == 'bma' and self.device_type == 'desktop' else vec.sb.GAMING_FOOTER_ITEM
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
        DESCRIPTION: Log in without remember me option
        EXPECTED: Login is successful
        """
        self.site.login(remember_me=False, async_close_dialogs=False, timeout_close_dialogs=5)

    def test_003_navigate_to_gaming_from_sports_selector_ribbon(self):
        """
        DESCRIPTION: Navigate to Gaming from Sports Selector Ribbon
        EXPECTED: Gaming Lobby is opened.
        EXPECTED: The user is automatically logged in to Gaming Lobby.
        """
        if self.device_type == 'mobile':
            menu_carousel = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(menu_carousel, msg='No items on Menu carousel found')
            gaming = menu_carousel.get(self.games)
            if gaming is None:
                gaming = menu_carousel.get(self.games.upper())
            if not gaming:
                footer_navigation_menu = self.site.navigation_menu.items_as_ordered_dict
                self.assertTrue(footer_navigation_menu, msg='No items on Footer navigation found')
                self.__class__.games = next((menu_name for menu_name in footer_navigation_menu if
                                             menu_name.upper().strip() == self.games.upper().strip()), None)
                gaming = footer_navigation_menu.get(self.games)

            self.assertTrue(gaming, msg=f'"{self.games}" is not found')
        else:
            # workaround for appearing Sports Selector Ribbon on beta-sports.ladbrokes.com
            top_items = self.site.header.top_menu.items_as_ordered_dict
            self.assertTrue(top_items, msg='Header menu has no items')
            self.__class__.games = next(
                (menu_name for menu_name in top_items if menu_name.upper().strip() == self.game_menu.upper().strip()), None)
            gaming = top_items.get(self.games)
            self.assertTrue(gaming, msg=f'"{self.games}" menu item not found in "{top_items.keys()}"')
        gaming.click()

        attempts = 5
        while attempts:
            try:
                attempts -= 1
                gaming_opened = wait_for_result(
                    lambda: 'gaming' in self.device.get_current_url() or 'games' in self.device.get_current_url(),
                    timeout=10, poll_interval=1, name='Gaming Lobby to be opened')
                self.assertTrue(
                    gaming_opened,
                    msg=f'Gaming Lobby is not opened, instead page {self.device.get_current_url()} is opened')
                res = self.assertTrue(self.site.gaming_main_page.header.has_right_menu(),
                                      msg='User is not automatically logged in to Gaming Lobby') is None
                if res:
                    break
            except Exception as e:
                if attempts:
                    wait_for_haul(5)
                else:
                    raise e

    def test_004_log_out_from_gaming_lobby(self):
        """
        DESCRIPTION: Log out from Gaming Lobby
        EXPECTED: User is logged out in Gaming Lobby
        """
        attempts = 5
        while attempts:
            attempts -= 1
            is_try_passed = False
            try:
                self.site.gaming_main_page.logout()
                self.device.refresh_page()
                is_try_passed = True
            except Exception as e:
                wait_for_haul(5)
                if not attempts:
                    raise e
            if is_try_passed:
                break
    def test_005_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened.
        EXPECTED: User is logged out
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('Home')
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')

    def test_006_log_in_with_remember_me_option_and_repeat_steps_3_5(self):
        """
        DESCRIPTION: Log in with remember me option and repeat steps #3-5
        EXPECTED: User is logged out
        """
        self.site.login(remember_me=True)

        self.test_003_navigate_to_gaming_from_sports_selector_ribbon()
        self.test_004_log_out_from_gaming_lobby()
        self.test_005_load_oxygen_application()
