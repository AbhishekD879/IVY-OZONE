import pytest
import voltron.environments.constants as vec
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.uat
@pytest.mark.portal_only_test
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870347_Verify_user_is_redirected_to_correct_page_after_clicking_on_the_links_in_the_Right_menu(Common):
    """
    TR_ID: C44870347
    NAME: Verify user is redirected to correct page after clicking on the links in the Right menu.
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def navigate_to_right_menu_item(self, index):
        item = (self.site.right_menu.items)[index]
        item.scroll_to()
        item.click()
        self.site.wait_splash_to_hide(timeout=3)
        self.site.wait_content_state_changed()

    def test_000_preconditions(self):
        """
        DESCRIPTION: log into application.
        EXPECTED: User is logged in the application.
        """
        self.site.login()

    def test_001_click_on_the_avatar_and_click_on_deposit_button_verify(self):
        """
        DESCRIPTION: Click on the Avatar and click on Deposit button. Verify.
        EXPECTED: User is navigated to the deposit page.
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right Menu" is not displayed')
        self.site.right_menu.deposit_button.click()
        self.assertTrue(wait_for_result(lambda: self.site.deposit.deposit_title, timeout=15),
                        msg=f'User is not navigated to "{vec.bma.DEPOSIT}" page')
        self.navigate_to_page('Homepage')

    def test_002_click_on_all_of_the_below_links_and_verify_1_banking_consisting_of_my_balance_deposit_withdraw2_offers__free_bets_consisting_of_sports_free_bets_sports_promotions_gaming_promotios_voucher_codes3_history_consisting_of_betting_history_transaction_history__payment_history4_messages5_connect_consisting_of_shop_exclusive_promos_shop_bet_tracker_football_bet_filter__shop_locator6_settings_consisting_of_my_account_details_change_password_marketing_preferences__betting_settings7_gambling_controls_consisting_of_deposit_limits_time_management__account_closurereopening8_help__contact9_log_out(
            self):
        """
        DESCRIPTION: Click on all of the below links and verify:-
        DESCRIPTION: 1. Banking consisting of My Balance, Deposit, Withdraw
        DESCRIPTION: 2. Offers & Free bets consisting of Sports free bets, Sports promotions, Gaming promotios, Voucher codes
        DESCRIPTION: 3. History consisting of Betting History, Transaction History & Payment History.
        DESCRIPTION: 4. Messages
        DESCRIPTION: 5. Connect consisting of Shop exclusive promos, shop bet tracker, football bet filter & shop locator
        DESCRIPTION: 6. Settings consisting of My account details, change password, marketing preferences & betting settings.
        DESCRIPTION: 7. Gambling controls consisting of Spending Controls, Time management & Account closure/reopening.
        DESCRIPTION: 8. Help & Contact.
        DESCRIPTION: 9. Log out.
        EXPECTED: User is navigated to the corresponding pages.
        """
        self.site.header.right_menu_button.click()
        actual_right_menu = list(self.site.right_menu.items_as_ordered_dict)
        self.assertTrue((item in vec.bma.EXPECTED_LIST_OF_RIGHT_MENU for item in actual_right_menu),
                        msg=f'Actual items: "{actual_right_menu}" are not equal with the '
                            f'Expected items: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU}"')
        right_menu = self.site.right_menu

        # BANKING
        right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0])
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
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        # Coral: MESSAGES, Ladbrokes: Sports Free Bets
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3])
        if self.brand == 'bma':
            actual_title_text = self.site.messages.title.text
            self.assertEqual(actual_title_text, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3],
                             msg=f'Actual text: "{actual_title_text}" is not equal to'
                                 f'Expected text: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3]}"')
            self.site.messages.back_button.click()
        else:
            self.assertTrue(wait_for_result(lambda: self.site.freebets.header_line, timeout=5),
                            msg='User is not navigated to "Free Bets" page')
            self.site.close_all_dialogs(async_close=False, timeout=0.5)
            self.device.go_back()
            self.site.wait_splash_to_hide(timeout=3)
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not displayed')

        # Coral: CONNECT, Ladbrokes: My Bets
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[4])
        if self.brand == 'bma':
            actual_connect_items = list(right_menu.get_items().keys())
            self.assertEqual(actual_connect_items, vec.bma.CONNECT_MENU_ITEMS,
                             msg=f'Actual connect menu items "{actual_connect_items}" is not as same as'
                                 f'Expected connect menu items "{vec.bma.CONNECT_MENU_ITEMS}"')
            right_menu.header.back_button.click()
        else:
            self.assertTrue(wait_for_result(lambda: self.site.open_bets.header_line, timeout=5),
                            msg='User is not navigated to "My Bets" page')
            self.device.go_back()
            self.site.wait_splash_to_hide(timeout=1)
        self.assertTrue(self.site.right_menu.is_displayed(), msg='Right menu is not displayed')

        # Coral: SETTINGS, Ladbrokes: Messages
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[5])
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
            self.site.my_inbox.back_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        # Coral: GAMBLING CONTROLS, Ladbrokes: History
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6])
        self.site.wait_content_state_changed()
        if self.brand == 'bma':
            self.assertTrue(wait_for_result(lambda: self.site.gambling_controls_page.wait_item_appears('Spending Controls'), timeout=20),
                            msg='User is not navigated to "Gambling Controls" page')
            actual_gc_items = list(self.site.gambling_controls_page.get_items().keys())
            self.assertEqual(actual_gc_items, vec.bma.GAMBLING_CONTROLS_MENU_ITEMS,
                             msg=f'Actual gambling controls menu items "{actual_gc_items}" is not as same as'
                                 f'Expected gambling controls menu items "{vec.bma.GAMBLING_CONTROLS_MENU_ITEMS}"')
            self.device.go_back()
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
        if self.brand == 'bma':
            self.assertTrue(wait_for_result(lambda: self.site.direct_chat.topics, timeout=5),
                            msg='User is not navigated to "Help Centre" page')
            self.site.direct_chat.close_button.click()
        else:
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[7],
                             msg='"The Grid" menu is not displayed')
            actual_the_grid_items = list(self.site.right_menu.get_items().keys())
            self.assertEqual(actual_the_grid_items, vec.bma.THE_GRID_MENU_ITEMS,
                             msg=f'Actual the grid menu items "{actual_the_grid_items}" is not as same as'
                                 f'Expected the grid menu items "{vec.bma.THE_GRID_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

        if self.brand == 'ladbrokes':
            # Ladbrokes: Settings
            self.navigate_to_right_menu_item(8)
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[8],
                             msg='"Settings" menu is not displayed')
            actual_settings_items = list(self.site.right_menu.get_items().keys())
            self.assertEqual(actual_settings_items, vec.bma.SETTINGS_MENU_ITEMS,
                             msg=f'Actual settings menu items "{actual_settings_items}" is not as same as'
                                 f'Expected settings menu items "{vec.bma.SETTINGS_MENU_ITEMS}"')
            self.site.right_menu.header.back_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

            # Ladbrokes: Gambling Controls
            self.navigate_to_right_menu_item(9)
            self.assertTrue(wait_for_result(lambda: self.site.gambling_controls_page.wait_item_appears('Spending Controls'),
                                            timeout=20), msg='User is not navigated to "Gambling Controls" page')
            actual_gc_items = list(self.site.gambling_controls_page.get_items().keys())
            self.assertEqual(actual_gc_items, vec.bma.GAMBLING_CONTROLS_MENU_ITEMS,
                             msg=f'Actual gambling controls menu items "{actual_gc_items}" is not as same as'
                                 f'Expected gambling controls menu items "{vec.bma.GAMBLING_CONTROLS_MENU_ITEMS}"')
            self.device.go_back()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')

            # Ladbrokes: Help & Contact
            self.navigate_to_right_menu_item(10)
            self.assertTrue(wait_for_result(lambda: self.site.direct_chat.topics, timeout=5),
                            msg='User is not navigated to "Help Centre" page')
            self.site.direct_chat.close_button.click()
            self.assertTrue(self.site.right_menu.is_displayed(), msg='"Right menu" is not opened')
        # Log Out
        self.site.right_menu.logout()
        self.assertTrue(self.site.wait_logged_out(), "User is not logged out")
