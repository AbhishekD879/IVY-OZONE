import pytest
import tests
import datetime
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from faker import Faker
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.deposit
@pytest.mark.desktop
@pytest.mark.registration
@pytest.mark.uat
@vtest
class Test_C44870130_Verify_new_user_can_add_a_card_details_and_deposit_money(Common):
    """
    TR_ID: C44870130
    NAME: Verify new user can add a card details and deposit money.
    NOTE: Please ignore if 'Cardholder name' option is not available. As we will be mostly using Test cards (Cardholder name) can be ignored.
    """
    keep_browser_open = True
    deposit_amount = 20.00
    user_name = f'{tests.settings.registration_pattern_prefix}{Faker().pyint(max_value=999)}{Faker().pystr(max_chars=5)}'[:15]

    def test_000_preconditions(self):
        """
        DESCRIPTION: User is registered
        EXPECTED: User has registered successfully
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[-2:]}'
        self.gvc_wallet_user_client.register_new_user(username=self.user_name)
        self.site.login(username=self.user_name)
        self.assertTrue(self.site.wait_content_state("Homepage"))

    def test_001_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: Deposit page is opened
        """
        self.site.header.right_menu_button.click()
        # if self.brand == 'bma':
        #     self.site.right_menu.click_item(item_name='Banking')
        # else:
        #     self.site.right_menu.click_item(item_name='Banking & Balances')
        self.site.right_menu.click_item(item_name='Deposit')
        self.__class__.select_deposit_method = self.site.select_deposit_method
        self.assertTrue(wait_for_result(lambda: self.select_deposit_method.deposit_title.is_displayed(), timeout=5),
                        msg='"Deposit page" is not displayed')

    def test_002_tap_on_the_card_types_available(self):
        """
        DESCRIPTION: Tap on the Card types available
        EXPECTED: Select payment option page is displayed with following fields:
        EXPECTED: Enter amount(+ / -) with quick deposit of £20 "50 £100
        EXPECTED: Card Number
        EXPECTED: Cardholder Name
        EXPECTED: Expiration Date
        EXPECTED: CVV2
        """
        self.select_deposit_method.master_card_button.click()
        self.__class__.deposit = self.site.deposit
#        self.assertTrue(self.deposit.amount.is_displayed(), msg='Enter Amount field is not displayed')
        self.assertTrue(self.deposit.card_number.is_displayed(), msg='Card number field is not displayed')
        self.assertTrue(self.deposit.card_holder.is_displayed(), msg='Name on Card field is not displayed')
        self.assertTrue(self.deposit.expiry_date.is_displayed(), msg='Expiry Date field is not displayed')
#        self.assertTrue(self.deposit.cvv_2.is_displayed(), msg='CVV2 field is not displayed')

    def test_003_update_all_required_fields_tab_on_deposit(self):
        """
        DESCRIPTION: Update all required fields & Tab on Deposit
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: Amount on message is displayed in decimal format
        """
        self.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=tests.settings.master_card,
                                              cvv_2=tests.settings.visa_card_cvv, expiry_date=self.card_date)
        expected_deposit_message = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.deposit_amount)
        actual_deposit_message = self.site.deposit_transaction_details.successful_message
        self.assertEqual(actual_deposit_message, expected_deposit_message,
                         msg=f'Actual message: "{actual_deposit_message}" is not same as Expected: "{expected_deposit_message}"')

    def test_004_click_OK_close_deposit_view_check_balance_in_the_header(self):
        """
        DESCRIPTION: Click "OK"
        DESCRIPTION: Check Balance in the header
        EXPECTED: User is taken to the Homepage
        EXPECTED: Balance is increased on sum of deposit
        """
        self.site.deposit_transaction_details.ok_button.click()
        self.site.wait_content_state('HomePage', timeout=5)
        actual_balance = self.site.header.user_balance
        expected_balance = float(self.deposit_amount)
        self.assertEqual(actual_balance, expected_balance,
                         msg=f'Actual user balance "{actual_balance}" != Expected "{expected_balance}"')
