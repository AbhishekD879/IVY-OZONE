import pytest
import tests
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.deposit
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1532')
@vtest
class Test_C17013227_Vanilla_Verify_successful_Deposit_via__Mastercard_Credit_Card(BaseUserAccountTest):
    """
    TR_ID: C17013227
    NAME: [Vanilla] Verify successful Deposit via Mastercard Credit Card
    DESCRIPTION: This test case verifies successful deposit functionality for Mastercard payment method
    """
    keep_browser_open = True
    deposit_amount = 5.15
    payment_card = tests.settings.master_card

    def test_000_preconditions(self):
        """
        DESCRIPTION:
        PRECONDITIONS: User has registered supported cards(e.g Mastercard);
        PRECONDITIONS: Balance of card is enough for deposit from;
        PRECONDITIONS: User logged into the application;
        PRECONDITIONS: Confluence page for payments test data https://confluence.egalacoral.com/display/SPI/GVC+Payment+Methods
        """
        self.__class__.username = tests.settings.master_card_user
        self.site.login(username=self.username)
        self.site.wait_content_state('HomePage')
        self.__class__.initial_balance = self.site.header.user_balance

    def test_001_click_on_user_avatar_icon_on_the_header(self):
        """
        DESCRIPTION: Click on User "Avatar" icon on the header
        EXPECTED: User menu is opened
        """
        self.site.header.right_menu_button.avatar_icon.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')

    def test_002_click_on_cashier_section_in_user_menu(self):
        """
        DESCRIPTION: Click on "Deposit" section in User menu
        EXPECTED: Cashier Menu is opened and "Deposit" section is present in the list
        """
        cashier_title = self.site.window_client_config.cashier_menu_title
        self.site.right_menu.click_item(item_name=cashier_title)
        result = wait_for_result(lambda: self.site.right_menu.header.title == cashier_title,
                                 name='Wait for header title to change')
        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                        f'expected "{cashier_title}"')
        sections = self.site.right_menu.items_names
        deposit = self.site.window_client_config.deposit_menu_title
        self.assertIn(deposit, sections,
                      msg=f'"{deposit}" is not found in "{sections}"')

    def test_003_click_on_deposit_section(self):
        """
        DESCRIPTION: Click on "Deposit" section
        EXPECTED: Deposit page with Mastercard payment method is opened
        EXPECTED: Note - for test users Deposit page with Mastercard payment method is opened
        """

        self.site.right_menu.click_item(item_name=self.site.window_client_config.deposit_menu_title)
        self.assertTrue(self.site.deposit.is_displayed(scroll_to=False),
                        msg='"Deposit" menu is not displayed')

    def test_004_select_mastercard_payment_method(self):
        """
        DESCRIPTION: Select Mastercard payment method
        EXPECTED: Deposit page with Mastercard payment method is opened
        """
        # Skipping this step according to the note in step #3
        pass

    def test_005_enter_valid_cv2_into_cv2_field(self):
        """
        DESCRIPTION: Enter valid CV2 into CV2 field
        EXPECTED: CV2 is entered.
        """
        if self.brand == 'bma':
            self.__class__.deposit_menu = self.site.deposit
            self.deposit_menu.cvv_2.input.value = tests.settings.master_card_cvv
            actual_cvv2 = self.deposit_menu.cvv_2.input.value
            self.assertEqual(actual_cvv2, tests.settings.master_card_cvv,
                             msg=f'Actual CVV2 "{actual_cvv2}" != Expected "{tests.settings.master_card_cvv}"')
        else:
            self.site.deposit.deposit_and_close(amount=self.deposit_amount, cvv_2=tests.settings.master_card_cvv)

    def test_006_enter_valid_amount_manually_or_using_plus_minus_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using '+', '-' buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        if self.brand == 'bma':
            self.deposit_menu.amount.input.value = self.deposit_amount
            actual_amount = self.deposit_menu.amount.input.value
            expected_amount = str(self.deposit_amount)
            self.assertEqual(actual_amount, expected_amount,
                             msg=f'Actual amount "{actual_amount}" != Expected "{expected_amount}"')

    def test_007_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Successful message: 'Your deposit of <currency symbol> XX.XX has been successful' appears
        *Successful message verification will not be automated*
        """
        if self.brand == 'bma':
            self.deposit_menu.deposit_button.click()
            wait_for_result(lambda: self.site.deposit_transaction_details.ok_button.is_displayed(),
                            name='OK button is displayed',
                            timeout=5)
            self.site.deposit_transaction_details.ok_button.click()

    def test_008_close_deposit_viewcheck_balance_in_the_header(self):
        """
        DESCRIPTION: Close Deposit view
        DESCRIPTION: Check Balance in the header
        EXPECTED: Balance is increased on sum of deposit
        """
        self.navigate_to_page("Homepage")
        self.site.wait_content_state('HomePage', timeout=5)
        expected_user_balance = float(self.deposit_amount + self.initial_balance)
        self.verify_user_balance(expected_user_balance, timeout=5)
