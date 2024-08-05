import datetime
import pytest
import tests
import voltron.environments.constants as vec
from faker import Faker
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.critical
@pytest.mark.deposit
@pytest.mark.desktop
@pytest.mark.user_account
@pytest.mark.login
@vtest
class Test_C17987900_Vanilla_Verify_successful_first_Deposit(BaseUserAccountTest):
    """
    TR_ID: C17987900
    NAME: [Vanilla] Verify successful first Deposit
    DESCRIPTION: This test case verifies successful first deposit flow using any of supported payment methods
    PRECONDITIONS: User has no registered any cards and user balance is 0.
    PRECONDITIONS: User logged into the application;
    PRECONDITIONS: Confluence page for payments test data https://confluence.egalacoral.com/display/SPI/GVC+Payment+Methods
    """
    keep_browser_open = True
    deposit_amount = 10.49
    now = datetime.datetime.now()
    shifted_year = str(now.year + 5)
    exp_card_date = f'{now.month:02d}/{shifted_year[2:]}'
    f = Faker()

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User has no registered any cards and user balance is 0.
        PRECONDITIONS: User logged into the application;
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[:-2]}'

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_001_click_on_user_avatar_icon_on_the_header(self):
        """
        DESCRIPTION: Click on User "Avatar" icon on the header
        EXPECTED: User menu is opened
        """
        self.__class__.initial_user_balance = self.site.header.user_balance
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(),
                        msg='User menu is not opened')

    def test_002_click_on_cashier_section_in_user_menu(self):
        """
        DESCRIPTION: Click on "Cashier" section in User menu
        EXPECTED: Cashier Menu is opened and "Deposit" section is present in the list
        """
        self.site.right_menu.click_item(item_name=self.site.window_client_config.cashier_menu_title, timeout=7)
        deposit = self.site.window_client_config.deposit_menu_title
        result = wait_for_result(lambda: deposit in self.site.right_menu.items_names,
                                 name='Menu items to load',
                                 timeout=7,
                                 bypass_exceptions=VoltronException)
        self.assertTrue(result, msg=f'"{deposit}" is not found in "{self.site.right_menu.items_names}"')

    def test_003_click_on_deposit_section(self):
        """
        DESCRIPTION: Click on "Deposit" section
        EXPECTED: "Deposit" menu is opened with a list of all available payment methods for the User;
        EXPECTED: e.g:
        EXPECTED: VISA
        EXPECTED: MasterCard
        EXPECTED: etc.
        """
        self.site.right_menu.click_item(item_name=self.site.window_client_config.deposit_menu_title, timeout=7)
        select_deposit_method = self.site.select_deposit_method
        available_deposit_options = select_deposit_method.items_as_ordered_dict
        self.assertTrue(available_deposit_options, msg='No deposit options available')

        if 'visa' in available_deposit_options.keys():
            self.__class__.deposit_option_name = 'visa'
        elif 'mastercard' in available_deposit_options.keys():
            self.__class__.deposit_option_name = 'mastercard'
        elif 'card' in available_deposit_options.keys():
            self.__class__.deposit_option_name = 'card'

        if self.deposit_option_name in available_deposit_options.keys():
            self.__class__.deposit_option = available_deposit_options.get(self.deposit_option_name)
        else:
            raise VoltronException(f'"{self.deposit_option_name}" payment method is not available')

        self.assertIsNotNone(self.deposit_option, msg=f'Deposit option for "{self.deposit_option_name}" is absent')
        self.assertTrue(self.deposit_option.is_displayed(),
                        msg=f'"{self.deposit_option_name}" payment method is not displayed')

    def test_004_select_any_payment_method_eg_mastercard(self):
        """
        DESCRIPTION: Select any payment method (e.g. MasterCard)
        EXPECTED: Deposit page with selected(e.g. MasterCard) payment method is opened
        """
        self.deposit_option.click()
        self.assertTrue(self.site.deposit.is_displayed(), msg='"Deposit page" is not displayed')

    def test_005_enter_credit_card_number(self):
        """
        DESCRIPTION: Enter credit card number (e.g. 5137658844677245)
        EXPECTED: card number is entered. Green tick appears in card number field
        """
        self.site.deposit.card_number.input.value = tests.settings.visa_card
        actual_card_number = self.site.deposit.card_number.input.value.replace(' ', '')
        result = wait_for_result(lambda: actual_card_number == tests.settings.visa_card,
                                 name='Card number to be entered',
                                 timeout=5)
        self.assertTrue(result, msg=f'Card number "{actual_card_number}" is not displayed')
        self.assertTrue(self.site.deposit.card_number.is_valid_with_green_tick(),
                        msg='"Green tick" is not displayed')

    def test_006_enter_credit_card_name(self):
        """
        DESCRIPTION: Enter credit card name
        EXPECTED: card name is entered. Name tick appears in card name field
        """
        name = self.f.name()
        self.site.deposit.card_holder.input.value = name
        actual_card_holder = self.site.deposit.card_holder.input.value
        self.assertEqual(actual_card_holder, name,
                         msg=f'Actual card holder "{actual_card_holder}" != Expected "{name}"')
        self.assertTrue(self.site.deposit.card_holder.is_valid_with_green_tick(),
                        msg='"Green tick" is not displayed')

    def test_007_enter_expiry_date(self):
        """
        DESCRIPTION: Enter Expiry date
        EXPECTED: The expiry date is entered. Green tick appears in the Expiry date field
        """
        self.site.deposit.expiry_date.input.value = self.exp_card_date
        actual_card_expiry_date = self.site.deposit.expiry_date.input.value
        self.assertEqual(actual_card_expiry_date, self.exp_card_date,
                         msg=f'Actual card expiry date "{actual_card_expiry_date}" != Expected "{self.exp_card_date}"')
        self.assertTrue(self.site.deposit.expiry_date.is_valid_with_green_tick(),
                        msg='"Green tick" is not displayed')

    def test_008_enter_valid_cv2_into_cv2_field(self):
        """
        DESCRIPTION: Enter valid CV2 into CV2 field
        EXPECTED: CV2 is entered. Green tick appears in CV2 field
        """
        self.site.deposit.cvv_2.input.value = tests.settings.visa_card_cvv
        actual_cvv2 = self.site.deposit.cvv_2.input.value
        self.assertEqual(actual_cvv2, tests.settings.visa_card_cvv,
                         msg=f'Actual CVV2 "{actual_cvv2}" != Expected "{tests.settings.visa_card_cvv}"')
        self.assertTrue(self.site.deposit.cvv_2.is_valid_with_green_tick(),
                        msg='"Green tick" is not displayed')

    def test_009_enter_valid_amount_manually_or_using_plus_minus_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using '+', '-' buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        self.site.deposit.amount.input.value = self.deposit_amount
        actual_amount = self.site.deposit.amount.input.value
        expected_amount = str(self.deposit_amount)
        self.assertEqual(actual_amount, expected_amount,
                         msg=f'Actual amount "{actual_amount}" != Expected "{expected_amount}"')

    def test_010_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Successful message: 'Your deposit of <currency symbol> XX.XX has been successful' appears
        """
        self.site.deposit.deposit_button.click()
        expected = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.deposit_amount)
        actual = self.site.deposit_transaction_details.successful_message
        self.assertEqual(actual, expected,
                         msg=f'Actual message "{actual}" != Expected "{expected}"')

    def test_011_close_deposit_view_check_balance_in_the_header(self):
        """
        DESCRIPTION: Close Deposit view
        DESCRIPTION: Check Balance in the header
        EXPECTED: Balance is increased on sum of deposit
        """
        self.site.deposit_transaction_details.ok_button.click()
        self.site.wait_content_state(state_name='HomePage', timeout=5)

        actual = self.site.header.user_balance
        expected = float(self.deposit_amount) + self.initial_user_balance
        self.assertEqual(actual, expected,
                         msg=f'Actual user balance "{actual}" != Expected "{expected}"')
