import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from time import sleep


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C57994472_Vanilla_Verify_Right_Menu(Common):
    """
    TR_ID: C57994472
    NAME: [Vanilla] Verify Right Menu
    DESCRIPTION: This test case verifies Right Menu
    """
    keep_browser_open = True

    def navigate_to_right_menu_item(self, index):
        item = (self.site.right_menu.items)[index]
        item.scroll_to()
        item.click()
        self.site.wait_splash_to_hide(timeout=3)
        self.site.wait_content_state_changed()

    def test_001_load_app_and_login(self):
        """
        DESCRIPTION: Load app and login
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_002_click_on_the_avatar_icon_on_the_header(self):
        """
        DESCRIPTION: Click on the avatar icon on the header
        EXPECTED: Mini menu is displayed
        """
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')

    def test_003_verify_menu_items(self):
        """
        DESCRIPTION: Verify Menu Items
        EXPECTED: Menu items (Banking, Offers, History, etc) are clickable.
        EXPECTED: Relevant sub menu or another page is displayed after clicking on menu item.
        """
        actual_right_menu = list(self.site.right_menu.items_as_ordered_dict)
        self.assertTrue((item in vec.bma.EXPECTED_LIST_OF_RIGHT_MENU for item in actual_right_menu),
                        msg=f'Actual items: "{actual_right_menu}" are not equal with the '
                            f'Expected items: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU}"')
        right_menu = self.site.right_menu

        # BANKING
        right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0])
        sleep(2)
        self.assertEqual(right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0],
                         msg='"Banking menu" is not displayed')
        actual_banking_items = list(right_menu.get_items().keys())
        self.assertEqual(actual_banking_items, vec.bma.BANKING_MENU_ITEMS,
                         msg=f'Actual banking menu items "{actual_banking_items}" is not as same as '
                             f'Expected banking menu items "{vec.bma.BANKING_MENU_ITEMS}"')
        right_menu.header.back_button.click()
        self.assertTrue(right_menu.is_displayed(), msg='"Right menu" is not displayed')

        # Coral: OFFERS & FREE BETS, Ladbrokes: Promotions
        right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
        sleep(2)
        actual_menu_items = list(right_menu.get_items().keys())
        if self.brand == 'bma':
            self.assertEqual(actual_menu_items, vec.bma.OFFERS_FREE_BETS_MENU_ITEMS,
                             msg=f'Actual offers & free bets items "{actual_menu_items}" is not as same as '
                                 f'Expected offers & free bets items "{vec.bma.OFFERS_FREE_BETS_MENU_ITEMS}"')
        else:
            self.assertEqual(actual_menu_items, vec.bma.PROMOTIONS_MENU_ITEMS,
                             msg=f'Actual offers & free bets items "{actual_menu_items}" is not as same as '
                                 f'Expected offers & free bets items "{vec.bma.PROMOTIONS_MENU_ITEMS}"')
        right_menu.header.back_button.click()
        self.assertTrue(right_menu.is_displayed(), msg='"Right menu" is not displayed')

        # Coral: HISTORY, Ladbrokes: Odds Boost
        right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2])
        sleep(2)
        if self.brand == 'bma':
            actual_history_items = list(right_menu.get_items().keys())
            self.assertEqual(actual_history_items, vec.bma.HISTORY_MENU_ITEMS,
                             msg=f'Actual history menu items "{actual_history_items}" is not as same as'
                                 f'Expected history menu items "{vec.bma.HISTORY_MENU_ITEMS}"')
            right_menu.header.back_button.click()
        else:
            self.assertTrue(wait_for_result(lambda: self.site.odds_boost_page.header_line, timeout=5),
                            msg='User is not navigated to "Odds Boost" page')
            self.site.close_all_dialogs(async_close=False, timeout=0.5)
            self.device.go_back()
            if self.device_type == 'desktop':
                self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        # Coral: MESSAGES, Ladbrokes: Sports Free Bets
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3])
        sleep(2)
        if self.brand == 'bma':
            actual_title_text = self.site.messages.title.text
            self.assertEqual(actual_title_text, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3],
                             msg=f'Actual text: "{actual_title_text}" is not equal to'
                                 f'Expected text: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3]}"')
            if self.device_type == 'mobile':
                self.site.messages.back_button.click()
            else:
                self.site.messages.close_button.click()
                self.site.header.right_menu_button.click()
                self.site.wait_content_state_changed()
                right_menu = self.site.right_menu
        else:
            self.assertTrue(wait_for_result(lambda: self.site.freebets.header_line, timeout=5),
                            msg='User is not navigated to "Free Bets" page')
            self.site.close_all_dialogs(async_close=False, timeout=0.5)
            self.device.go_back()
            self.site.wait_splash_to_hide(timeout=3)
            if self.device_type == 'desktop':
                self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not displayed')

        # Coral: CONNECT, Ladbrokes: My Bets
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[4])
        sleep(2)
        if self.brand == 'bma':
            actual_connect_items = list(self.site.right_menu.get_items().keys())
            self.assertEqual(actual_connect_items, vec.bma.CONNECT_MENU_ITEMS,
                             msg=f'Actual connect menu items "{actual_connect_items}" is not as same as'
                                 f'Expected connect menu items "{vec.bma.CONNECT_MENU_ITEMS}"')
            right_menu.header.back_button.click()
        else:
            self.assertTrue(wait_for_result(lambda: self.site.open_bets.header_line, timeout=5),
                            msg='User is not navigated to "My Bets" page')
            self.device.go_back()
            self.site.wait_splash_to_hide(timeout=1)
            if self.device_type == 'desktop':
                self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='Right menu is not displayed')

        # Coral: SETTINGS, Ladbrokes: Messages
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[5])
        sleep(2)
        if self.brand == 'bma':
            actual_settings_items = list(right_menu.get_items().keys())
            self.assertEqual(actual_settings_items, vec.bma.SETTINGS_MENU_ITEMS,
                             msg=f'Actual settings menu items "{actual_settings_items}" is not as same as'
                                 f'Expected settings menu items "{vec.bma.SETTINGS_MENU_ITEMS}"')
            right_menu.header.back_button.click()
        else:
            self.assertTrue(wait_for_result(lambda: self.site.my_inbox, timeout=10),
                            msg='User is not navigated to "My Inbox" page')
            self.site.wait_splash_to_hide(timeout=3)
            if self.device_type == 'mobile':
                self.site.my_inbox.back_button.click()
            else:
                self.site.messages.close_button.click()
                self.site.header.right_menu_button.click()
                self.site.wait_content_state_changed()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        # Coral: GAMBLING CONTROLS, Ladbrokes: History
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6])
        self.site.wait_content_state_changed()
        if self.brand == 'bma':
            self.assertTrue(
                wait_for_result(lambda: self.site.gambling_controls_page.wait_item_appears('Spending Controls'),
                                timeout=20),
                msg='User is not navigated to "Gambling Controls" page')
            actual_gc_items = list(self.site.gambling_controls_page.get_items().keys())
            self.assertEqual(actual_gc_items, vec.bma.GAMBLING_CONTROLS_MENU_ITEMS,
                             msg=f'Actual gambling controls menu items "{actual_gc_items}" is not as same as'
                                 f'Expected gambling controls menu items "{vec.bma.GAMBLING_CONTROLS_MENU_ITEMS}"')
            self.device.go_back()
            if self.device_type == 'desktop':
                self.device.refresh_page()
                sleep(3)
                self.site.header.right_menu_button.click()
                self.site.wait_content_state_changed()
        else:
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6],
                             msg='"History" menu is not displayed')
            actual_history_items = list(self.site.right_menu.get_items().keys())
            self.assertEqual(actual_history_items, vec.bma.HISTORY_MENU_ITEMS,
                             msg=f'Actual history menu items "{actual_history_items}" is not as same as'
                                 f'Expected history menu items "{vec.bma.HISTORY_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        # Coral: HELP & CONTACT, Ladbrokes: The Grid
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[7])
        sleep(2)
        if self.brand == 'bma':
            self.assertTrue(wait_for_result(lambda: self.site.direct_chat.topics, timeout=5),
                            msg='User is not navigated to "Help Centre" page')
            if self.device_type == 'mobile':
                self.site.direct_chat.close_button.click()
            else:
                self.device.go_back()
                self.device.refresh_page()
                sleep(3)
                self.site.header.right_menu_button.click()
        else:
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[7],
                             msg='"The Grid" menu is not displayed')
            actual_the_grid_items = list(self.site.right_menu.get_items().keys())
            self.assertEqual(actual_the_grid_items, vec.bma.THE_GRID_MENU_ITEMS,
                             msg=f'Actual the grid menu items "{actual_the_grid_items}" is not as same as'
                                 f'Expected the grid menu items "{vec.bma.THE_GRID_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
            sleep(2)
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')
        if self.brand == 'ladbrokes':
            # Ladbrokes: Settings
            if self.device_type == 'mobile':
                self.navigate_to_right_menu_item(8)
            else:
                item = (self.site.right_menu.items)[8]
                item.click()
                sleep(2)
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[8],
                             msg='"Settings" menu is not displayed')
            actual_settings_items = list(self.site.right_menu.get_items().keys())
            self.assertEqual(actual_settings_items, vec.bma.SETTINGS_MENU_ITEMS,
                             msg=f'Actual settings menu items "{actual_settings_items}" is not as same as'
                                 f'Expected settings menu items "{vec.bma.SETTINGS_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
            sleep(2)
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

            # Ladbrokes: Gambling Controls
            if self.device_type == 'mobile':
                self.navigate_to_right_menu_item(9)
            else:
                item = (self.site.right_menu.items)[9]
                item.click()
                sleep(2)
            self.assertTrue(
                wait_for_result(lambda: self.site.gambling_controls_page.wait_item_appears('Spending Controls'),
                                timeout=30), msg='User is not navigated to "Gambling Controls" page')
            actual_gc_items = list(self.site.gambling_controls_page.get_items().keys())
            self.assertEqual(actual_gc_items, vec.bma.GAMBLING_CONTROLS_MENU_ITEMS,
                             msg=f'Actual gambling controls menu items "{actual_gc_items}" is not as same as'
                                 f'Expected gambling controls menu items "{vec.bma.GAMBLING_CONTROLS_MENU_ITEMS}"')
            self.device.go_back()
            if self.device_type == 'desktop':
                self.device.refresh_page()
                sleep(3)
                self.site.header.right_menu_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

            # Ladbrokes: Help & Contact
            if self.device_type == 'mobile':
                self.navigate_to_right_menu_item(10)
            else:
                item = (self.site.right_menu.items)[10]
                item.click()
                sleep(2)
            self.assertTrue(wait_for_result(lambda: self.site.direct_chat.topics, timeout=5),
                            msg='User is not navigated to "Help Centre" page')
            if self.device_type == 'mobile':
                self.site.direct_chat.close_button.click()
            else:
                self.device.go_back()
                self.device.refresh_page()
                sleep(3)
                self.site.header.right_menu_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')
        # Log Out
        self.site.right_menu.logout()
        self.assertTrue(self.site.wait_logged_out(), "User is not logged out")

    def test_004_verify_sub_menu(self):
        """
        DESCRIPTION: Verify Sub Menu
        EXPECTED: Sub Menu is displayed.
        EXPECTED: Relevant page is displayed after clicking on sub menu item.
        EXPECTED: It is possible to go back to the main menu via Back button.
        """
        # Covered in step 3

    def test_005_verify_menu_closure(self):
        """
        DESCRIPTION: Verify Menu closure
        EXPECTED: Menu and Sub menus can be closed
        """
        # Covered in step 3
