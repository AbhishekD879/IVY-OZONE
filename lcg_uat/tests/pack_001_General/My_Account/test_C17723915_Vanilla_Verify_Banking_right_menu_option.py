import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from voltron.utils.exceptions.voltron_exception import VoltronException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


# @pytest.mark.desktop
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17723915_Vanilla_Verify_Banking_right_menu_option(Common):
    """
    TR_ID: C17723915
    NAME: [Vanilla] Verify 'Banking' right menu option
    DESCRIPTION: This test case is to verify all option menus under Banking right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

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

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in, 'My Account' button appears
        """
        self.site.wait_content_state("HomePage")
        self.site.login()

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap 'My Account' button
        EXPECTED: Right menu is displayed
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')

    def test_003_clicktap_banking__balances_ladbrokesbankingcoral_menu_option(self):
        """
        DESCRIPTION: Click/tap 'Banking & Balances' (Ladbrokes)/'Banking'(Coral) menu option
        EXPECTED: 'Banking & Balances'/'Banking' menu is displayed with the following options:
        EXPECTED: - My Balance
        EXPECTED: - Deposit
        EXPECTED: - Transfer (Ladbrokes only)
        EXPECTED: - Withdraw
        EXPECTED: - Payment History (Ladbrokes only)
        """
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0])
        self.site.wait_content_state_changed(timeout=15)
        self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0],
                         msg='"Banking menu" is not displayed')
        actual_banking_menu = list(self.site.right_menu.items_as_ordered_dict)
        self.assertEqual(actual_banking_menu, vec.bma.BANKING_MENU_ITEMS,
                         msg=f'Actual items: "{actual_banking_menu}" are not equal with the'
                             f'Expected items: "{vec.bma.BANKING_MENU_ITEMS}"')

    def test_004_clicktap_my_balance_option(self):
        """
        DESCRIPTION: Click/tap 'My Balance' option
        EXPECTED: 'My Balance' is displayed with the following information:
        EXPECTED: - Withdrawable - Online
        EXPECTED: - Restricted (Coral only)
        EXPECTED: - Available balance
        EXPECTED: - Total balance
        EXPECTED: At the bottom there is a 'Deposit' button and 'Available to use on' section
        """
        self.__class__.cashier_menu_title = self.site.window_client_config.cashier_menu_title
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
        status = all(item in sections for item in expected_my_balance_title)

        self.assertTrue(status, msg=f'Actual Menu items "{set(sections)}" != Expected "{set(expected_my_balance_title)}')

        self.assertTrue(self.site.right_menu.my_balance.deposit_button.is_displayed(),
                        msg='Deposit button is not present')
        self.assertTrue(self.site.right_menu.my_balance.available_to_use.is_displayed(),
                        msg='Available to use on table is not present')

    def test_005_navigate_back_and_clicktap_deposit_option(self):
        """
        DESCRIPTION: Navigate back and click/tap 'Deposit' option
        EXPECTED: User is taken to 'Deposit/payment methods' page
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

    def test_006_navigate_back_and_clicktap_withdraw_option(self):
        """
        DESCRIPTION: Navigate back and click/tap 'Withdraw' option
        EXPECTED: User is taken to 'Withdraw' page
        """
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
        self.site.wait_content_state_changed(timeout=20)
        self.assertTrue(self.site.menus.withdrawal, msg='Withdraw Overlay is not opened')

    def test_007_ladbrokes_onlynavigate_back_and_clicktap_transfer_option(self):
        """
        DESCRIPTION: **Ladbrokes only:**
        DESCRIPTION: Navigate back and click/tap 'Transfer' option
        EXPECTED: User is taken to 'Transfer' page
        """
        if self.brand == 'ladbrokes':
            self.device.go_back()
            if self.device_type == 'desktop':
                self.test_002_clicktap_my_account_button()
                self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0])
                self.assertTrue(self.site.right_menu.header.back_button, msg='"Back button" is not present')
            self.site.right_menu.click_item(vec.bma.BANKING_MENU_ITEMS[2])

    def test_008_ladbrokes_onlynavigate_back_and_clicktap_payment_history_option(self):
        """
        DESCRIPTION: **Ladbrokes only:**
        DESCRIPTION: Navigate back and click/tap 'Payment History' option
        EXPECTED: User is taken to 'Payment History' page
        """
        if self.brand == 'ladbrokes':
            self.device.go_back()
            if self.device_type == 'desktop':
                self.test_002_clicktap_my_account_button()
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[0])
            self.assertTrue(self.site.right_menu.header.back_button, msg='"Back button" is not present')
            self.site.right_menu.click_item(vec.bma.BANKING_MENU_ITEMS[4])
            self.assertTrue(self.site.payment_history.go_button, msg='"Go button" is not present')
