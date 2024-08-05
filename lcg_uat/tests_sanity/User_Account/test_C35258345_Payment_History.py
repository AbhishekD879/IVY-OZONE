import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.waiters import wait_for_result
from time import sleep
from datetime import datetime


# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.critical
@pytest.mark.user_account
@pytest.mark.desktop
# @pytest.mark.sanity
@vtest
class Test_C35258345_Payment_History(BaseUserAccountTest):
    """
    TR_ID: C35258345
    NAME: Payment History
    DESCRIPTION: This test case verifies Payment History page.
    PRECONDITIONS: 1 User is logged in to view their Payment History
    PRECONDITIONS: 2 User has Approved and Declined Deposit transactions for the past three months
    PRECONDITIONS: 3 User has Approved/Pending/Declined Withdraw transactions for the past three months (optional)
    PRECONDITIONS: 4 User has navigated to the  'My Account' menu
    """
    keep_browser_open = True
    deposit_amount = 5.00
    now = datetime.now()
    shifted_year = str(now.year + 5)
    card_date = f'{now.month:02d}/{shifted_year[-2:]}'

    def deposit_through_ui(self):
        self.site.header.right_menu_button.click()
        if self.brand == 'bma':
            self.site.right_menu.click_item(item_name='Banking')
        else:
            self.site.right_menu.click_item(item_name='Banking & Balances')
        self.site.right_menu.click_item(item_name='Deposit')
        sleep(3)
        deposit = self.site.deposit
        deposit.amount.input.value = self.deposit_amount
        deposit.cvv_2.input.value = tests.settings.master_card_cvv
        deposit.deposit_button.click(scroll_to=False)
        sleep(3)
        self.site.deposit_transaction_details.ok_button.click()
        self.site.wait_content_state("Homepage")

    def navigate_payment_history_page(self):
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.EXPECTED_RIGHT_MENU.history)
        self.site.wait_content_state_changed(timeout=5)
        self.site.right_menu.click_item(vec.bma.EXPECTED_HISTORY_MENU.payment_history)
        self.site.wait_content_state_changed()

    def test_001_select_banking__balances__payment_historycoral_history__payment_history(self):
        """
        DESCRIPTION: Select 'Banking & Balances' > 'Payment History'
        DESCRIPTION: (Coral: History > Payment History)
        EXPECTED: * 'Payment History' page is opened
        EXPECTED: ![](index.php?/attachments/get/111269030)
        """
        self.__class__.username = tests.settings.payment_history_user
        self.site.login(username=self.username)
        self.site.wait_content_state('Homepage')
        if tests.settings.brand == 'ladbrokes':
            self.deposit_through_ui()
        else:
            self.add_card_and_deposit(username=self.username, amount='5', card_number=tests.settings.master_card)
        self.navigate_payment_history_page()

    def test_002_specify_dates_click_goverify_transaction_history_table_under_the_filter(self):
        """
        DESCRIPTION: Specify dates, Click 'GO',
        DESCRIPTION: Verify transaction history table under the filter
        EXPECTED: Table consists of:
        EXPECTED: 'Date' column
        EXPECTED: 'Transaction type' column
        EXPECTED: 'Transaction amount' column
        EXPECTED: transaction block is expandable
        """
        expected_details = ['Date created:', 'Method:', 'Transaction currency:', 'Billing descriptor:', 'Status:']
        self.site.payment_history.history_date.from_date = -5
        self.site.payment_history.history_date.to_date = 0
        self.site.payment_history.go_button.click()
        wait_for_result(lambda: self.site.payment_history.history_table, timeout=10)
        items = list(self.site.payment_history.history_table.items_as_ordered_dict.values())
        self.assertTrue(items, msg='"No Transactions observed" from last few days/months')
        val = 0
        for item in items:
            self.assertTrue(item.amount.is_displayed(),
                            msg='"Transaction Amount" is not shown')
            self.assertTrue(item.transaction_type.is_displayed(),
                            msg='"Transaction type" is not shown')
            self.assertTrue(item.name.text,
                            msg='"Payment ID" is not shown')
            item.click()
            sleep(2)
            item_after_click = list(self.site.payment_history.history_table.items_as_ordered_dict.values())[val]
            self.assertTrue(item_after_click, msg='"Transaction block" is not expandable')
            actual_details = ','.join(item_after_click.collapse_body.text.split('\n'))
            for detail in expected_details:
                self.assertIn(detail, actual_details, msg=f'Expected detail "{detail}" is not available'
                                                          f'in actual detail "{actual_details}" for payment id "{item.name.text}"')
            val += 1

    def test_003_try_different_values_in_the_filter_and_check_the_table(self):
        """
        DESCRIPTION: Try different values in the filter and check the table
        EXPECTED: Table is shown according to the filter settings
        """
        self.site.payment_history.click_transaction_option(value='Deposit')
        avaiable_payment_methods = self.site.payment_history.all_payment_history.payment_option_list
        self.site.payment_history.all_payment_history.click_option(value=avaiable_payment_methods[1])
        self.site.payment_history.history_date.from_date = -28
        self.site.payment_history.history_date.to_date = 0
        self.site.payment_history.go_button.click()
        wait_for_result(lambda: self.site.payment_history.history_table, timeout=10)
        items = list(self.site.payment_history.history_table.items_as_ordered_dict.values())
        self.assertTrue(items, msg='"No Transactions observed" from last few days/months')
        for item in items:
            self.assertTrue(item.amount.is_displayed(),
                            msg='"Transaction Amount" is not shown')
            self.assertTrue(item.transaction_type.is_displayed(),
                            msg='"Transaction type" is not shown')
            self.assertTrue(item.payment_type.is_displayed(),
                            msg='"Payment type" is not shown')
            self.assertTrue(item.name.text,
                            msg='"Payment ID" is not shown')

    def test_004_expand_a_few_transactions_to_verify_details(self):
        """
        DESCRIPTION: Expand a few transactions to verify details
        EXPECTED: Expanded area contains following information:
        EXPECTED: Time
        EXPECTED: Product
        EXPECTED: Balance
        EXPECTED: Transaction ID
        EXPECTED: Explained type of transaction (not for all transactions, if possible check for:
        EXPECTED: - withdrawal,
        EXPECTED: - redeem promotions)
        """
        # covered in step 2

    def test_005_verify_net_deposits_value_correctness(self):
        """
        DESCRIPTION: Verify 'Net Deposits' value correctness
        EXPECTED: Net deposits value equals to total of all deposits minus the sum of all withdrawals for the whole time
        """
        net_deposit_gbp = self.site.payment_history.net_deposit.deposit_text.text.split(':')[1]
        self.__class__.net_deposit = float(net_deposit_gbp.split(' ')[1])
        total_withdraw = float(0.00)  # As withdrawal is not allowed for test users
        net_deposit_value = self.net_deposit - total_withdraw
        self.assertEqual(self.net_deposit, net_deposit_value,
                         msg='Net deposits value is not equals to total of all deposits minus the sum of all withdrawals')

    def test_006_make_a_deposit_and_verify_the_values_in_the_table_change(self):
        """
        DESCRIPTION: Make a deposit and verify the values in the table change
        EXPECTED: The values change accordingly
        """
        self.navigate_to_page('/')
        if tests.settings.brand == 'ladbrokes':
            self.deposit_through_ui()
        else:
            self.add_card_and_deposit(username=self.username, amount='5', card_number=tests.settings.master_card)
        self.navigate_payment_history_page()
        self.site.payment_history.history_date.from_date = -28
        self.site.payment_history.history_date.to_date = 0
        self.site.payment_history.go_button.click()
        net_deposit_gbp = self.site.payment_history.net_deposit.deposit_text.text.split(':')[1]
        net_deposit_added = float(net_deposit_gbp.split(' ')[1])
        self.assertGreater(net_deposit_added, self.net_deposit, msg='Newly Deposit is not credited')

    def test_007_tap_on_the__icon_near_net_deposits(self):
        """
        DESCRIPTION: Tap on the '?' icon near Net Deposits
        EXPECTED: pop-up is shown:
        EXPECTED: "Net deposits are calculated by taking the sum of approved deposits (including any deposit corrections) and deducting approved withdrawals (including any withdrawal corrections)."
        EXPECTED: ![](index.php?/attachments/get/111269031)
        """
        self.site.payment_history.net_deposit.deposit_tool_tip.click()
        popup_text = self.site.payment_history.deposit_info.deposit_text.text
        self.assertEqual(popup_text, vec.bma.NET_DEPOSIT_POP_UP_MSG, msg="pop is appearing as blank")
        self.site.payment_history.deposit_info.info_ok_button.click()
