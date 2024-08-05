from time import sleep

import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.gaming
@pytest.mark.sanity
@vtest
class Test_C36377806_Verify_Gaming_Cross_Login(Common):
    """
    TR_ID: C36377806
    NAME: Verify Gaming Cross Login
    DESCRIPTION: This test case verifies that cross Login is working after navigation from BMA to Gaming Lobby
    """
    keep_browser_open = True
    games = vec.sb.GAMING_FOOTER_ITEM
    casino = 'Casino'
    desktop_gaming_display = False
    device_name = 'iPhone XS' if not tests.use_browser_stack else tests.mobile_safari_default

    def verify_redirection_to_gaming_page(self):
        gaming_opened = wait_for_result(lambda: 'gaming' in self.device.get_current_url() or
                                                'games' in self.device.get_current_url(),
                                        timeout=10,
                                        poll_interval=1,
                                        name='Gaming Lobby to be opened')
        self.assertTrue(gaming_opened,
                        msg=f'Gaming Lobby is not opened, instead page {self.device.get_current_url()} is opened')

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')
        if self.device_type == 'desktop':
            # workaround for appearing Sports Selector Ribbon on beta-sports.ladbrokes.com
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Homepage')

    def test_002_log_in_without_remember_me_option(self):
        """
        DESCRIPTION: Log in (without remember me option)
        EXPECTED: Login is successful
        """
        username = tests.settings.betplacement_user
        self.site.login(username=username)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in.')
        self.__class__.oxygen_url = self.device.get_current_url()

    def test_003_select_gaming_from_sports_selector_ribbon(self):
        """
        DESCRIPTION: Select Gaming from Sports Selector Ribbon
        EXPECTED: * Gaming Lobby is opened.
        EXPECTED: * User is automatically logged in to Gaming Lobby.
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
                gaming = footer_navigation_menu.get(self.games)
                if gaming is None:
                    gaming = footer_navigation_menu.get(self.games.upper())
                    if gaming is None:
                        gaming = footer_navigation_menu.get(self.casino)
                        if gaming is None:
                            gaming = footer_navigation_menu.get(self.casino.upper())

            self.assertTrue(gaming, msg=f'"{self.games}" is not found')
            gaming.click()
            sleep(10)
            self.verify_redirection_to_gaming_page()
            self.assertTrue(self.site.gaming_main_page.header.has_right_menu(timeout=10),
                            msg='User is not automatically logged in to Gaming Lobby')

    def test_004_navigate_back_to_oxygen_using_sports_icon_from_gaming_footer(self):
        """
        DESCRIPTION: Navigate back to Oxygen using Sports icon from Gaming Footer
        EXPECTED: * Oxygen app is loaded
        EXPECTED: * User is still logged in
        """
        if self.device_type == 'mobile':
            cookie_banner = self.site.cookie_banner
            if cookie_banner:
                cookie_banner.ok_button.click()
            footer_menu_item = 'Sports' if self.brand == 'ladbrokes' else 'SPORTS'
            try:
                self.site.gaming_main_page.footer.click_item(footer_menu_item)
            except VoltronException:
                self.device.refresh_page()
                self.site.gaming_main_page.footer.click_item(footer_menu_item)
            if 'hlv' in tests.settings.cms_env:
                self.navigate_to_page('/')  # on hl envs click above redirects to the prod env
            self.site.wait_splash_to_hide()
            wait_for_result(lambda: self.device.get_current_url() == self.oxygen_url,
                            name=f'Url to change to https://{tests.HOSTNAME}/',
                            timeout=2)
            current_url = self.device.get_current_url().replace('http://', '').replace('https://', '').replace(
                '?automationtest=true', '')
            self.assertIn(current_url, self.oxygen_url,
                          msg=f'"{self.oxygen_url}" is not loaded. User is on "{current_url}"')
            self.site.close_all_banners(async_close=False, timeout=10)
            self.assertTrue(self.site.wait_logged_in(), msg='User is not automatically logged into Oxygen application')
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=1)
            if dialog:
                dialog.close_dialog()

    def test_005_tap_gaming_icon_from_all_sports(self):
        """
        DESCRIPTION: Tap Gaming icon from Top Sports
        EXPECTED: * Gaming Lobby is opened
        EXPECTED: * User is logged in to Gaming Lobby
        """
        if self.device_type != 'desktop':
            self._logger.warning('*** This step is desktop only, skipping verification for other devices')
            return

        top_items = self.site.header.top_menu.items_as_ordered_dict
        self.assertTrue(top_items, msg='Header menu has no items')
        gaming = top_items.get(self.games)
        if gaming is None:
            gaming = top_items.get(self.games.upper())
            if gaming is None:
                gaming = top_items.get(self.casino)
                if gaming is None:
                    gaming = top_items.get(self.casino.upper())
        self.assertTrue(gaming, msg=f'"{self.games}" menu item not found in "{top_items.keys()}"')

        gaming.click()
        self.verify_redirection_to_gaming_page()
        self.assertTrue(self.site.gaming_main_page.header.has_right_menu(timeout=10),
                        msg='User is not automatically logged in to Gaming Lobby')

    def test_006_tap_gaming_icon_from_footer_menu_mobile_tablet(self):
        """
        DESCRIPTION: Tap Gaming icon from Footer menu (Mobile/Tablet)
        EXPECTED: * Gaming Lobby is opened
        EXPECTED: * User is logged in to Gaming Lobby
        """
        if 'automationtest=true' not in self.device.get_current_url():
            self.device.refresh_page()
        if self.device_type == 'mobile':
            try:
                self.site.navigation_menu.click_item(self.games)
            except Exception:
                self.site.navigation_menu.click_item(self.casino.upper())
            self.verify_redirection_to_gaming_page()
            self.assertTrue(self.site.wait_logged_in(), msg='User is not automatically logged into Gaming lobby')
            self.assertTrue(self.site.gaming_main_page.header.has_right_menu(),
                            msg='User is not automatically logged in to Gaming Lobby')

    def test_007_log_out_from_gaming_lobby(self):
        """
        DESCRIPTION: Log out from Gaming Lobby
        """
        try:
            self.site.gaming_main_page.logout()
        except VoltronException:
            self.device.refresh_page()
            self.site.gaming_main_page.logout()

    def test_008_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: * Homepage is opened.
        EXPECTED: * User is logged out.
        """
        self.navigate_to_page(name='/')
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
