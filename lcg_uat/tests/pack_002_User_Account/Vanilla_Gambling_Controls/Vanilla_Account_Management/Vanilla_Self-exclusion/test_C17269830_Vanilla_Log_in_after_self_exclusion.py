import voltron.environments.constants as vec
import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result
from datetime import datetime, timedelta, date


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17269830_Vanilla_Log_in_after_self_exclusion(BaseBetSlipTest):
    """
    TR_ID: C17269830
    NAME: [Vanilla] Log in after self-exclusion
    PRECONDITIONS: App is loaded
    PRECONDITIONS: Prepare two users:
    PRECONDITIONS: - UK user
    PRECONDITIONS: - non UK user
    PRECONDITIONS: *For both:*
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'Id like to take an irreversible time-out or exclude myself from gaming' option
    PRECONDITIONS: User clicks the 'Self-exclusion' link, where Self-exclusion option is selected by default and clicks the Choose button
    PRECONDITIONS: User selects the duration and reason of self-exclusion and proceeds by clicking Self Exclude
    PRECONDITIONS: User ticks both ticks on self-exclusion pop-up and proceeds by clicking YES
    PRECONDITIONS: User logs out from the app
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
        PRECONDITIONS: User is logged in
        PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure
        PRECONDITIONS: User selects the 'Id like to take an irreversible time-out or exclude myself from gaming' option
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
            self.site.register_new_user(birth_date='01-06-1977', country='Ireland', state='County Dublin', post_code='A847545',
                                        username=self.user_name,
                                        city='Dublin', currency='EUR')
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
        self.site.self_exclusion.self_exclusion_link.scroll_to()
        self_exclusion_link = self.site.self_exclusion.self_exclusion_link
        self.assertTrue(self_exclusion_link.is_displayed(), msg=f'"Self Exclusion" link is not displayed')
        self_exclusion_link.click()
        images = self.site.self_exclusion_selection.image
        self.assertTrue(images[0].is_enabled(), msg='"Self-exclusion" option is not selected by default')
        self.site.self_exclusion_selection.choose_button.click()
        self_exclusion_options = self.site.self_exclusion_options
        duration = self_exclusion_options.duration_options
        self.assertTrue(duration, msg='"Duration options" are not available')
        reason = self_exclusion_options.reason_options
        self.assertTrue(duration, msg='"Reason options" are not available')
        duration[0].click()
        click(reason[0])
        self.assertTrue(self_exclusion_options.continue_button.is_enabled(),
                        msg=f'Continue button:"{vec.account.CONTINUE}" is not enabled')
        self._logger.info('"Duration" and "Reason" options are selected as continue button is enabled')
        self_exclusion_options.continue_button.click()
        self_exclusion_options = self.site.self_exclusion_options
        self.assertTrue(self_exclusion_options.password_field.is_displayed(),
                        msg='User is not redirected to Self-Exclusion password confirmation page')
        self_exclusion_options.password_input(tests.settings.default_password)
        self.assertTrue(self_exclusion_options.self_exclude_button.is_enabled(),
                        msg='Password was not entered as Self exclude button was not enabled')
        self_exclusion_options.self_exclude_button.click()
        self.assertTrue(self.site.self_exclusion_options.info_message.is_displayed(),
                        msg='Self-exclusion confirmation page was not appeared')
        actual_text = self.site.self_exclusion_options.info_message.text
        self.assertEqual(actual_text, vec.bma.SELF_EXCLUDED_INFO_MESSAGE,
                         msg=f'Actual self-excluded message: "{actual_text}" is not same as Expected self-excluded message: "{vec.bma.SELF_EXCLUDED_INFO_MESSAGE}"')
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

    def test_002_log_in_using_credentials_of_self_excluded_uk_user(self):
        """
        DESCRIPTION: Log in using credentials of self-excluded UK user
        EXPECTED: Error message appears on the login pop-up:
        EXPECTED: "Account Inaccessible
        EXPECTED: Your account is locked because you have chosen to self-exclude yourself from our products."
        EXPECTED: ![](index.php?/attachments/get/35867)
        """
        self.dialog.username = self.user_name
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        actual_error_message = wait_for_result(lambda: self.site.login_dialog.error_message,
                                               name='error message will be displayed')
        self.assertEqual(actual_error_message, vec.bma.SELF_EXCLUDED_LOGIN_ERROR_MESSAGE,
                         msg=f'User: "{self.user_name}" is not excluded from Products')

    def test_003_log_in_using_credentials_of_self_excluded_non_uk_user(self):
        """
        DESCRIPTION: Log in using credentials of self-excluded non UK user
        EXPECTED: User is able to log in.
        """
        self.test_000_preconditions(uk=False)
        self.test_001_click_the_login_button()
        self.dialog.username = self.user_name
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        expected_error_message = 'Your account is currently blocked because you’ve opted to take a time-out. You’ll not be able to access your account until'
        actual_error_message = wait_for_result(lambda: self.site.login_dialog.error_message,
                                               name='error message will be displayed')
        self.assertIn(expected_error_message, actual_error_message,
                      msg=f'User: "{self.user_name}" is not excluded from Products')
        self.__class__.excluded_date = date.today() + timedelta(days=1)
        if self.excluded_date.day <= 9:
            day = f'0{self.excluded_date.day}'
        else:
            day = self.excluded_date.day
        if self.excluded_date.month <= 9 and self.brand == 'ladbrokes':
            month = f'0{self.excluded_date.month}'
        else:
            month = self.excluded_date.month
        if self.brand == 'bma':
            formatted_date = f'{month}/{day}/{str(self.excluded_date.year)[-2:]}'
        else:
            formatted_date = f'{day}/{month}/{str(self.excluded_date.year)[-2:]}'
        self.assertIn(formatted_date, actual_error_message,
                      msg=f'Selected time out date: "{formatted_date}" is not present in the Time out error message: '
                          f'"{actual_error_message}"')
