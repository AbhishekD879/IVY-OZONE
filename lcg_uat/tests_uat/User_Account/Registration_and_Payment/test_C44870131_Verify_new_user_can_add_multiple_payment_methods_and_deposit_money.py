import pytest
import tests
import voltron.environments.constants as vec
import datetime
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.user_account
@pytest.mark.deposit
@pytest.mark.medium
@pytest.mark.registration
@vtest
class Test_C44870131_Verify_new_user_can_add_multiple_payment_methods_and_deposit_money(Common):
    """
    TR_ID: C44870131
    NAME: Verify new user can add multiple payment methods and deposit money
    DESCRIPTION: Note: For test accounts only Master card, Visa & Maestro are available.
    PRECONDITIONS: User is logged in.
    PRECONDITIONS: In order to get number of credit card the following links can be used:
    PRECONDITIONS: http://www.getcreditcardnumbers.com/how-to-get-a-master-card-credit-card
    PRECONDITIONS: http://www.getcreditcardnumbers.com/how-to-get-a-visa-credit-card
    """
    keep_browser_open = True
    deposit_amount = 5.00

    def deposit_money_and_verify_user_balance(self, card_number, cvv):
        self.site.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=card_number,
                                                   cvv_2=cvv, expiry_date=self.card_date)
        expected_deposit_message = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.deposit_amount)
        actual_deposit_message = self.site.deposit_transaction_details.successful_message
        self.assertEqual(actual_deposit_message, expected_deposit_message,
                         msg=f'Actual message "{actual_deposit_message}" is not same as '
                             f'Expected "{expected_deposit_message}"')
        self.site.deposit_transaction_details.ok_button.click()
        self.site.wait_content_state('HomePage', timeout=5)
        self.verify_user_balance(expected_user_balance=self.user_balance + float(self.deposit_amount))
        self.__class__.user_balance = self.user_balance + float(self.deposit_amount)

    def navigate_to_right_menu_and_click_on_deposit(self):
        self.site.header.right_menu_button.click()
        right_menu = self.site.right_menu
        self.assertTrue(right_menu,
                        msg='Right menu is not opened')
        self.assertTrue(right_menu.has_deposit_button(),
                        msg='Quick Deposit button is not displayed in right menu')
        right_menu.deposit_button.click()

    def test_000_preconditions(self):
        """
        DESCRIPTION: User is registered
        EXPECTED: User has registered successfully
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[2:]}'
        user = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user)

    def test_001_tap_on_the_balance_or_avataron_the_top_right_of_the_appweb_Tap_Deposit_button_bottom_of_the_page(self):
        """
        DESCRIPTION: Tap on the 'Balance' or 'Avatar'on the top right of the App/Web
        DESCRIPTION: Tap 'Deposit' button on the bottom of the page
        EXPECTED: My Balance & Menu is opened respectively.
        EXPECTED: 'Deposit' page is opened
        """
        self.navigate_to_right_menu_and_click_on_deposit()
        sleep(30)
        self.assertTrue(self.site.select_deposit_method.deposit_title.is_displayed(),
                        msg='"Deposit page" is not displayed')

    def test_002_Select_payment_option_page_is_displayed_with_following_fields(self):
        """
        DESCRIPTION: Select payment option page is displayed with following fields
        EXPECTED: VISA/MASTERCARD/MAESTRO are available
        """
        self.__class__.deposit_method = self.site.select_deposit_method
        self.assertTrue(self.deposit_method.visa_button.is_displayed(), msg='"Visa card" is not available')
        self.assertTrue(self.deposit_method.master_card_button.is_displayed(), msg='"Master card" is not available')
        self.assertTrue(self.deposit_method.maestro_button.is_displayed(), msg='"Maestro card" is not available')

    def test_003_verify_adding_of_visa_card_fill_in_all_required_fields_and_tap_Deposit_button(self):
        """
        DESCRIPTION: Verify adding of '**Visa**' card
        DESCRIPTION: Fill in all required fields and tap 'Deposit' button
        EXPECTED: Deposit page with Visa card payment method is opened
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        """
        self.deposit_method.master_card_button.click()
        self.assertTrue(self.site.deposit.deposit_title.is_displayed(),
                        msg='Deposit page with visa card payment method is not opened')
        if tests.settings.backend_env == 'prod':
            self.site.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=tests.settings.master_card,
                                                       cvv_2=tests.settings.master_card_cvv, expiry_date=self.card_date)
        else:
            self.site.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=4142731270314439,
                                                       cvv_2=tests.settings.visa_card_cvv, expiry_date=self.card_date)
        expected_deposit_message = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.deposit_amount)
        actual_deposit_message = self.site.deposit_transaction_details.successful_message
        self.assertEqual(expected_deposit_message, actual_deposit_message,
                         msg=f'Actual message "{actual_deposit_message}" is not same as '
                             f'Expected "{expected_deposit_message}"')

    def test_004_click_OK_Verify_user_Balance(self):
        """
        DESCRIPTION: Click OK
        EXPECTED: User is taken to homepage
        """
        self.site.deposit_transaction_details.ok_button.click()
        self.site.wait_content_state('Homepage')
        self.navigate_to_page('/')
        self.__class__.user_balance = self.site.header.user_balance
        self.assertEqual(self.user_balance, float(self.deposit_amount),
                         msg=f'Actual user balance "{self.user_balance}" is not equal to '
                             f'Expected "{float(self.deposit_amount)}"')

    def test_005_tap_deposit_button_on_the_bottom_of_the_page_click_on_down_arrow_loacted_next_to_the_current_card(self):
        """
        DESCRIPTION: Tap 'Deposit' button on the bottom of the page
        DESCRIPTION: Click on the Down arrow located next to the Current card number
        EXPECTED: 'Deposit' page is opened with Amount/Card number/ CVV etc
        EXPECTED: 'Other payment options' available.
        """
        self.navigate_to_right_menu_and_click_on_deposit()
        self.__class__.quick_deposit_menu = self.site.deposit.stick_to_iframe()
        self.assertTrue(self.quick_deposit_menu, msg='Deposit page is not opened')
        self.assertTrue(self.quick_deposit_menu.amount.is_displayed(), msg='Enter Amount field is not displayed')
        self.assertTrue(self.quick_deposit_menu.accounts.is_displayed(), msg='Accounts field is not displayed')
        self.assertTrue(self.quick_deposit_menu.cvv_2.is_displayed(), msg='CVV2 field is not displayed')

        self.quick_deposit_menu.accounts.click()
        select_menu_list = self.quick_deposit_menu.accounts.select_menu.items_names
        self.assertIn(vec.bma.OTHER_PAYMENT_OPTIONS, select_menu_list,
                      msg=f'"{vec.bma.OTHER_PAYMENT_OPTIONS}" option is not available')

    def test_006_Click_on_Other_payment_options_to_add_a_new_card(self):
        """
        DESCRIPTION: Click on 'Other payment options' to add a new card
        EXPECTED: VISA/MASTERCARD/MAESTRO are available
        """
        self.quick_deposit_menu.accounts.select_menu.click_item(vec.bma.OTHER_PAYMENT_OPTIONS)
        sleep(20)
        if self.device_type == 'desktop':
            self.site.select_deposit_method.back_button.click()
        else:
            self.site.select_deposit_method.add_payment_methods.click()
        self.test_002_Select_payment_option_page_is_displayed_with_following_fields()

    def test_007_verify_adding_depositing_via_master_card_card_Verify_user_Balance(self):
        """
        DESCRIPTION: Verify adding and depositing via '**Master Card**' card
        DESCRIPTION: Verify user Balance
        EXPECTED: User is able to add the Master card
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: Balance is increased on sum of deposit
        """
        self.site.select_deposit_method.visa_button.click()
        self.deposit_money_and_verify_user_balance(card_number=tests.settings.visa_card,
                                                   cvv=tests.settings.visa_card_cvv)

    def test_008_tap_on_the_balance_or_avataron_the_top_right_of_the_appwebtap_deposit_button_on_the_bottom_of_the_page(
            self):
        """
        DESCRIPTION: Tap on the 'Balance' or 'Avatar'on the top right of the App/Web
        DESCRIPTION: Tap 'Deposit' button on the bottom of the page
        EXPECTED: 'Deposit' page is opened
        """
        self.site.close_all_banners()
        self.site.close_all_dialogs()
        self.navigate_to_right_menu_and_click_on_deposit()
        sleep(10)
        # self.site.select_deposit_method.add_payment_methods.click()

    def test_009_and_now_click_on_all_options_on_the_deposit_cashier_page(self):
        """
        DESCRIPTION: and now click on "All options" on the Deposit cashier page
        EXPECTED: Page with all options of cards are available.
        EXPECTED: Eg: VISA/MASTERCARD/MAESTRO are available
        """
        self.site.select_deposit_method.back_button.click()
        self.test_002_Select_payment_option_page_is_displayed_with_following_fields()

    def test_010_verify_adding_and_depositing_via_maestro_cardverify_user_balance(self):
        """
        DESCRIPTION: Verify adding and depositing via '**Maestro**' card.
        DESCRIPTION: Verify user Balance
        EXPECTED: User is able to add the Maestro card.
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: Balance is increased on sum of deposit.
        """
        # Maestro card is not available
        # todo : When maestro card is available need to complete this step
        # self.site.select_deposit_method.maestro_button.click()
        # self.deposit_money_and_verify_user_balance(card_number=tests.settings.maestro_card,
        #                                            cvv=tests.settings.maestro_card_cvv)
