import pytest
import tests
from time import sleep
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.desktop
# @pytest.mark.uat
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870403_Verify_my_account_menu_items_navigation(Common):
    """
    TR_ID: C44870403
    NAME: Verify my account menu items navigation
    DESCRIPTION: Verify menu items available under My Account, user will be able to successfully navigate to these respective pages.
    """
    keep_browser_open = True
    password_type = 'password'
    device_name = tests.desktop_default

    def test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://sports.coral.co.uk/ on Chrome browser.
        EXPECTED: https://sports.coral.co.uk/ displayed on Chrome browser.
        """
        self.site.wait_content_state("HomePage")

    def test_002_click_on_login(self):
        """
        DESCRIPTION: Click on Login.
        EXPECTED: Login box appears.
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')

    def test_003_enter_username_and_password(self):
        """
        DESCRIPTION: Enter username and password.
        EXPECTED: User credentials displayed with password masked
        """
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        actual_password_type = self.dialog.password.input_type
        self.assertEqual(actual_password_type, self.password_type,
                         msg=f'Actual password type: "{actual_password_type}" is not equal with the'
                             f'Expected password type: "{self.password_type}"')

    def test_004_click_on_login(self):
        """
        DESCRIPTION: Click on Login.
        EXPECTED: User logged in successfully
        """
        self.dialog.click_login()
        dialog_closed = self.dialog.wait_dialog_closed()
        self.assertTrue(dialog_closed, msg='"Login dialog" is not closed')
        self.site.wait_content_state('HomePage')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')

    def test_005_click_on_avatar_my_account(self):
        """
        DESCRIPTION: Click on Avatar (My Account)
        EXPECTED: Menu item links are available.
        """
        self.device.refresh_page()
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        self.site.right_menu.deposit_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(wait_for_result(lambda: self.site.deposit.deposit_title, timeout=15),
                        msg=f'User is not navigated to "{vec.bma.DEPOSIT}" page')
        self.site.deposit.close_button.click()
        self.navigate_to_page('Homepage')
        self.site.header.right_menu_button.click()

    def test_006_verify_menu_item_links_availablebankingoffers__free_betshistorymessagesconnectsettingsgambling_controlshelp__contactlog_outdeposit(self):
        """
        DESCRIPTION: Verify menu item links available:
        DESCRIPTION: Banking
        DESCRIPTION: Offers & Free bets
        DESCRIPTION: History
        DESCRIPTION: Messages
        DESCRIPTION: Connect
        DESCRIPTION: Settings
        DESCRIPTION: Gambling Controls
        DESCRIPTION: Help & Contact
        DESCRIPTION: Log out
        DESCRIPTION: Deposit
        EXPECTED: Menu item links available:
        EXPECTED: Banking
        EXPECTED: Offers & Free bets
        EXPECTED: History
        EXPECTED: Messages
        EXPECTED: Connect
        EXPECTED: Settings
        EXPECTED: Gambling Controls
        EXPECTED: Help & Contact
        EXPECTED: Log out
        EXPECTED: Deposit
        """
        actual_right_menu = list(self.site.right_menu.items_as_ordered_dict)
        self.assertTrue((item in vec.bma.EXPECTED_LIST_OF_RIGHT_MENU for item in actual_right_menu),
                        msg=f'Actual right menu items: "{actual_right_menu}"'
                            f' are not same as Expected right menu items: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU}"')
        actual_deposit_and_log_out = [self.site.right_menu.deposit_button.text, self.site.right_menu.log_out_button.text]
        if self.brand == 'bma':
            expectd_deposit_and_log_out = [vec.bma.DEPOSIT.upper(), vec.bma.LOG_OUT.upper()]
        else:
            expectd_deposit_and_log_out = [vec.bma.DEPOSIT.upper(), vec.bma.LOG_OUT]
        self.assertEqual(actual_deposit_and_log_out, expectd_deposit_and_log_out,
                         msg=f'Actual items: "{actual_deposit_and_log_out}" are not equal with the'
                             f'Expected items: "{expectd_deposit_and_log_out}"')

    def test_007_navigate_to_banking(self):
        """
        DESCRIPTION: Navigate to Banking.
        EXPECTED: Banking page displayed:
        EXPECTED: My Balance
        EXPECTED: Deposit
        EXPECTED: Withdraw
        """
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0])
        self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0],
                         msg='"Banking menu" is not displayed')
        actual_banking_menu = list(self.site.right_menu.items_as_ordered_dict)
        self.assertEqual(actual_banking_menu, vec.bma.BANKING_MENU_ITEMS,
                         msg=f'Actual items: "{actual_banking_menu}" are not equal with the'
                             f'Expected items: "{vec.bma.BANKING_MENU_ITEMS}"')

    def test_008_click_on_back__button(self):
        """
        DESCRIPTION: Click on back (<) button
        EXPECTED: Navigated back to Menu links
        """
        self.site.wait_splash_to_hide(timeout=5)
        self.assertTrue(self.site.right_menu.header.back_button.is_displayed(), msg='"Back button" is not present')
        self.site.right_menu.header.back_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

    def test_009_click_on_history(self):
        """
        DESCRIPTION: Click on History.
        EXPECTED: Betting History
        EXPECTED: Transaction History
        EXPECTED: Payment History
        """
        # Coral: HISTORY, Ladbrokes: Odds Boost
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2])
        sleep(1)
        if self.brand == 'bma':
            actual_history_items = list(self.site.right_menu.items_as_ordered_dict)
            self.assertEqual(actual_history_items, vec.bma.HISTORY_MENU_ITEMS,
                             msg=f'Actual history menu items "{actual_history_items}" is not as same as'
                                 f'Expected history menu items "{vec.bma.HISTORY_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
        else:
            self.assertTrue(wait_for_result(lambda: self.site.odds_boost_page.header_line, timeout=5),
                            msg='User is not navigated to "Odds Boost" page')
            self.site.close_all_dialogs(async_close=False, timeout=0.5)
            self.device.go_back()
            sleep(1)
            self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

    def test_010_repeat_above_steps_for_all_menu_items_available(self):
        """
        DESCRIPTION: Repeat above steps for all menu items available.
        EXPECTED: Respective menu items display and user is able to navigate between them.
        """
        # Coral: OFFERS & FREE BETS, Ladbrokes: Promotions
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
        sleep(1)
        actual_menu_items = list(self.site.right_menu.items_as_ordered_dict)
        if self.brand == 'bma':
            self.assertTrue((item in vec.bma.OFFERS_FREE_BETS_MENU_ITEMS for item in actual_menu_items),
                            msg=f'Actual offers & free bets items: "{actual_menu_items}"'
                                f' are not same as Expected offers & free bets items: "{vec.bma.OFFERS_FREE_BETS_MENU_ITEMS}"')
        else:
            self.assertEqual(actual_menu_items, vec.bma.PROMOTIONS_MENU_ITEMS,
                             msg=f'Actual Promotions items "{actual_menu_items}" is not as same as '
                                 f'Expected Promotions items "{vec.bma.PROMOTIONS_MENU_ITEMS}"')
        self.site.right_menu.header.back_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not displayed')

        # Coral: MESSAGES, Ladbrokes: Sports Free Bets
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3])
        sleep(1)
        if self.brand == 'bma':
            actual_title_text = self.site.messages.title.text
            self.assertEqual(actual_title_text, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3],
                             msg=f'Actual text: "{actual_title_text}" is not equal to'
                                 f'Expected text: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3]}"')
            self.site.messages.close_button.click()
        else:
            self.site.wait_content_state_changed()
            self.assertTrue(wait_for_result(lambda: self.site.freebets.header_line, timeout=20),
                            msg='User is not navigated to "Free Bets" page')
            self.site.close_all_dialogs(async_close=False, timeout=0.5)
            self.device.go_back()
            sleep(1)
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not displayed')

        # Coral: CONNECT, Ladbrokes: My Bets
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[4])
        sleep(1)
        if self.brand == 'bma':
            actual_connect_items = list(self.site.right_menu.items_as_ordered_dict)
            self.assertTrue(set(vec.bma.CONNECT_MENU_ITEMS).issubset(actual_connect_items),
                            msg=f'Actual items: "{actual_connect_items}" are not equal with the'
                                f'Expected items: "{vec.bma.CONNECT_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
        else:
            self.assertTrue(wait_for_result(lambda: self.site.open_bets.header_line, timeout=5),
                            msg='User is not navigated to "My Bets" page')
            self.device.go_back()
            sleep(1)
            self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right Menu" is not displayed')

        # Coral: SETTINGS, Ladbrokes: Messages
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[5])
        sleep(1)
        if self.brand == 'bma':
            actual_settings_items = list(self.site.right_menu.items_as_ordered_dict)
            self.assertEqual(actual_settings_items, vec.bma.SETTINGS_MENU_ITEMS,
                             msg=f'Actual settings menu items "{actual_settings_items}" is not as same as'
                                 f'Expected settings menu items "{vec.bma.SETTINGS_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
        else:
            self.assertTrue(wait_for_result(lambda: self.site.my_inbox, timeout=5),
                            msg='User is not navigated to "My Inbox" page')
            self.site.wait_splash_to_hide(timeout=3)
            self.site.my_inbox.close_button.click()
            self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        # Coral: GAMBLING CONTROLS, Ladbrokes: History
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6])
        self.site.wait_content_state_changed()
        if self.brand == 'bma':
            self.assertTrue(wait_for_result(lambda: self.site.gambling_controls_page.wait_item_appears('Spending Controls'), timeout=20),
                            msg='User is not navigated to "Gambling Controls" page')
            actual_gc_items = list(self.site.gambling_controls_page.items_as_ordered_dict)
            self.assertEqual(actual_gc_items, vec.bma.GAMBLING_CONTROLS_MENU_ITEMS,
                             msg=f'Actual gambling controls menu items "{actual_gc_items}" is not as same as'
                                 f'Expected gambling controls menu items "{vec.bma.GAMBLING_CONTROLS_MENU_ITEMS}"')
            self.device.go_back()
            self.site.header.right_menu_button.click()
        else:
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6],
                             msg='"History" menu is not displayed')
            actual_history_items = list(self.site.right_menu.items_as_ordered_dict)
            self.assertEqual(actual_history_items, vec.bma.HISTORY_MENU_ITEMS,
                             msg=f'Actual history menu items "{actual_history_items}" is not as same as'
                                 f'Expected history menu items "{vec.bma.HISTORY_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        # Coral: HELP & CONTACT, Ladbrokes: The Grid
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[7])
        if self.brand == 'bma':
            self.assertTrue(wait_for_result(lambda: self.site.direct_chat.topics, timeout=5),
                            msg='User is not navigated to "Help Centre" page')
            self.device.go_back()
            self.site.header.right_menu_button.click()
        else:
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[7],
                             msg='"The Grid" menu is not displayed')
            actual_the_grid_items = list(self.site.right_menu.items_as_ordered_dict)
            self.assertEqual(actual_the_grid_items, vec.bma.THE_GRID_MENU_ITEMS,
                             msg=f'Actual the grid menu items "{actual_the_grid_items}" is not as same as'
                                 f'Expected the grid menu items "{vec.bma.THE_GRID_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        if self.brand == 'ladbrokes':
            # Ladbrokes: Settings
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[8])
            self.site.wait_content_state_changed(timeout=2)
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[8],
                             msg='"Settings" menu is not displayed')
            actual_settings_items = list(self.site.right_menu.items_as_ordered_dict)
            self.assertEqual(actual_settings_items, vec.bma.SETTINGS_MENU_ITEMS,
                             msg=f'Actual settings menu items "{actual_settings_items}" is not as same as'
                                 f'Expected settings menu items "{vec.bma.SETTINGS_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

            # Ladbrokes: Spending Controls.
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[9])
            self.assertTrue(wait_for_result(lambda: self.site.gambling_controls_page.wait_item_appears('Spending Controls'),
                                            timeout=5), msg='"Spending Controls." is not displayed ')
            actual_gc_items = list(self.site.gambling_controls_page.items_as_ordered_dict)
            self.assertEqual(actual_gc_items, vec.bma.GAMBLING_CONTROLS_MENU_ITEMS,
                             msg=f'Actual gambling controls menu items "{actual_gc_items}" is not as same as'
                                 f'Expected gambling controls menu items "{vec.bma.GAMBLING_CONTROLS_MENU_ITEMS}"')
            self.device.go_back()
            sleep(1)
            self.site.header.right_menu_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

            # Ladbrokes: Help & Contact
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[10])
            self.assertTrue(wait_for_result(lambda: self.site.direct_chat.topics, timeout=5),
                            msg='User is not navigated to "Help Centre" page')
            self.device.go_back()
            sleep(1)
            self.site.header.right_menu_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        # Log Out
        self.site.right_menu.logout()
        self.assertTrue(self.site.wait_logged_out(), "User is not logged out")
