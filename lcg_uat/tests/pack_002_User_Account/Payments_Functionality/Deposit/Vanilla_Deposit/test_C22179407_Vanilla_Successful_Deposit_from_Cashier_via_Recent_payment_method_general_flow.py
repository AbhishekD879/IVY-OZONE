import datetime

import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.deposit
@pytest.mark.desktop
@pytest.mark.user_account
@pytest.mark.login
@vtest
class Test_C22179407_Vanilla__Successful_Deposit_from_Cashier_via_Recent_payment_method_general_flow(BaseUserAccountTest):
    """
    TR_ID: C22179407
    NAME: [Vanilla] - Successful Deposit from Cashier via Recent payment method  (general flow)
    DESCRIPTION: This test case verifies Deposit of Funds from Cashier via Recent payment method
    PRECONDITIONS: 1. User should register at least 1 payment method (e.g Mastercard);
    PRECONDITIONS: 2. User logged into the application;
    PRECONDITIONS: 3. User performed Deposit for registered payment Method;
    """
    keep_browser_open = True
    deposit_amount = 10.49

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. User should register at least 1 payment method (e.g Mastercard);
        DESCRIPTION: 2. User logged into the application;
        DESCRIPTION: 3. User performed Deposit for registered payment Method;
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[:-2]}'

        username = self.gvc_wallet_user_client.register_new_user().username
        self.__class__.card_type, user_card = ('mastercard', tests.settings.master_card) \
            if tests.settings.backend_env == 'prod' else ('visa', tests.settings.visa_card)
        self.add_card_and_deposit(username=username, amount=str(self.deposit_amount), card_number=user_card)
        self.site.login(username=username)

        self.__class__.initial_user_balance = self.site.header.user_balance

    def test_001_click_on_user_avatar_icon_on_the_header(self):
        """
        DESCRIPTION: Click on User "Avatar" icon on the header.
        EXPECTED: User menu is opened;
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(),
                        msg='User menu is not opened')

    def test_002_click_on_cashier_section_in_user_menu(self):
        """
        DESCRIPTION: Click on "Cashier" section in User menu;
        EXPECTED: Cashier Menu is opened and "Deposit" section is present there;
        """
        cashier_title = self.site.window_client_config.cashier_menu_title
        self.site.right_menu.click_item(item_name=cashier_title)
        result = wait_for_result(lambda: self.site.right_menu.header.title == cashier_title,
                                 name='Wait for header title to change',
                                 timeout=3)
        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                        f'expected "{cashier_title}"')
        sections = self.site.right_menu.items_names
        deposit = self.site.window_client_config.deposit_menu_title
        self.assertIn(deposit, sections,
                      msg=f'"{deposit}" is not found in "{sections}"')

    def test_003_click_on_deposit_section(self):
        """
        DESCRIPTION: Click On "Deposit" section
        EXPECTED: "Deposit" menu is opened;
        """
        self.site.right_menu.click_item(item_name=self.site.window_client_config.deposit_menu_title)
        self.assertTrue(self.site.deposit.is_displayed(scroll_to=False),
                        msg='"Deposit" menu is not displayed')

    def test_004_1_enter_amount_for_deposit2_select_card3_enter_security_codeid4_click_on_the_deposit_button(self):
        """
        DESCRIPTION: 1. Enter Amount for Deposit;
        DESCRIPTION: 2. Select Card
        DESCRIPTION: 3. Enter Security code/id
        DESCRIPTION: 4. Click on the 'Deposit' button;
        EXPECTED: Deposit is Successful
        """
        self.site.deposit.add_new_card_and_deposit(amount=self.deposit_amount,
                                                   cvv_2=tests.settings.visa_card_cvv)

    def test_005_verify_that_balance_is_changed(self):
        """
        DESCRIPTION: Verify that balance is changed;
        EXPECTED: Balance changed and increased equal to the amount of Deposit;
        """
        self.site.wait_for_deposit_pop_up_closed(timeout=10)

        if self.card_type == 'visa' and self.device_type == 'mobile':
            self.site.right_menu.close_icon.click()
        self.site.wait_content_state('HomePage', timeout=20)

        actual = str(self.site.header.user_balance)
        expected = "{0:.2f}".format(self.deposit_amount + float(self.initial_user_balance))
        self.assertEqual(actual, expected,
                         msg=f'Actual user balance "{actual}" != Expected "{expected}"')
