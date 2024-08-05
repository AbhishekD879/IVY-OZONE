import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


# @pytest.mark.prod
# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.uat
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C44870341_Verify_the_navigation_for_the_sections_items_in_the_Banking_menu_in_My_Account(Common):
    """
    TR_ID: C44870341
    NAME: Verify the navigation for the sections/items in the Banking menu in My Account.
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_000_pre_condition(self):
        """
        DESCRIPTION: User is logged in
        """
        self.site.login()

    def test_001_clicktap_my_account_button_avatar__balance(self):
        """
        DESCRIPTION: Click/tap My Account button (Avatar)-> Balance
        EXPECTED: Banking menu with My Balance, Deposit and Withdraw is displayed
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='Failed to open Right Menu')
        self.__class__.cashier_menu_title = self.site.window_client_config.cashier_menu_title
        self.__class__.right_menu = self.site.right_menu
        self.right_menu.click_item(item_name=self.cashier_menu_title)
        banking_menu_title = self.right_menu.header.title
        self.assertEqual(banking_menu_title, self.cashier_menu_title,
                         msg=f'Actual text: "{banking_menu_title}" is not same as'
                             f' Expected text: "{self.cashier_menu_title}"')
        banking_menu_items = list(self.right_menu.get_items().keys())
        self.assertEqual(banking_menu_items, vec.bma.BANKING_MENU_ITEMS,
                         msg=f'Actual items: "{banking_menu_items}"is not same as '
                             f'Expected items: "{vec.bma.BANKING_MENU_ITEMS}"')
        self.site.wait_content_state_changed()

    def test_002_verify_my_balance_pageclick_on_my_balance(self):
        """
        DESCRIPTION: Verify My Balance Page
        DESCRIPTION: Click on My Balance
        EXPECTED: My Balance page is opened with list
        EXPECTED: Withdrawable - Online
        EXPECTED: Restricted
        EXPECTED: Available Balance
        EXPECTED: Total Balance
        """
        self.right_menu.click_item(item_name=vec.bma.BANKING_MENU_ITEMS[0])
        self.assertTrue(wait_for_result(lambda: self.right_menu.header.title, timeout=15),
                        msg=f'"{vec.bma.RIGHT_MENU_MY_BALANCE}" right menu items not visible')
        self.site.wait_content_state_changed()
        my_balance_title = self.right_menu.header.title
        self.assertEqual(my_balance_title.upper(), vec.bma.RIGHT_MENU_MY_BALANCE,
                         msg=f'Actual text: "{my_balance_title}"'
                             f'is not same as Expected text: "{vec.bma.RIGHT_MENU_MY_BALANCE}"')
        my_balance_section = list(self.right_menu.my_balance.items_as_ordered_dict)
        expected_my_balance = [item for item in my_balance_section]
        self.assertTrue(set(expected_my_balance).issubset(vec.bma.MY_BALANCE_MENU_ITEMS),
                        msg=f'Actual items: "{expected_my_balance}" are not equal with the'
                            f'Expected items: "{vec.bma.MY_BALANCE_MENU_ITEMS}"')

    def test_003_click_back_button_on_my_balance_page(self):
        """
        DESCRIPTION: Click Back button on My Balance page
        EXPECTED: User is navigated to previous page
        """
        self.right_menu.header.back_button.click()
        self.site.wait_content_state_changed()
        if self.device_type == 'mobile':
            actual_title = self.right_menu.header.title
            self.assertEqual(actual_title, self.cashier_menu_title,
                             msg=f'Actual title: "{actual_title}" is not same as'
                                 f' Expected title: "{self.cashier_menu_title}"')
        else:
            self.assertTrue(self.right_menu.is_displayed(), msg='Banking menu is not displayed')

    def test_004_verify_deposit_on_banking_pageclick_on_deposit(self):
        """
        DESCRIPTION: Verify Deposit on Banking page
        DESCRIPTION: Click on Deposit
        EXPECTED: Deposit Page is opened
        EXPECTED: Header with "Deposit" is displayed
        """
        if self.device_type == 'desktop':
            self.right_menu.click_item(item_name=self.cashier_menu_title)
        self.site.wait_content_state_changed()
        self.right_menu.click_item(item_name=self.site.window_client_config.deposit_menu_title)
        self.assertTrue(wait_for_result(lambda: self.site.deposit.deposit_title, timeout=15),
                        msg=f'User is not navigated to "{vec.bma.DEPOSIT}" page')
        actual_title = self.site.deposit.deposit_title.text.split('\n')[0]
        self.assertEqual(actual_title, vec.bma.DEPOSIT,
                         msg=f'Actual title: "{actual_title}" is not same as'
                             f'Expected title: "{vec.bma.DEPOSIT}"')

    def test_005_click_cancel_button_on_deposit_page(self):
        """
        DESCRIPTION: Click Cancel button on Deposit Page
        EXPECTED: User is navigate to HomePage
        """
        self.site.deposit.close_button.click()
        self.site.wait_for_deposit_pop_up_closed()
        self.site.wait_content_state('HomePage')

    def test_006_verify_withdrawrepeat_step_1click_on_withdraw(self):
        """
        DESCRIPTION: Verify Withdraw
        DESCRIPTION: Repeat step 1
        DESCRIPTION: Click on Withdraw
        EXPECTED: Withdraw page is opened
        EXPECTED: Header with "Withdrawal" is displayed
        """
        self.site.wait_content_state_changed()
        self.test_001_clicktap_my_account_button_avatar__balance()
        if self.brand == 'bma':
            self.right_menu.click_item(item_name=vec.bma.BANKING_MENU_ITEMS[2])
        else:
            self.right_menu.click_item(item_name=vec.bma.BANKING_MENU_ITEMS[3])
        actual_title = self.site.withdrawal.withdrawal_title.text
        self.assertEqual(actual_title, vec.gvc.WITHDRAWAL, msg=f'Actual title: "{actual_title}" is not same as'
                                                               f'Expected title: "{vec.bet_history.WITHDRAWALS}"')

    def test_007_click_cancel_button_on_withdraw(self):
        """
        DESCRIPTION: Click Cancel button on Withdraw
        EXPECTED: User is navigated back to HomePage
        """
        self.site.withdrawal.close_button.click()
        self.site.wait_content_state('HomePage')
