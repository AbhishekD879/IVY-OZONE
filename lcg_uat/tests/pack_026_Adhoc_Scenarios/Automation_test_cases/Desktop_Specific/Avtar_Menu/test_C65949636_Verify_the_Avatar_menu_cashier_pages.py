import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.avtar_menu
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@vtest
class Test_C65949636_Verify_the_Avatar_menu_cashier_pages(Common):
    """
    TR_ID: C65949636
    NAME: Verify the Avatar menu cashier pages.
    DESCRIPTION: This test case is to validate the Avatar menu cashier pages.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_launch_the__ladbrokescoral_application(self):
        """
        DESCRIPTION: launch the  Ladbrokes/Coral application.
        EXPECTED: Application should be  Launched successfully and by default user is in sports Home page.
        """
        # Covered In Step2

    def test_002_click_on_login_cta__from_header_menu_enter_valid_credentials_and_click_on_log_in(self):
        """
        DESCRIPTION: Click on login CTA  from Header Menu, enter valid credentials and click on log in.
        EXPECTED: User must be logged in sucessfully and user must be able to see the Deposit CTA, inbox and avatar menu.
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username, amount='5',
                                                                     card_number='5137651100600001',
                                                                     card_type='mastercard',
                                                                     expiry_month='12',
                                                                     expiry_year='2080',
                                                                     cvv='123'
                                                                     )
        self.site.login(username=username)

    def test_003_click_on_avatar_menu(self):
        """
        DESCRIPTION: Click on Avatar menu.
        EXPECTED: Under Avatar meny user must be able to see the
        EXPECTED: Cashier , Promotions and Account Pages.
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        right_menu_items = self.site.right_menu.section_wise_items
        self.assertTrue(right_menu_items, msg="Avatar Menu Is Not displayed even after clicking Avatar Icon")

    def test_004_verify_the_cashier_pages(self):
        """
        DESCRIPTION: Verify the Cashier pages.
        EXPECTED: Cashier page consists of Deposit, Withdraw,
        EXPECTED: Payment history and Manage My cards.
        """
        right_menu_items = self.site.right_menu.section_wise_items
        cashier_items = right_menu_items.get("CASHIER").keys()
        expected_cashier_items = ['DEPOSIT', 'WITHDRAW', 'PAYMENTHISTORY', 'MANAGEMYCARDS']
        for cashier_item in expected_cashier_items:
            self.assertIn(cashier_item, cashier_items,
                          msg=f"cashier item {cashier_item} is not present in cashier items {cashier_items}")

    def test_005_click_on_deposit(self):
        """
        DESCRIPTION: Click on Deposit
        EXPECTED: Quick Deposit pop-up should be displayed.
        EXPECTED: Enter the Required amount in the Amount filed and enter CVV.
        EXPECTED: Click on Deposit.
        EXPECTED: Deposited amount must be added to the user wallet.
        """
        initial_user_balance = float(self.site.header.user_balance)
        right_menu_items = self.site.right_menu.section_wise_items
        deposit_button = right_menu_items.get("CASHIER").get("DEPOSIT")
        self.assertTrue(deposit_button, msg=f"Deposit Button not found in {right_menu_items.get('CASHIER').keys()}")
        deposit_button.click()
        wait_for_haul(5)
        if self.device_type != "mobile":
            desktop_quick_deposit = self.site.quick_deposit_desktop.stick_to_iframe()
            desktop_quick_deposit.cvv.value = "123"
            self.assertEqual(desktop_quick_deposit.cvv.value, "123",
                             msg="Desktop Quick Deposit cvv value not changed to 123")
            deposit_amount = float(desktop_quick_deposit.amount.value)
            desktop_quick_deposit.deposit_btn.click()
            desktop_quick_deposit.switch_to_main_page()
            wait_for_haul(8)
            after_deposit_user_balance = float(self.site.header.user_balance)
            expected_amount_after_deposit = deposit_amount + initial_user_balance
            self.assertEqual(after_deposit_user_balance, expected_amount_after_deposit,
                             msg=f"Expected amount after deposit {expected_amount_after_deposit} "
                                 f"is not equal to actual amount after deposit {after_deposit_user_balance}")
        else:
            quick_deposit_menu = self.site.deposit.stick_to_iframe()
            quick_deposit_menu.cvv.value = 123
            quick_deposit_menu.deposit_btn.click()
            wait_for_haul(5)

        self.navigate_to_page('/')

    def test_006_click_on_withdraw(self):
        """
        DESCRIPTION: Click on Withdraw
        EXPECTED: User must be navigated to the withdraw page.
        EXPECTED: Click on 'X' mark next to the balance on Header page, user must be navigated back to the sports homepage.
        """
        self.site.header.right_menu_button.click()
        right_menu_items = self.site.right_menu.section_wise_items
        withdraw_button = right_menu_items.get("CASHIER").get("WITHDRAW")
        withdraw_button.click()
        self.site.cashier_withdraw.header.close_button.click()
        is_beta_environment = 'beta' in self.device.get_current_url().split("sports", 1)[0]
        if not is_beta_environment:
            self.navigate_to_page('/')

    def test_007_click_on_payment_history(self):
        """
        DESCRIPTION: Click on Payment history.
        EXPECTED: User must be navigated to the Payment history page.
        EXPECTED: In payment history page user must be able to see the last 30days total net deposits.
        EXPECTED: User must be able to apply the filters and see the results accordingly.
        EXPECTED: Click on 'X' mark next to the balance on Header page, user must be navigated back to the sports homepage.
        """
        self.site.header.right_menu_button.click()
        right_menu_items = self.site.right_menu.section_wise_items
        payment_history = right_menu_items.get("CASHIER").get("PAYMENTHISTORY")
        payment_history.click()
        wait_for_haul(8)
        payment_history_page = self.site.cashier_payment_history
        last_days = payment_history_page.content.account_info.last_days.text
        net_deposit = payment_history_page.content.account_info.items_as_ordered_dict.get(
            'Total Net Deposits').amount.text
        transaction_filter = payment_history_page.content.transaction_filters.items_as_ordered_dict
        self.assertTrue(transaction_filter, msg="Transaction filters Not displayed")
        self.assertTrue(last_days, msg="Last 30 days Label Not Displayed")
        self.assertTrue(net_deposit, msg="Net Deposits Not Displayed")
        payment_history_page.header.close_button.click()
        is_beta_environment = 'beta' in self.device.get_current_url().split("sports", 1)[0]
        if not is_beta_environment:
            self.navigate_to_page('/')
            wait_for_haul(10)
            self.site.header.right_menu_button.click()

    def test_008_click_on_manage_my_cards(self):
        """
        DESCRIPTION: Click on Manage My Cards.
        EXPECTED: User must be navigated to the Manage my cards page where all the cards that are been saved by user are visible.
        EXPECTED: Click on delete CTA, the selected card must be removed.
        EXPECTED: Click on 'X' mark next to the balance on Header page, user must be navigated back to the sports homepage.
        """
        wait_for_haul(10)
        if self.device_type != 'mobile' and tests.settings.brand == 'bma':
            self.site.header.right_menu_button.click()
        right_menu_items = self.site.right_menu.section_wise_items
        manage_card = right_menu_items.get("CASHIER").get("MANAGEMYCARDS")
        manage_card.click()
        wait_for_haul(10)
        cashier_manage_my_card = self.site.cashier_manage_my_card
        cashier_manage_my_card.content.card_section.delete_card_btn.click()
        delete_popup = wait_for_result(lambda: cashier_manage_my_card.delete_popup, timeout=20,
                                       bypass_exceptions=VoltronException)
        self.assertTrue(delete_popup, msg="Delete popup Did not appear after clicking delete button")
        cashier_manage_my_card.delete_popup.confirm_delete.click()
        cashier_manage_my_card.header.close_button.click()
        is_beta_environment = 'beta' in self.device.get_current_url().split("sports", 1)[0]
        if not is_beta_environment:
            self.navigate_to_page('/')
