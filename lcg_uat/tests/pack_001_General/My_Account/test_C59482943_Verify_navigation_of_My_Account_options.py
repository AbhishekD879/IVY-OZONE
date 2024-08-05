from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from time import sleep
import voltron.environments.constants as vec
import pytest
import tests


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.navigation
@vtest
class Test_C59482943_Verify_navigation_of_My_Account_options(Common):
    """
    TR_ID: C59482943
    NAME: Verify navigation of  'My Account' options
    DESCRIPTION: This test case verifies opening the correct pages by clicking/tapping on 'My Account' options.
    DESCRIPTION: **Note:**
    DESCRIPTION: My Account Menu or User Menu is handled and set on GVC side.
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Log in with valid credentials
    PRECONDITIONS: 3. Make sure that the 'My Account' button is displayed on Header with 'FB' icon available when the user has free bets
    PRECONDITIONS: 4. Click/Tap the 'My Account' button on the Header
    PRECONDITIONS: 5. Make sure that 'My Account' is opened and contains the following items:
    PRECONDITIONS: **Coral**
    PRECONDITIONS: * 'Menu' title and 'Close' button
    PRECONDITIONS: * Banking
    PRECONDITIONS: * Offers & Free Bets
    PRECONDITIONS: * History
    PRECONDITIONS: * Messages
    PRECONDITIONS: * Connect
    PRECONDITIONS: * Settings
    PRECONDITIONS: * Gambling Controls
    PRECONDITIONS: * Help & Contact
    PRECONDITIONS: * Log Out
    PRECONDITIONS: * Green'DEPOSIT' button
    PRECONDITIONS: **Ladbrokes**
    PRECONDITIONS: * 'Menu' title and 'Close' button
    PRECONDITIONS: * Banking & Balances
    PRECONDITIONS: * Promotions
    PRECONDITIONS: * Odds Boosts
    PRECONDITIONS: * Sports Free Bets
    PRECONDITIONS: * My Bets
    PRECONDITIONS: * Messages
    PRECONDITIONS: * History
    PRECONDITIONS: * The Grid
    PRECONDITIONS: * Settings
    PRECONDITIONS: * Gambling Controls
    PRECONDITIONS: * Help & Contact
    PRECONDITIONS: * Log Out
    PRECONDITIONS: * Green'DEPOSIT' button
    """
    keep_browser_open = True
    connect_menu_names_with_condition = []
    device_name = 'Desktop Chrome' if not tests.use_browser_stack else tests.desktop_default

    def items_loaded(self, expression, item_to_wait=None):
        bypass_exceptions = (NoSuchElementException, StaleElementReferenceException, VoltronException)
        if item_to_wait:
            wait_for_result(lambda: item_to_wait in expression(),
                            timeout=15,
                            name=f'Item "{item_to_wait}" to be present',
                            bypass_exceptions=bypass_exceptions)
        return wait_for_result(expression,
                               timeout=15,
                               name='Items are loaded',
                               bypass_exceptions=bypass_exceptions)

    def verify_items(self, item_names, right_menu_name, promo_external_link=None):
        def verify_item(menu_item_name):
            # We have to re-initialize items every time as page is reloaded later during verifications
            self.items_loaded(lambda: self.site.menus.items_as_ordered_dict, item_to_wait=menu_item_name)
            items = self.site.menus.items_as_ordered_dict
            self.assertTrue(items, msg='Cannot get My Account Menu items')
            menu_item = items.get(menu_item_name)
            self.assertTrue(menu_item, msg=f'"{menu_item_name}" was not found in "{items.keys()}"')

            self._logger.info(f'*** Opening menu item "{menu_item_name}"')
            menu_item.click()
            self.assertTrue(wait_for_result(lambda: menu_item.get_header, timeout=15), msg=f'header is not displayed')
            header_wrapper = menu_item.get_header
            current_url = self.device.get_current_url()
            if 'promo/offers' in current_url and promo_external_link:
                self.assertEqual(
                    current_url, promo_external_link,
                    msg=f'Actual Gaming promotions external link "{current_url}" != Expected "{promo_external_link}')
                self.navigate_to_page(name='/')
            else:
                self.assertTrue(wait_for_result(lambda: header_wrapper.header, timeout=15),
                                msg=f'header is not displayed')
                header = header_wrapper.header
                self.assertTrue(header.page_title.is_displayed(), msg=f'"{menu_item_name}" page is not opened')
                dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, timeout=1)
                if dialog:
                    dialog.close_dialog()
                header.back_button.click()

            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='Homepage')
            wait_for_result(
                lambda: self.site.header.has_right_menu() and self.site.header.right_menu_button.is_displayed(timeout=1),
                timeout=2,
                name='Right Menu button to be displayed')
            self.site.header.right_menu_button.click()
            self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
            self.site.right_menu.click_item(item_name=right_menu_name)

        for item_name in item_names:
            if item_name in self.connect_menu_names_with_condition:
                break
            verify_item(item_name)

    def open_right_menu(self):
        self.navigate_to_page(name='/')
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')

    def test_000_precondition(self):
        """
        DESCRIPTION: Load Oxygen app and login
        EXPECTED: * User is logged in successfully
        EXPECTED: * [My Account] button is displayed on Header with 'FB' icon available when user has freebets
        """
        if tests.settings.backend_env != 'prod':
            username = tests.settings.betplacement_user
            self.ob_config.grant_freebet(username=username)
            self.site.login(username=username)
            self.assertTrue(self.site.header.user_panel.my_account_button.has_freebet_icon(),
                            msg='"FB" icon is not available')
        else:
            self.site.login()
            self.site.close_all_dialogs()

        self.assertTrue(self.site.header.right_menu_button.is_displayed(),
                        msg='[My Account] button is not displayed on Header')

        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        my_account_menu = self.site.window_client_config.get_gvc_config_item(key_title='type', value_title='menu')
        self.__class__.get_gvc_menu_items = {}
        for item in my_account_menu.get('children'):
            if item.get('name') != 'gamblingcontrols_inshop' and item.get('menuRoute') != 'menu/vip':
                if 'children' in item.keys():
                    self.get_gvc_menu_items.setdefault('with_arrow', [])
                    self.get_gvc_menu_items['with_arrow'].append(item.get('text').upper() if self.brand == 'bma' else item.get('text'))
                else:
                    self.get_gvc_menu_items.setdefault('without_arrow', [])
                    self.get_gvc_menu_items['without_arrow'].append(item.get('text').upper() if self.brand == 'bma' else item.get('text'))

        self.__class__.actual_menu_items = self.items_loaded(lambda: self.site.right_menu.items_names)
        expected_menu_items = []
        for value in self.get_gvc_menu_items.values():
            expected_menu_items += value
        if self.brand == 'bma':
            if expected_menu_items.__contains__('LOSS LIMIT'):
                expected_menu_items.remove('LOSS LIMIT')
        else:
            if expected_menu_items.__contains__('Loss Limit'):
                expected_menu_items.remove('Loss Limit')
        self.assertEqual(sorted(self.actual_menu_items), sorted(expected_menu_items),
                         msg=f'Actual Menu items "{sorted(self.actual_menu_items)}" != '
                             f'Expected "{sorted(expected_menu_items)}')
        self.assertTrue(self.site.right_menu.has_deposit_button(), msg='Deposit button is not displayed')

    def test_001_clicktap_on_bankingbanking__balances_item(self):
        """
        DESCRIPTION: Click/Tap on 'Banking'/'Banking & Balances' item
        EXPECTED: 'Banking'/'Banking & Balances' Menu is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * My balance
        EXPECTED: * Deposit
        EXPECTED: * Withdraw
        EXPECTED: ![](index.php?/attachments/get/115420271)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * My balance
        EXPECTED: * Deposit
        EXPECTED: * Transfer
        EXPECTED: * Withdraw
        EXPECTED: * Payment History
        EXPECTED: ![](index.php?/attachments/get/115420277)
        """
        self.__class__.cashier_menu_title = self.site.window_client_config.cashier_menu_title
        self.site.right_menu.click_item(item_name=self.cashier_menu_title)
        expected_banking_items = self.site.window_client_config.get_gvc_config_item(key_title='name',
                                                                                    value_title='cashieritems')
        expected_banking_title = []
        for item in expected_banking_items.get('children'):
            if item.get('name') != 'deposit_inshop' and item.get('name') != 'withdraw_inshop':
                expected_banking_title.append(item.get('text').upper() if self.brand == 'bma' else item.get('text'))
        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=expected_banking_title[0])
        self.assertTrue(set(sections) == set(expected_banking_title),
                        msg=f'Actual Menu items "{sections}" != Expected "{expected_banking_title}')

    def test_002_clicktap_my_balance_item_and_verify_overlaypop_up_view(self):
        """
        DESCRIPTION: Click/Tap 'My balance' item and verify Overlay/Pop-up view
        EXPECTED: 'My Balance' Overlay/Pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Withdrawable-online
        EXPECTED: * Restricted
        EXPECTED: * Available balance
        EXPECTED: * Total Balance
        EXPECTED: * Deposit Button
        EXPECTED: * 'Available to use on' table
        EXPECTED: ![](index.php?/attachments/get/115420294)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Withdrawable-online
        EXPECTED: * Available balance
        EXPECTED: * Total Balance
        EXPECTED: * Deposit Button
        EXPECTED: * 'Available to use on' table
        EXPECTED: ![](index.php?/attachments/get/115420297)
        """
        my_balance_text = self.site.window_client_config.get_gvc_config_item_text(key_title='name',
                                                                                  value_title='balance')
        self.site.right_menu.click_item(item_name=my_balance_text)
        sections = self.site.right_menu.my_balance.items_names
        right_menu_deposit_items = self.site.window_client_config.get_gvc_config_item(key_title='menuRoute',
                                                                                      value_title='menu/balance')
        my_balance_items = self.site.window_client_config.get_gvc_config_item(key_title='name',
                                                                              value_title='balanceitems',
                                                                              context=right_menu_deposit_items)
        expected_my_balance_title = []
        for item in my_balance_items.get('children'):
            if item.get('name') != 'inplay' and item.get('name') != 'withdrawableinshop' and \
                    item.get('name') != 'negative' and item.get('name') != 'restricted':
                expected_my_balance_title.append(item.get('text').upper() if self.brand == 'bma' else item.get('text'))
        # 'restricted' item is skipped as we cannot identify whether it'll be displayed
        status = all(item in sections for item in expected_my_balance_title)

        self.assertTrue(status,
                        msg=f'Actual Menu items "{set(sections)}" != Expected "{set(expected_my_balance_title)}')

        self.assertTrue(self.site.right_menu.my_balance.deposit_button.is_displayed(),
                        msg='Deposit button is not present')
        self.assertTrue(self.site.right_menu.my_balance.available_to_use.is_displayed(),
                        msg='Available to use on table is not present')

    def test_003_clicktap_back__button_on_header_and_check_deposit_and_withdraw_item_navigation(self):
        """
        DESCRIPTION: Click/Tap 'Back' ('<') button on header and check 'Deposit' and 'Withdraw' item navigation
        EXPECTED: * Clicking on Deposit opens deposit Overlay/pop-up
        EXPECTED: * Clicking on Withdraw opens Withdraw Overlay
        """
        self.site.right_menu.my_balance.header.back_button.click()
        if self.device_type == 'desktop':
            self.items_loaded(lambda: self.site.right_menu.items_names,
                              item_to_wait=self.cashier_menu_title)
            self.site.right_menu.click_item(item_name=self.cashier_menu_title)
        self.items_loaded(lambda: self.site.right_menu.items_names,
                          item_to_wait=self.site.window_client_config.deposit_menu_title)
        self.site.right_menu.click_item(item_name=self.site.window_client_config.deposit_menu_title)
        self.site.wait_splash_to_hide()
        self.assertTrue(self.site.deposit.is_displayed(), msg='"Deposit" menu is not displayed')

        self.open_right_menu()
        self.site.right_menu.click_item(item_name=self.cashier_menu_title)

        withdraw_text = self.site.window_client_config.get_gvc_config_item_text(key_title='name',
                                                                                value_title='withdraw')
        self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=withdraw_text)
        self.site.right_menu.click_item(item_name=withdraw_text)
        sleep(10)
        self.assertTrue(self.site.menus.withdrawal.is_displayed(), msg='Withdraw Overlay is not opened')

    def test_004__go_back_and_open_my_account_menu_clicktap_on_offers__free_betspromotions_item(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Offers & Free Bets'/'Promotions' item
        EXPECTED: 'Offers'/'Promotions' Overlay/Pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Odds Boost
        EXPECTED: * Sports Free Bets
        EXPECTED: * Sports Promotions
        EXPECTED: * Gaming Promotions
        EXPECTED: * Voucher Code
        EXPECTED: ![](index.php?/attachments/get/39224046)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Free Bets
        EXPECTED: * Odds Boost
        EXPECTED: * Sports Promotions
        EXPECTED: * Gaming Promotions
        EXPECTED: ![](index.php?/attachments/get/115421347)
        """
        wait_for_result(lambda: self.site.menus.withdrawal.header.close_button.is_displayed(), timeout=15)
        self.site.menus.withdrawal.header.close_button.click()

        self.open_right_menu()

        self.site.right_menu.click_item(item_name=self.site.window_client_config.offers_menu_title)
        offers_items = self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='offeritems')
        offer_menu_names = [item.get('text').upper() if self.brand == 'bma' else item.get('text')
                            for item in offers_items.get('children')]
        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=offer_menu_names[0])
        self.assertEqual(set(sections), set(offer_menu_names),
                         msg=f'Actual Menu items "{sections}" != Expected "{offer_menu_names}')

    def test_005_verify_every_item_menu_navigation_by_clickingtapping_on_it(self):
        """
        DESCRIPTION: Verify every item menu navigation by clicking/tapping on it
        EXPECTED: **Coral**
        EXPECTED: * Odds Boost opens Odds Boost page
        EXPECTED: * Sports Free Bets opens Freebets page
        EXPECTED: * Sports Promotions opens Promotions page
        EXPECTED: * Gaming Promotions opens Gaming promotions (external https://beta-promo.coral.co.uk/en/promo/offers)
        EXPECTED: * Voucher Code opens Voucher page (https://beta-sports.coral.co.uk/voucher-code)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Free Bets opens Free Bets page
        EXPECTED: * Odds Boost opens Odds Boost page
        EXPECTED: * Sports Promotions opens Promotions page
        EXPECTED: * Gaming Promotions opens Gaming promotions (external https://promo.ladbrokes.com/en/promo/offers)
        """
        value = 'myrewards' if self.brand == 'bma' else 'gamingpromotions'
        promo_configuration = self.site.window_client_config.get_gvc_config_item(
            key_title='name', value_title=value)
        promo_external_link = promo_configuration.get('url')
        if not promo_external_link:
            raise VoltronException('Cannot get Gaming promotions external link')
        item_names = self.site.menus.items_names
        self.site.close_all_dialogs()
        self.verify_items(item_names, self.site.window_client_config.offers_menu_title, promo_external_link)

    def test_006_ladbrokes_go_back_and_open_my_account_menu_clicktap_on_sports_free_bets_item(self):
        """
        DESCRIPTION: **Ladbrokes**
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Sports Free Bets' item
        EXPECTED: 'Sports Free Bets' opens Free Bets page
        """

        if self.site.brand == 'ladbrokes':
            self.open_right_menu()
            self.site.right_menu.click_item(item_name='Sports Free Bets')
            sports_free_bet_configuration = self.site.window_client_config.get_gvc_config_item(
                key_title='name', value_title='sportsfreebets')
            sports_free_bet_external_link = sports_free_bet_configuration.get('url')
            self.assertIn('/freebets', sports_free_bet_external_link)

    def test_007_ladbrokes_go_back_and_open_my_account_menu_clicktap_on_odds_boosts_item(self):
        """
        DESCRIPTION: **Ladbrokes**
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Odds Boosts' item
        EXPECTED: 'Odds Boosts' opens Odds Boosts page
        """
        if self.site.brand == 'ladbrokes':
            self.open_right_menu()
            self.site.right_menu.click_item(item_name='Odds Boosts')
            sports_free_bet_configuration = self.site.window_client_config.get_gvc_config_item(
                key_title='name', value_title='oddsboost')
            sports_free_bet_external_link = sports_free_bet_configuration.get('url')
            self.assertIn('/oddsboost', sports_free_bet_external_link)

    def test_008_ladbrokes_go_back_and_open_my_account_menu_clicktap_on_my_bets_item(self):
        """
        DESCRIPTION: **Ladbrokes**
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'My Bets' item
        EXPECTED: 'My Bets' opens My Bets page
        """
        if self.site.brand == 'ladbrokes':
            self.open_right_menu()
            self.site.right_menu.click_item(item_name='My Bets')
            sports_free_bet_configuration = self.site.window_client_config.get_gvc_config_item(
                key_title='name', value_title='mybets')
            sports_free_bet_external_link = sports_free_bet_configuration.get('text')
            self.assertIn('My Bets', sports_free_bet_external_link)
            sleep(5)

    def test_009__go_back_and_open_my_account_menu_clicktap_on_history_item(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click/Tap on 'History' item
        EXPECTED: 'History' Overlay/pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Betting History
        EXPECTED: * Transaction History
        EXPECTED: * Payment History
        EXPECTED: ![](index.php?/attachments/get/115421428)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Betting History
        EXPECTED: * Payment History
        EXPECTED: * Transactions History
        EXPECTED: ![](index.php?/attachments/get/115421452)
        """
        self.open_right_menu()
        history_config = self.site.window_client_config.get_gvc_config_item(
            key_title='name', value_title='history')
        self.__class__.history_title = history_config.get('text').upper()
        self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=self.history_title)
        self.site.right_menu.click_item(item_name=self.history_title)
        history_items = self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='historyitems')
        history_menu_names = [item.get('text').upper() if self.brand == 'bma' else item.get('text') for item in
                              history_items.get('children')]
        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=history_menu_names[0])
        self.assertEqual(set(sections), set(history_menu_names),
                         msg=f'Actual Menu items "{sections}" != Expected "{history_menu_names}')

    def test_010_verify_every_item_menu_navigation_by_clickingtapping_on_it(self):
        """
        DESCRIPTION: Verify every item menu navigation by clicking/tapping on it
        EXPECTED: * Betting History opens Settled Bets page/tab
        EXPECTED: * Transaction History opens Gaming history ( e.g. https://beta-sports.coral.co.uk/en/mobileportal/transactions)
        EXPECTED: * Payment History opens Payment history page ( e.g. https://cashier.coral.co.uk/home/txnSearchPageMerchant.action?sessionKey=198d8026e07f487fb348c516cc3d355a&LANG_ID=en&parent=https://beta-sports.coral.co.uk/)
        """
        self.__class__.history_title = self.site.window_client_config.get_gvc_config_item_text(key_title='name',
                                                                                               value_title='history')
        betting_text = self.site.window_client_config.get_gvc_config_item_text(key_title='name', value_title='betting')
        transaction_text = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='transaction')
        payment_text = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='payment')

        def get_header_wrapper(config_text):
            self.items_loaded(lambda: self.site.menus.items_names, item_to_wait=config_text)
            items = self.site.menus.items_as_ordered_dict
            self.assertTrue(items, msg='Cannot get History Overlay items')
            menu_item = items.get(config_text)
            self.assertTrue(menu_item, msg=f'"{config_text} was not found in "{items.keys()}"')
            menu_item.click()
            self.assertTrue(wait_for_result(lambda: menu_item.get_header, timeout=15), msg=f'header is not displayed')
            header_wrapper = menu_item.get_header
            return header_wrapper

        header_wrapper = get_header_wrapper(betting_text)
        header = header_wrapper.header
        self.assertTrue(header.page_title.is_displayed(), msg=f'"{betting_text}" page is not opened')
        header.back_button.click()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')

        self.open_right_menu()
        self.site.right_menu.click_item(item_name=self.history_title)
        header_wrapper = get_header_wrapper(transaction_text)
        if self.device_type == 'desktop':
            transaction_text = self.site.window_client_config.mobile_portal_transaction_history
            self.assertEquals(header_wrapper.transactions_left_nav_menu.active_link.text, transaction_text,
                              msg=f'Actual name "{header_wrapper.transactions_left_nav_menu.active_link.text}" != '
                                  f'Expected name "{transaction_text}"')
            items = header_wrapper.transactions_left_nav_menu.items_as_ordered_dict
            payment_transaction_item = items.get(transaction_text)
            self.assertTrue(payment_transaction_item,
                            msg=f'Item "{transaction_text}" is not found in "{items.keys()}"')
            payment_transaction_item.click()
            actual_text = header_wrapper.transactions_left_nav_menu.active_link.text
            self.assertEquals(actual_text, transaction_text,
                              msg=f'Actual "{actual_text}" != Expected "{transaction_text}"')
            self.navigate_to_page(name='/')
        else:
            self.assertTrue(header_wrapper.specific_header.is_displayed(timeout=3),
                            msg=f'"{transaction_text}" page is not opened')
            header_wrapper.specific_header.back_button.click()
            self.assertTrue(self.site.is_right_menu_opened(timeout=3), msg='Failed to open My Account Menu')

            header_wrapper = get_header_wrapper(payment_text)
            self.assertTrue(header_wrapper.payment_history_header.is_displayed(),
                            msg=f'"{payment_text}" page is not opened')
            header_wrapper.payment_history_header.close_button.click()

    def test_011__go_back_and_open_my_account_menu_clicktap_on_messages_item(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Messages' item
        EXPECTED: 'Messages' overlay/pop-up is opened with rich inbox messages available or 'You have no messages!' in case messages are not available
        """
        self.open_right_menu()
        right_menu_messages_title = self.site.window_client_config.messages_title
        items = self.site.menus.items_as_ordered_dict
        self.assertTrue(items, msg='Cannot get My Account Menu items')
        inbox = items.get(right_menu_messages_title)
        self.assertTrue(inbox, msg=f'"{right_menu_messages_title} was not found in "{items.keys()}"')
        inbox.click()
        sleep(5)
        self.assertTrue(wait_for_result(lambda: inbox.get_header, timeout=15), msg=f'header is not displayed')
        self.__class__.header_wrapper = inbox.get_header
        self.assertTrue(self.header_wrapper.inbox_header.is_displayed(), msg=f'"{right_menu_messages_title}" page is not opened')

    def test_012__go_back_and_open_my_account_menu_clicktap_on_connectthe_grid_item(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Connect'/'The Grid' item
        EXPECTED: 'Connect' Overlay/pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * Shop Exclusive Promos
        EXPECTED: * Shop Bet Tracker
        EXPECTED: * Football Bet Filter
        EXPECTED: * Shop Locator
        EXPECTED: ![](index.php?/attachments/get/115421482)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * The Grid Home
        EXPECTED: * Join Grid
        EXPECTED: * My Payout Settings
        EXPECTED: * Shop Locator
        EXPECTED: ![](index.php?/attachments/get/115421484)
        """

        if self.device_type == 'desktop':
            self.header_wrapper.inbox_header.close_button.click()
            self.site.header.right_menu_button.click()
        else:
            self.header_wrapper.inbox_header.back_button.click()
        if self.brand == 'ladbrokes':
            self._logger.warning('*** Skipping verification as this option is present only for Coral')
            return

        self.__class__.connect_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='connect')
        self.site.right_menu.click_item(item_name=self.connect_title)

        connect_items = self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='connectitems')
        connect_menu_names = [item.get('text') for item in connect_items.get('children')
                              if 'condition' not in item.keys()]
        self.__class__.connect_menu_names_with_condition = [item.get('text') for item in connect_items.get('children')
                                                            if 'condition' in item.keys()]
        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=connect_menu_names[0])

        if self.brand == 'bma':
            connect_menu_names = [text.upper() for text in connect_menu_names]
            self.__class__.connect_menu_names_with_condition = [text.upper() for text in
                                                                self.connect_menu_names_with_condition]
        self.assertTrue(set(connect_menu_names).issubset(set(sections)),
                        msg=f'Actual Menu items "{sections}" != Expected "{connect_menu_names}"')

    def test_013_verify_every_item_menu_navigation_by_clickingtapping_on_it(self):
        """
        DESCRIPTION: Verify every item menu navigation by clicking/tapping on it
        EXPECTED: **Coral**
        EXPECTED: * Shop Exclusive Promos opens Promotions page > Shop Exclusive tab
        EXPECTED: * Shop Bet Tracker opens Shop Bet Tracker page
        EXPECTED: * Football Bet Filter opens Football Bet Filter page
        EXPECTED: * Shop Locator opens Shop Locator page with map opened
        EXPECTED: **Ladbrokes**
        EXPECTED: * The Grid Home opens external link (e.g. https://thegrid.ladbrokes.com/en)
        EXPECTED: * Join Grid opens Generate Grid card page (e.g. https://sports.ladbrokes.com/en/mobileportal/virtualcard)
        EXPECTED: * My Payout Settings opens the Payout settings page (e.g. http://sports.ladbrokes.com/en/mobileportal/payoutsettings)
        EXPECTED: * Shop Locator opens Shop Locator page with map opened
        """
        if self.brand == 'ladbrokes':
            self._logger.warning('*** Skipping verification as this option is present only for Coral')
            return

        item_names = self.site.menus.items_names
        self.verify_items(item_names, self.connect_title)

    def test_014__go_back_and_open_my_account_menu_click_on_settings_item(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click on 'Settings' item
        EXPECTED: 'Settings'Overlay/pop-up is opened with the following items:
        EXPECTED: **Coral**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * My Account Details
        EXPECTED: * Change Password
        EXPECTED: * Marketing Preferences
        EXPECTED: * Betting Setting
        EXPECTED: ![](index.php?/attachments/get/115421553)
        EXPECTED: **Ladbrokes**
        EXPECTED: * Title, 'Back' and 'Close' button
        EXPECTED: * My Account Details
        EXPECTED: * Change Password
        EXPECTED: * Communication Preferences
        EXPECTED: * Betting Setting
        EXPECTED: ![](index.php?/attachments/get/115421556)
        """
        if self.brand == 'bma':
            self.site.right_menu.header.back_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        settings_title = self.site.window_client_config.get_gvc_config_item_text(key_title='name', value_title='settings')
        self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=settings_title)
        self.site.right_menu.click_item(item_name=settings_title)

        settings_items = \
            self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='settingitems')
        settings_menu_names = [item.get('text') for item in settings_items.get('children')
                               if item.get('name') != 'myaccountdetails_inshop']
        if self.brand == 'bma':
            settings_menu_names = [text.upper() for text in settings_menu_names]

        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=settings_menu_names[0])
        self.assertEqual(set(sections), set(settings_menu_names),
                         msg=f'Actual Menu items "{sections}" != Expected "{settings_menu_names}')

    def test_015_verify_every_item_menu_navigation_by_clickingtapping_on_it(self):
        """
        DESCRIPTION: Verify every item menu navigation by clicking/tapping on it
        EXPECTED: * My Account Details opens My account details overlay/pop-up
        EXPECTED: * Change Password opens Change Password overlay/pop-up
        EXPECTED: * Marketing/Communication Preferences opens  Communication Preferences
        EXPECTED: * Betting Setting opens Preferences Page
        """
        settings_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='settings')
        item_names = self.site.menus.items_names
        betting_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='bettingsettings')

        def do_navigate(menu_item_name):
            self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=menu_item_name)
            items = self.site.menus.items_as_ordered_dict
            self.assertTrue(items, msg='Cannot get "My Account" Details section items')
            menu_item = items.get(menu_item_name)
            self.assertTrue(menu_item, msg=f'"{menu_item} was not found in "{items.keys()}"')
            menu_item.click()
            sleep(5)
            self.assertTrue(wait_for_result(lambda: menu_item.get_header, timeout=15),
                            msg=f'{menu_item} header is not displayed')
            return menu_item.get_header

        def verify_item_mobile(menu_item_name):
            self._logger.info(f'*** Opening menu item "{menu_item_name}"')
            lazy_header = do_navigate(menu_item_name)

            self.site.wait_content_state_changed(timeout=10)
            if menu_item_name == betting_title:
                self.assertTrue(wait_for_result(lambda: lazy_header.header, timeout=15),
                                msg=f'header is not displayed')
                header = lazy_header.header
                header.back_button.click()
                return
            self.assertTrue(wait_for_result(lambda: lazy_header.specific_header, timeout=15),
                            msg=f'header is not displayed')
            header = lazy_header.specific_header
            self.assertTrue(header.page_title.is_displayed(), msg=f'"{menu_item_name}" page is not opened')
            header.back_button.click()

        def verify_item_desktop(menu_item_name):
            self._logger.info(f'*** Opening menu item "{menu_item_name}"')
            lazy_header = do_navigate(menu_item_name)

            change_password_title = self.site.window_client_config.get_gvc_config_item_text(
                key_title='name', value_title='changepassword')
            communication_preferences_title = self.site.window_client_config.get_gvc_config_item_text(
                key_title='name', value_title='communication')

            left_navigation_menu_items = [change_password_title, communication_preferences_title]
            if menu_item_name in left_navigation_menu_items:
                nav_menu = lazy_header.transactions_left_nav_menu
            elif menu_item_name == betting_title:
                nav_text = lazy_header.header.page_title.text
                expected_text = vec.bma.USER_SETTINGS_HEADING.upper() if self.brand == 'bma' else vec.bma.USER_SETTINGS_HEADING
                self.assertEquals(nav_text, expected_text, msg=f'Actual "{nav_text}" != Expected "{expected_text}"')
                return
            else:
                nav_menu = lazy_header.details_top_nav_menu
            link = nav_menu.active_link
            self.assertEquals(link.text.upper(), menu_item_name.upper(),
                              msg=f'Actual name "{link.text.upper()}" != Expected "{menu_item_name.upper()}"')

            self.open_right_menu()
            self.site.right_menu.click_item(item_name=settings_title)

        item_verification = verify_item_desktop if self.device_type == 'desktop' else verify_item_mobile
        for item_name in item_names:
            # TODO "extra item coming in settings menu in jenkins"
            if item_name != 'COOKIES SETTINGS':
                item_verification(item_name)

    def test_016__go_back_and_open_my_account_menu_clicktap_on_gambling_controls(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Gambling controls'
        EXPECTED: 'Gambling Controls' Overlay/Pop-up is opened
        EXPECTED: ![](index.php?/attachments/get/115421561)
        EXPECTED: ![](index.php?/attachments/get/115421562)
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open "My Account" menu')

        right_menu_gambling_controls_title = self.site.window_client_config.gambling_controls_title

        items = self.site.menus.items_as_ordered_dict
        self.assertTrue(items, msg='Cannot get My Account Menu items')
        gambling = items.get(right_menu_gambling_controls_title)
        self.assertTrue(gambling, msg=f'"{right_menu_gambling_controls_title} was not found in "{items.keys()}"')
        gambling.click()
        self.assertTrue(wait_for_result(lambda: gambling.get_header, timeout=15),
                        msg=f'gambling header is not displayed')
        self.__class__.gambling_header = gambling.get_header
        gambling_controls_title = self.site.window_client_config.mobile_portal_gambling_controls
        if self.device_type == 'desktop':
            nav_menu = self.gambling_header.transactions_left_nav_menu
            link = nav_menu.active_link
            self.assertEquals(link.text, gambling_controls_title)
        else:
            self.assertTrue(self.gambling_header.inbox_header.is_displayed(),
                            msg=f'"{gambling_controls_title}" page is not opened')

    def test_017__go_back_and_open_my_account_menu_clicktap_on_help__contact(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Help & Contact'
        EXPECTED: 'Help & Contact' Overlay/Pop-up is opened
        EXPECTED: ![](index.php?/attachments/get/115421563)
        EXPECTED: ![](index.php?/attachments/get/115421564)
        """
        if self.device_type == 'desktop':
            self.site.header.right_menu_button.click()
        else:
            self.gambling_header.inbox_header.back_button.click()
        # self.open_right_menu()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        contact_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='class', value_title='theme-help-contact')
        items = self.site.menus.items_as_ordered_dict
        self.assertTrue(items, msg='Cannot get "My Account" menu items')
        contact = items.get(contact_title)
        self.assertTrue(contact, msg=f'"{contact_title} was not found in "{items.keys()}"')
        contact.click()
        sleep(5)
        self.assertTrue(wait_for_result(lambda: contact.get_header, timeout=15),
                        msg=f'header is not displayed')
        self.__class__.contact_header = contact.get_header
        contact_title = contact_title.title()
        if self.device_type == 'desktop':
            self.assertEquals(self.contact_header.help_contact_header.text, contact_title)
        else:
            self.assertTrue(self.contact_header.inbox_header.is_displayed(),
                            msg=f'"{contact_title}" page is not opened')

    def test_018__go_back_and_open_my_account_menu_clicktap_on_log_out(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Log Out'
        EXPECTED: User is logged out
        """
        if self.device_type == 'desktop':
            self.site.header.right_menu_button.click()
        else:
            self.contact_header.inbox_header.back_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        self.site.right_menu.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')

    def test_019__go_back_and_open_my_account_menu_clicktap_on_deposit_button(self):
        """
        DESCRIPTION: * Go back and open 'My Account' menu
        DESCRIPTION: * Click/Tap on 'Deposit' button
        EXPECTED: 'Deposit' button opens deposit Overlay/pop-up
        """
        self.site.login()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        self.site.right_menu.deposit_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(wait_for_result(lambda: self.site.deposit.deposit_title, timeout=15),
                        msg=f'User is not navigated to "{vec.bma.DEPOSIT}" page')
