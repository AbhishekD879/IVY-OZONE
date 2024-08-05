from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import tests
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2  # Portal related test
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
# @pytest.mark.high
@pytest.mark.portal_only_test
@pytest.mark.user_account
@pytest.mark.login
@pytest.mark.desktop
# @pytest.mark.sanity
# @pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1636')  # ladbrokes QA2 only
@vtest
class Test_C35238874_Navigation_My_Account_options(Common):
    """
    TR_ID: C35238874
    NAME: Navigation 'My Account' options
    DESCRIPTION: Verify that "My Account" options open the correct page
    PRECONDITIONS: My Account Menu or User Menu is handled and set on GVC side.
    """
    keep_browser_open = True
    connect_menu_names_with_condition = []

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
        sleep(3)

        def verify_item(menu_item_name):
            # We have to re-initialize items every time as page is reloaded later during verifications
            self.items_loaded(lambda: self.site.menus.items_as_ordered_dict, item_to_wait=menu_item_name)
            items = self.site.menus.items_as_ordered_dict
            self.assertTrue(items, msg='Cannot get My Account Menu items')
            menu_item = items.get(menu_item_name)
            self.assertTrue(menu_item, msg=f'"{menu_item_name}" was not found in "{items.keys()}"')

            self._logger.info(f'*** Opening menu item "{menu_item_name}"')
            menu_item.click()
            header_wrapper = menu_item.get_header
            current_url = self.device.get_current_url()
            if 'promo/offers' in current_url and promo_external_link:
                self.assertEqual(
                    current_url, promo_external_link,
                    msg=f'Actual Gaming promotions external link "{current_url}" != Expected "{promo_external_link}')
                self.navigate_to_page(name='/')
            else:
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

    def test_001_load_oxygen_app_and_login(self):
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

        self.assertTrue(self.site.header.right_menu_button.is_displayed(),
                        msg='[My Account] button is not displayed on Header')

    def test_002_click_on_my_account_button_on_header(self):
        """
        DESCRIPTION: Click on [My Account] button on Header
        EXPECTED: Menu Overlay appears on full screen on Mobile and as a pop-up on Tablet/Desktop with next items ( configurable on GVC side):
        EXPECTED: * Cashier
        EXPECTED: * Offers
        EXPECTED: * History
        EXPECTED: * Inbox
        EXPECTED: * Connect
        EXPECTED: * Settings
        EXPECTED: * Gambling Controls
        EXPECTED: * Help & Contact
        EXPECTED: * Log Out
        EXPECTED: * Green'DEPOSIT' button
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        my_account_menu = self.site.window_client_config.get_gvc_config_item(key_title='type', value_title='menu')
        self.__class__.get_gvc_menu_items = {}
        for item in my_account_menu.get('children'):
            if item.get('name') != 'gamblingcontrols_inshop' and item.get('menuRoute') != 'menu/vip' and item.get('name') != 'affordabilitylosslimits':
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
        self.assertEqual(sorted(self.actual_menu_items), sorted(expected_menu_items),
                         msg=f'Actual Menu items "{sorted(self.actual_menu_items)}" != '
                             f'Expected "{sorted(expected_menu_items)}')
        self.assertTrue(self.site.right_menu.has_deposit_button(), msg='Deposit button is not displayed')

    def test_003_check_every_item_view(self):
        """
        DESCRIPTION: * Check every item view
        EXPECTED: * Every item has an icon an is left aligned
        EXPECTED: * 'Offers' have 'FB' icon if user has freebets
        EXPECTED: * 'Inbox' have counter badge if user has rich inbox messages unread
        EXPECTED: * Arrow is present from right side for items that have further pop-up/overlay navigation ( e.g. Cashier,Offers,History,Connect,Settings)
        """
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Cannot get My Account Menu items')
        for name, value in menu_items.items():
            menu_item = self.site.right_menu.items_as_ordered_dict.get(name)
            self.assertTrue(menu_item.has_icon(), msg=f'"{name}" item has not an icon')
            if tests.settings.backend_env != 'prod' and name == self.site.window_client_config.offers_menu_title:
                self.assertTrue(menu_items.get(name).has_free_bet_icon(),
                                msg=f'FB icon for "{self.site.window_client_config.offers_menu_title}" is not present')
        for item in self.get_gvc_menu_items.get('with_arrow'):
            self.assertTrue(menu_items.get(item).has_arrow_icon(), msg=f'{item} item has not an arrow icon')

    def test_004_click_on_banking_item(self):
        """
        DESCRIPTION: Click on 'Banking' item
        EXPECTED: Banking Menu is opened with
        EXPECTED: * My balance
        EXPECTED: * Deposit
        EXPECTED: * Withdraw
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

    def test_005_click_my_balance_item_and_check_overlay_pop_up_view(self):
        """
        DESCRIPTION: Click 'My balance' item and check Overlay/Pop-up view
        EXPECTED: My Balance Overlay/Pop-up is opened with next items:
        EXPECTED: * Withdrawable-online
        EXPECTED: * Restricted
        EXPECTED: * Available balance
        EXPECTED: * Total Balance
        EXPECTED: * Deposit Button
        EXPECTED: * Available to use on table
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

        self.assertTrue(status, msg=f'Actual Menu items "{set(sections)}" != Expected "{set(expected_my_balance_title)}')

        self.assertTrue(self.site.right_menu.my_balance.deposit_button.is_displayed(),
                        msg='Deposit button is not present')
        self.assertTrue(self.site.right_menu.my_balance.available_to_use.is_displayed(),
                        msg='Available to use on table is not present')

    def test_006_click_back_button_on_header_and_check_deposit_and_withdaw_item_navigation(self):
        """
        DESCRIPTION: Click back ('<') button on header and check 'Deposit' and 'Withdaw' item navigation
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
        self.assertTrue(self.site.deposit.is_displayed(), msg='"Deposit" menu is not displayed')

        self.site.deposit.close()

        self.navigate_to_page(name='/')
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')

        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        self.site.right_menu.click_item(item_name=self.cashier_menu_title)

        withdraw_text = self.site.window_client_config.get_gvc_config_item_text(key_title='name',
                                                                                value_title='withdraw')
        self.items_loaded(lambda: self.site.right_menu.items_names,
                          item_to_wait=withdraw_text)
        self.site.right_menu.click_item(item_name=withdraw_text)
        self.assertTrue(self.site.menus.withdrawal.is_displayed(), msg='Withdraw Overlay is not opened')

    def test_007_go_back_and_open_my_account_menu_click_on_offers(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Offers'
        EXPECTED: Offers Overlay is opened with next item menus:
        EXPECTED: * Sports Free Bets
        EXPECTED: * Sports Promotions
        EXPECTED: * Gaming Promotions
        EXPECTED: * Voucher Code
        """
        self.site.menus.withdrawal.header.close_button.click()
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        self.site.right_menu.click_item(item_name=self.site.window_client_config.offers_menu_title)

        offers_items = self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='offeritems')
        offer_menu_names = [item.get('text').upper() if self.brand == 'bma' else item.get('text')
                            for item in offers_items.get('children')]
        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=offer_menu_names[0])
        self.assertEqual(set(sections), set(offer_menu_names),
                         msg=f'Actual Menu items "{sections}" != Expected "{offer_menu_names}')

    def test_008_check_every_item_menu_navigation(self):
        """
        DESCRIPTION: Check every item menu navigation
        EXPECTED: * Sports Free Bets opens Freebets page
        EXPECTED: * Sports Promotions opens Promotions page
        EXPECTED: * Gaming Promotions opens Gaming promotions ( external https://beta-promo.coral.co.uk/en/promo/offers)
        EXPECTED: * Voucher Code opens Voucher page ( https://beta-sports.coral.co.uk/voucher-code)
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

    def test_009_go_back_and_open_my_account_menu_click_on_history(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'History'
        EXPECTED: History Overlay/pop-up is opened with next items:
        EXPECTED: * Betting History
        EXPECTED: * Transaction History
        EXPECTED: * Payment History
        """
        sleep(3)
        self.site.right_menu.header.back_button.click()
        self.assertTrue(self.site.is_right_menu_opened(timeout=5), msg='Failed to open My Account Menu')
        history_config = self.site.window_client_config.get_gvc_config_item(
            key_title='name', value_title='history')
        self.__class__.history_title = history_config.get('text').upper()
        self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=self.history_title)
        self.site.right_menu.click_item(item_name=self.history_title)
        history_items = self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='historyitems')
        history_menu_names = [item.get('text').upper() if self.brand == 'bma' else item.get('text') for item in history_items.get('children')]
        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=history_menu_names[0])
        self.assertEqual(set(sections), set(history_menu_names),
                         msg=f'Actual Menu items "{sections}" != Expected "{history_menu_names}')

    def test_010_check_every_item_menu_navigation(self):
        """
        DESCRIPTION: Check every item menu navigation
        EXPECTED: * Betting History opens Settled Bets page/tab
        EXPECTED: * Transaction History opens Gaming history ( e.g. https://beta-sports.coral.co.uk/en/mobileportal/transactions)
        EXPECTED: * Payment History opens Payment history page ( e.g. https://cashier.coral.co.uk/home/txnSearchPageMerchant.action?sessionKey=198d8026e07f487fb348c516cc3d355a&LANG_ID=en&parent=https://beta-sports.coral.co.uk/)
        """
        self.__class__.history_title = self.site.window_client_config.get_gvc_config_item_text(key_title='name', value_title='history')
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
            header_wrapper = menu_item.get_header
            return header_wrapper

        header_wrapper = get_header_wrapper(betting_text)
        header = header_wrapper.header
        self.assertTrue(header.page_title.is_displayed(), msg=f'"{betting_text}" page is not opened')
        header.back_button.click()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
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

    def test_011_go_back_and_open_my_account_menu_click_on_inbox(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Inbox'
        EXPECTED: My Inbox overlay/pop-up is opened with rich inbox messages available.
        """
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open "My Account" menu')

        inbox_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='myinbox')
        items = self.site.menus.items_as_ordered_dict
        self.assertTrue(items, msg='Cannot get "My Account" menu items')
        inbox = items.get(inbox_title)
        self.assertTrue(inbox, msg=f'"{inbox} was not found in "{items.keys()}"')
        inbox.click()
        self.__class__.header_wrapper = inbox.get_header
        self.assertTrue(self.header_wrapper.inbox_header.is_displayed(), msg=f'"{inbox_title}" page is not opened')

    def test_012_go_back_and_open_my_account_menu_click_on_connect(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Connect'
        EXPECTED: 'Connect' Overlay/pop-up is opened with next items:
        EXPECTED: * Shop Exclusive Promos
        EXPECTED: * Shop Bet Tracker
        EXPECTED: * Football Bet Filter
        EXPECTED: * Shop Locator
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
            self.__class__.connect_menu_names_with_condition = [text.upper() for text in self.connect_menu_names_with_condition]
        self.assertTrue(set(connect_menu_names).issubset(set(sections)),
                        msg=f'Actual Menu items "{sections}" != Expected "{connect_menu_names}"')

    def test_013_check_every_item_menu_navigation(self):
        """
        DESCRIPTION: Check every item menu navigation
        EXPECTED: * Shop Exclusive Promos opens Promotions page > Shop Exclusive tab
        EXPECTED: * Shop Bet Tracker opens Shop Bet Tracker page
        EXPECTED: * Football Bet Filter opens Football Bet Filter page
        EXPECTED: * Shop Locator opens Shop Locator page with map opened
        """
        if self.brand == 'ladbrokes':
            self._logger.warning('*** Skipping verification as this option is present only for Coral')
            return

        item_names = self.site.menus.items_names
        self.verify_items(item_names, self.connect_title)

    def test_014_go_back_and_open_my_account_menu_click_on_settings(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Settings'
        EXPECTED: 'Settings'Overlay/pop-up is opened with next items:
        EXPECTED: * My Account Details
        EXPECTED: * Change Password
        EXPECTED: * Marketing Preferences
        EXPECTED: * Betting Setting
        """
        if self.brand == 'bma':
            self.site.right_menu.header.back_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        self.__class__.settings_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='settings')
        self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=self.settings_title)
        self.site.right_menu.click_item(item_name=self.settings_title)

        settings_items = \
            self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='settingitems')
        settings_menu_names = [item.get('text') for item in settings_items.get('children')
                               if item.get('name') != 'myaccountdetails_inshop']
        if self.brand == 'bma':
            settings_menu_names = [text.upper() for text in settings_menu_names]

        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=settings_menu_names[0])
        self.assertEqual(set(sections), set(settings_menu_names),
                         msg=f'Actual Menu items "{sections}" != Expected "{settings_menu_names}')

    def test_015_check_every_item_menu_navigation(self):
        """
        DESCRIPTION: Check every item menu navigation
        EXPECTED: * My Account Details opens My account details overlay/pop-up
        EXPECTED: * Change Password opens Change Password overlay/pop-up
        EXPECTED: * Marketing Preferences opens  Communication Preferences
        EXPECTED: * Betting Setting opens Preferences Page
        """
        settings_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='settings')
        item_names = self.site.menus.items_names
        self._logger.info(f'*** item names "{item_names}"')
        betting_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='bettingsettings')

        def do_navigate(menu_item_name):
            self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=menu_item_name)
            sleep(10)
            items = self.site.menus.items_as_ordered_dict
            self.assertTrue(items, msg='Cannot get "My Account" Details section items')
            menu_item = items.get(menu_item_name)
            self.assertTrue(menu_item, msg=f'"{menu_item} was not found in "{items.keys()}"')
            menu_item.click()
            return menu_item.get_header

        def verify_item_mobile(menu_item_name):
            self._logger.info(f'*** Opening menu item "{menu_item_name}"')
            lazy_header = do_navigate(menu_item_name)
            if menu_item_name == betting_title:
                header = lazy_header.header
                header.back_button.click()
                self.site.header.right_menu_button.click()
                self.assertTrue(self.site.is_right_menu_opened(), msg='right menu not opened')
                self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=self.settings_title)
                self.site.right_menu.click_item(item_name=self.settings_title)
                return
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
            security_title = self.site.window_client_config.get_gvc_config_item_text(key_title='name', value_title='security')

            left_navigation_menu_items = [change_password_title, communication_preferences_title, security_title]
            if menu_item_name in left_navigation_menu_items:
                nav_menu = lazy_header.transactions_left_nav_menu
            elif menu_item_name == betting_title:
                nav_text = lazy_header.header.page_title.text
                expected_text = vec.bma.USER_SETTINGS_HEADING.upper() if self.brand == 'bma' else vec.bma.USER_SETTINGS_HEADING
                self.assertEquals(nav_text, expected_text, msg=f'Actual "{nav_text}" != Expected "{expected_text}"')
                self.navigate_to_page(name='/')
                self.site.header.right_menu_button.click()
                self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
                self.site.right_menu.click_item(item_name=settings_title)
                return
            else:
                nav_menu = lazy_header.details_top_nav_menu
            link = nav_menu.active_link
            self.assertEquals(link.text.upper(), menu_item_name.upper(),
                              msg=f'Actual name "{link.text.upper()}" != Expected "{menu_item_name.upper()}"')

            self.navigate_to_page(name='/')
            self.site.header.right_menu_button.click()
            self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
            self.site.right_menu.click_item(item_name=settings_title)

        item_verification = verify_item_desktop if self.device_type == 'desktop' else verify_item_mobile
        for item_name in item_names:
            # TODO "extra item coming in settings menu in jenkins"
            if item_name not in ['COOKIES SETTINGS', 'Cookies Settings']:
                item_verification(item_name)

    def test_016_go_back_and_open_my_account_menu_click_on_gambling_controls(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Gambling controls'
        EXPECTED: Gambling Controls Overlay/Pop-up is opened
        """
        self.navigate_to_page(name='/')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open "My Account" menu')

        right_menu_gambling_controls_title = self.site.window_client_config.gambling_controls_title

        items = self.site.menus.items_as_ordered_dict
        self.assertTrue(items, msg='Cannot get My Account Menu items')
        gambling = items.get(right_menu_gambling_controls_title)
        self.assertTrue(gambling, msg=f'"{right_menu_gambling_controls_title} was not found in "{items.keys()}"')
        gambling.click()
        self.__class__.gambling_header = gambling.get_header
        gambling_controls_title = self.site.window_client_config.mobile_portal_gambling_controls
        if self.device_type == 'desktop':
            nav_menu = self.gambling_header.transactions_left_nav_menu
            link = nav_menu.active_link
            self.assertEquals(link.text, gambling_controls_title)
        else:
            self.assertTrue(self.gambling_header.inbox_header.is_displayed(),
                            msg=f'"{gambling_controls_title}" page is not opened')

    def test_017_go_back_and_open_my_account_menu_click_on_help_contact(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Help & Contact'
        EXPECTED: 'Help & Contact' Overlay/Pop-up is opened
        """
        if self.device_type == 'desktop':
            self.site.header.right_menu_button.click()
        else:
            self.gambling_header.inbox_header.back_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        contact_title = self.site.window_client_config.get_gvc_config_item_text(
            key_title='class', value_title='theme-help-contact')
        items = self.site.menus.items_as_ordered_dict
        self.assertTrue(items, msg='Cannot get "My Account" menu items')
        contact = items.get(contact_title)
        self.assertTrue(contact, msg=f'"{contact_title} was not found in "{items.keys()}"')
        contact.click()
        self.__class__.contact_header = contact.get_header
        contact_title = contact_title.title()
        if self.device_type == 'desktop':
            self.assertEquals(self.contact_header.help_contact_header.text, contact_title)
        else:
            self.assertTrue(self.contact_header.inbox_header.is_displayed(),
                            msg=f'"{contact_title}" page is not opened')

    def test_018_go_back_and_open_my_account_menu_click_on_log_out(self):
        """
        DESCRIPTION: * Go back and open My account Menu
        DESCRIPTION: * Click on 'Log Out'
        EXPECTED: User is logged out
        """
        if self.device_type == 'desktop':
            self.site.header.right_menu_button.click()
        else:
            self.contact_header.inbox_header.back_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        self.site.right_menu.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
