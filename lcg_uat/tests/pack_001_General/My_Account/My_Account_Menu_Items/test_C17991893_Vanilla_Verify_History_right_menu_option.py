import pytest
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


@pytest.mark.desktop
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.login
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C17991893_Vanilla_Verify_History_right_menu_option(Common):
    """
    TR_ID: C17991893
    NAME: [Vanilla] Verify History right menu option
    DESCRIPTION: This test case is to verify all option menus under History right menu option
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

    def get_header_wrapper(self, config_text):
        self.items_loaded(lambda: self.site.menus.items_names, item_to_wait=config_text)
        items = self.site.menus.items_as_ordered_dict
        self.assertTrue(items, msg='Cannot get History Overlay items')
        menu_item = items.get(config_text)
        self.assertTrue(menu_item, msg=f'"{config_text} was not found in "{items.keys()}"')
        menu_item.click()
        header_wrapper = menu_item.get_header
        return header_wrapper

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in, My Account button appears
        """
        self.site.wait_content_state("HomePage")
        self.site.login()

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')

    def test_003_clicktap_history_menu_option(self):
        """
        DESCRIPTION: Click/tap HISTORY menu option
        EXPECTED: History menu is displayed with the following options:
        EXPECTED: - Transaction History
        EXPECTED: - Payment History
        EXPECTED: - Betting History
        """
        history_config = self.site.window_client_config.get_gvc_config_item(
            key_title='name', value_title='history')
        history_title = history_config.get('text').upper()
        self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=history_title)
        self.site.right_menu.click_item(item_name=history_title)
        history_items = self.site.window_client_config.get_gvc_config_item(key_title='name', value_title='historyitems')
        history_menu_names = [item.get('text').upper() if self.brand == 'bma' else item.get('text') for item in history_items.get('children')]
        sections = self.items_loaded(lambda: self.site.right_menu.items_names, item_to_wait=history_menu_names[0])
        self.assertEqual(set(sections), set(history_menu_names),
                         msg=f'Actual Menu items "{sections}" != Expected "{history_menu_names}')

    def test_004_clicktap_transaction_history_option(self):
        """
        DESCRIPTION: Click/tap Transaction History option
        EXPECTED: My Transactions page is displayed
        """
        history_title = self.site.window_client_config.get_gvc_config_item_text(key_title='name', value_title='history')
        betting_text = self.site.window_client_config.get_gvc_config_item_text(key_title='name', value_title='betting')
        transaction_text = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='transaction')
        payment_text = self.site.window_client_config.get_gvc_config_item_text(
            key_title='name', value_title='payment')

        header_wrapper = self.get_header_wrapper(betting_text)
        header = header_wrapper.header
        self.assertTrue(header.page_title.is_displayed(), msg=f'"{betting_text}" page is not opened')
        header.back_button.click()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open My Account Menu')
        self.site.right_menu.click_item(item_name=history_title)

        header_wrapper = self.get_header_wrapper(transaction_text)
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

            header_wrapper = self.get_header_wrapper(payment_text)
            self.assertTrue(header_wrapper.payment_history_header.is_displayed(),
                            msg=f'"{payment_text}" page is not opened')
            header_wrapper.payment_history_header.close_button.click()

    def test_005_reopen_right_menu__history_and_clicktap_payment_history_option(self):
        """
        DESCRIPTION: Reopen right menu-> History and click/tap Payment History option
        EXPECTED: User is taken to Payment History page
        """
        # Covered into step 4

    def test_006_reopen_right_menu__history_and_clicktap_betting_history_option(self):
        """
        DESCRIPTION: Reopen right menu-> History and click/tap Betting History option
        EXPECTED: User is taken to My Bets -> Settled bets tab.
        EXPECTED: Sports section is selected by default
        """
        # Covered into step 4
