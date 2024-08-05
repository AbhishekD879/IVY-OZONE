import voltron.environments.constants as vec
import pytest
import tests
from datetime import datetime, timedelta, date
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C18258206_Vanilla_Log_in_after_time_out(BaseBetSlipTest):
    """
    TR_ID: C18258206
    NAME: [Vanilla] Log in after time-out
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'
    shifted_year = str(now.year + 5)
    card_date = f'{now.month:02d}/{shifted_year[-2:]}'

    def test_000_preconditions(self, uk=True):
        """
        PRECONDITIONS: App is loaded
        PRECONDITIONS: Prepare two users:
        PRECONDITIONS: - UK user
        PRECONDITIONS: - non UK user
        PRECONDITIONS: For both:
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Management
        PRECONDITIONS: User selects option - 'Id like to take an irreversible time-out or exclude myself from gaming'
        PRECONDITIONS: User selects the duration and reason of time-out and proceeds by clicking Continue (**remember selected date**)
        PRECONDITIONS: User clicks 'Take a short time-out' button
        PRECONDITIONS: User logs out from the app
        """
        if uk:
            self.__class__.user_name = self.gvc_wallet_user_client.register_new_user().username
            self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=self.deposit_amount,
                                                                     card_number=tests.settings.master_card,
                                                                     card_type='mastercard',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
            self.site.login(username=self.user_name)
        else:
            self.navigate_to_page(name='home')
            self.__class__.user_name = self.generate_user()
            self.site.register_new_user(birth_date='01-06-1977', country='Ireland', state='County Dublin',
                                        post_code='A847545', username=self.user_name, city='Dublin', currency='EUR')
            self.assertTrue(self.site.wait_content_state("Homepage"))
            self.site.header.right_menu_button.click()
            if self.brand == 'bma':
                self.site.right_menu.click_item(item_name='Banking')
            else:
                self.site.right_menu.click_item(item_name='Banking & Balances')
            self.site.right_menu.click_item(item_name='Deposit')
            self.__class__.select_deposit_method = self.site.select_deposit_method
            self.assertTrue(wait_for_result(lambda: self.select_deposit_method.deposit_title.is_displayed(), timeout=5),
                            msg='"Deposit page" is not displayed')
            self.select_deposit_method.master_card_button.click()
            self.__class__.deposit = self.site.deposit
            self.assertTrue(self.deposit.amount.is_displayed(), msg='Enter Amount field is not displayed')
            self.assertTrue(self.deposit.card_number.is_displayed(), msg='Card number field is not displayed')
            self.assertTrue(self.deposit.card_holder.is_displayed(), msg='Name on Card field is not displayed')
            self.assertTrue(self.deposit.expiry_date.is_displayed(), msg='Expiry Date field is not displayed')
            self.assertTrue(self.deposit.cvv_2.is_displayed(), msg='CVV2 field is not displayed')
            self.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=tests.settings.master_card,
                                                  cvv_2=tests.settings.master_card_cvv, expiry_date=self.card_date)
            expected_deposit_message = 'Your deposit of 20.00 EUR has been successful'
            actual_deposit_message = self.site.deposit_transaction_details.successful_message
            self.assertEqual(actual_deposit_message, expected_deposit_message,
                             msg=f'Actual message: "{actual_deposit_message}" is not same as Expected: "{expected_deposit_message}"')
            self.site.deposit_transaction_details.ok_button.click()
        self.site.wait_content_state("Homepage")
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=20)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.site.account_closure.click_item(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2)
        self.site.account_closure.continue_button.click()
        self.site.self_exclusion.duration_options[0].click()
        click(self.site.self_exclusion.reason_options[0])
        self.assertTrue(self.site.self_exclusion.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')
        self.site.self_exclusion.continue_button.click()
        self.__class__.date_time = self.site.self_exclusion.date_time.text
        self.assertTrue(self.site.self_exclusion.take_short_time_out.is_enabled(),
                        msg='"Take short time out" button is not enabled')
        self.__class__.excluded_date = date.today() + timedelta(weeks=1)
        ui_date = self.site.self_exclusion.date_time.text.split(',')[0]
        if self.excluded_date.day <= 9:
            day = f'0{self.excluded_date.day}'
        else:
            day = self.excluded_date.day
        if self.excluded_date.month <= 9:
            month = f'0{self.excluded_date.month}'
        else:
            month = self.excluded_date.month
        formated_date = f'{day}/{month}/{str(self.excluded_date.year)}'
        self.assertEqual(formated_date, ui_date,
                         msg=f'Selected time out date: "{formated_date}" is not same as Displayed time out date "{ui_date}"')
        self.site.self_exclusion.take_short_time_out.click()
        take_short_time_out_info_meaasage = self.site.self_exclusion.consequences_info_message.text
        self.assertEqual(take_short_time_out_info_meaasage, vec.account.CONSEQUENCES_INFO_MESSAGE,
                         msg=f'Actual Time Out Message: "{take_short_time_out_info_meaasage}" is not same as Expected'
                             f'Time Out Message: "{vec.account.CONSEQUENCES_INFO_MESSAGE}"')
        self.navigate_to_page("Homepage")
        self.site.logout()
        self.site.wait_logged_out(10)

    def test_001_click_the_login_button(self):
        """
        DESCRIPTION: Click the LOGIN button
        EXPECTED: Login pop-up appears
        """
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='Login dialog not displayed')

    def test_002_log_in_using_credentials_of_timed_out_uk_user(self):
        """
        DESCRIPTION: Log in using credentials of timed-out UK user
        EXPECTED: Error message appears on the login pop-up:
        EXPECTED: "Account Inaccessible
        EXPECTED: Your account is currently blocked because you have opted to take a time-out. You will not be able to access your account until <date> <time>"
        EXPECTED: ![](index.php?/attachments/get/35870)
        """
        self.dialog.username = self.user_name
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        expected_error_message = 'Your account is currently blocked because you’ve opted to take a time-out. You’ll not be able to access your account until'
        self.__class__.actual_error_message = wait_for_result(lambda: self.site.login_dialog.error_message,
                                                              name='error message will be displayed')
        self.assertIn(expected_error_message, self.actual_error_message,
                      msg=f'User: "{self.user_name}" is not excluded from Products')

    def test_003_validate_the_date_and_time_of_time_out(self):
        """
        DESCRIPTION: Validate the date and time of time-out
        EXPECTED: Date and time is the same as the one selected as duration
        """
        if self.excluded_date.day <= 9:
            day = f'0{self.excluded_date.day}'
        else:
            day = self.excluded_date.day
        if self.excluded_date.month <= 9 and self.brand == 'ladbrokes':
            month = f'0{self.excluded_date.month}'
        else:
            month = self.excluded_date.month
        if self.brand == 'bma':
            formated_date = f'{month}/{day}/{str(self.excluded_date.year)[-2:]}'
        else:
            formated_date = f'{day}/{month}/{str(self.excluded_date.year)[-2:]}'
        self.assertIn(formated_date, self.actual_error_message,
                      msg=f'Selected time out date: "{formated_date}" is not present in the Time out error message: '
                          f'"{self.actual_error_message}"')
        # time can't be verified

    def test_004_log_in_using_credentials_of_timed_out_non_uk_user(self):
        """
        DESCRIPTION: Log in using credentials of timed-out non UK user
        EXPECTED: User is able to log in.
        """
        self.test_000_preconditions(uk=False)
        self.test_001_click_the_login_button()
        self.test_002_log_in_using_credentials_of_timed_out_uk_user()
        self.test_003_validate_the_date_and_time_of_time_out()
