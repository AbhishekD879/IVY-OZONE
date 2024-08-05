import datetime
import pytest
import random
import tests
import voltron.environments.constants as vec
from time import time
from tests.base_test import vtest
from tests.Common import Common
from faker import Faker
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import string_generator
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.user_account
@pytest.mark.hotfix
@pytest.mark.sanity
@vtest
class Test_C34298265_Register_and_Add_Credit_Card(Common):
    """
    TR_ID: C34298265
    NAME: Register and Add Credit Card
    DESCRIPTION: Verify that the user can Register and add a Credit Card as payment method
    PRECONDITIONS: Note: Registration and Payment methods are handled on GVC side.
    PRECONDITIONS: * Documentation for user registration and payment methods:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+create+test+user+for+GVC+Vanilla+automatically+by-passing+KYC
    """
    keep_browser_open = True
    user = {"social_title": "Mr.",
            "first_name": Faker().first_name_female(),
            "last_name": Faker().last_name_female(),
            "birth_date": f'{random.randint(1,30)}-06-1977',
            "country": "United Kingdom",
            "email": f'test{time()}@internalgvc.com',
            "username": f'{tests.settings.registration_pattern_prefix}{string_generator(size=7)}'[:17],
            "password": tests.settings.default_password,
            }

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Generate card date
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[2:]}'

    def test_001_open_oxygen_app(self):
        """
        DESCRIPTION: Open Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('HomePage')

    def test_002_click_on_join_button(self):
        """
        DESCRIPTION: Click on 'JOIN' button
        EXPECTED: Registration Overlay is opened
        """
        self.site.header.join_us.click()
        self.__class__.three_step_form = wait_for_result(lambda : self.site.three_steps_registration, timeout=20, bypass_exceptions = VoltronException)
        self.assertTrue(self.three_step_form.form_step1,
                        msg='Page "Registration - Step 1 of 3" is  not shown')

    def test_003_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Country residence ( use 'United Kingdom')and currency
        DESCRIPTION: 2. Email (for internal accounts use *username*@internalgvc.com)
        DESCRIPTION: 3. Username (for internal accounts use testgvccl-*username*)
        DESCRIPTION: 4. Password
        """
        self.three_step_form.form_step1.enter_values(
            country=self.user['country'],
            email=self.user['email'],
            username=self.user['username'],
            password=self.user['password'],
        )

    def test_004_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button
        EXPECTED: Registration Step 2 is opened
        """
        self.three_step_form.submit_step1()

    def test_005_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Title: Mr/Ms
        DESCRIPTION: 2. First name
        DESCRIPTION: 3. Last name
        DESCRIPTION: 4. Date of birth (random day/month/year, 18 years plus)
        """
        self.three_step_form.form_step2.enter_values(
            social_title=self.user['social_title'],
            first_name=self.user['first_name'],
            last_name=self.user['last_name'],
            birth_date=self.user['birth_date'],
        )

    def test_006_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button
        EXPECTED: Registration Step 3 is opened
        """
        self.three_step_form.submit_step2()

    def test_007_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Postcode (use postcode 12345 and select suggested address)
        DESCRIPTION: 2. Phone number( use 07911123456)
        DESCRIPTION: 3. Checkboxes to receive FreeBets, bonuses and offers from Coral via ( choose any)
        """
        try:
            self.three_step_form.form_step3.enter_values()
        except Exception:
            if self.use_browser_stack:
                try:
                    self.three_step_form.submit_step2()
                    self.three_step_form.form_step3.enter_values()
                except VoltronException:
                    self.three_step_form.form_step3.enter_values()
        self.three_step_form.form_step3.all_marketing_options_checkbox.click()

    def test_008_click_on_create_my_account_button(self):
        """
        DESCRIPTION: Click on 'CREATE MY ACCOUNT' button
        EXPECTED: Desktop: 'SET YOUR DEPOSIT LIMITS' pop-up appears with option to close (x)
        EXPECTED: Mobile/Tablet:'SET YOUR DEPOSIT LIMITS' overlay appears with option to close (x)
        """
        self.three_step_form.submit_step3()
        if self.brand == 'bma':
            page_title = self.site.set_your_deposit_limits.header_line.page_title
            self.assertEqual(page_title, vec.gvc.SET_YOUR_DEPOSIT_LIMITS_TITLE,
                             msg=f'Actual page title "{page_title}" != '
                                 f'Expected "{vec.gvc.SET_YOUR_DEPOSIT_LIMITS_TITLE}"')
        has_close_btn = self.site.set_your_deposit_limits.header_line.has_close_button()
        self.assertTrue(has_close_btn, msg='Close button is not displayed')

    def test_009_choose_any_deposit_limit_select_checkbox_for_privacy_policy_click_submit_button(self):
        """
        DESCRIPTION: * Choose any deposit limit
        DESCRIPTION: * Select checkbox for privacy policy
        DESCRIPTION: * Click 'SUBMIT' button
        EXPECTED: Deposit page is opened with message on green panel:
        EXPECTED: Select A Payment Option & Make A Deposit To Claim Your Welcome Bonus!'and payment methods available ( e.g. Visa, Mastercard, Maestro)
        """
        self.site.set_your_deposit_limits.set_limits()

        successful_message = self.site.select_deposit_method.successful_message

        select_deposit_method = self.site.select_deposit_method
        available_deposit_options = select_deposit_method.items_as_ordered_dict
        self.assertTrue(available_deposit_options, msg='No deposit options available')

        # This change is for Using Master Card instead of Visa Card:
        deposit_option_name = 'Mastercard'
        expected_message = "HI " + self.user['first_name'].upper() + "! " + vec.gvc.MAKE_DEPOSIT_MESSAGE_TST2
        if deposit_option_name in available_deposit_options.keys():
            self.__class__.deposit_option = available_deposit_options.get(deposit_option_name)
        else:
            raise VoltronException(f'"{deposit_option_name}" payment method is not available')

        self.assertEqual(expected_message.upper(), successful_message.upper(),
                         msg=f'Expected message "{expected_message.upper()}" is not same as '
                             f'Actual "{successful_message.upper()}"')
        self.assertIsNotNone(self.deposit_option, msg=f'Deposit option for "{deposit_option_name}" is absent')
        self.assertTrue(self.deposit_option.is_displayed(),
                        msg=f'"{deposit_option_name}" payment method is not displayed')
        self.site.select_deposit_method.master_card_button.click()

        self.assertTrue(self.site.deposit.is_displayed(),
                        msg='"Deposit page" is not displayed')

    def test_010_choose_any_payment_method(self):
        """
        DESCRIPTION: Choose any payment method ( one from Visa, Mastercard, Maestro) and fill in the required data:
        DESCRIPTION: - Amount ( choose 20)
        DESCRIPTION: - Credit card number - (Use credit card added in documentation in Preconditions)
        DESCRIPTION: - Expiration date - any valid date in the future (e.g. 12.2018)
        DESCRIPTION: - CVV2 ( e.g. 123)
        """
        self.__class__.deposit_amount = 10.49
        # This change is for Using Master Card instead of Visa Card
        self.site.deposit.card_number.input.send_keys(keys=tests.settings.master_card)
        actual_card_number = self.site.deposit.card_number.input.value
        actual_card_number = actual_card_number.replace(' ', '')

        # This change is for Using Master Card instead of Visa Card
        self.assertEqual(actual_card_number, tests.settings.master_card,
                         msg=f'Actual card number "{actual_card_number}" != Expected "{tests.settings.master_card}"')
        self.assertTrue(self.site.deposit.card_number.is_valid_with_green_tick(),
                        msg='"Green tick" is not displayed')

        self.site.deposit.expiry_date.input.send_keys(keys=self.card_date)
        actual_card_expiry_date = self.site.deposit.expiry_date.input.value
        self.assertEqual(actual_card_expiry_date, self.card_date,
                         msg=f'Actual card expiry date "{actual_card_expiry_date}" != Expected "{self.card_date}"')
        self.assertTrue(self.site.deposit.expiry_date.is_valid_with_green_tick(),
                        msg='"Green tick" is not displayed')
        if self.device_type == 'mobile':
            self.site.deposit.next_button.click()
            try:# try and exception blocks added for browser stack run
                self.site.deposit.next_button.click()
            except Exception:
                self._logger.info('next button is not available')
        self.site.deposit.amount.input.value = self.deposit_amount
        actual_amount = self.site.deposit.amount.input.value
        expected_amount = str(self.deposit_amount)
        self.assertEqual(actual_amount, expected_amount,
                         msg=f'Actual amount "{actual_amount}" != Expected "{expected_amount}"')

        self.site.deposit.cvv_2.input.send_keys(keys=tests.settings.master_card_cvv)
        actual_cvv2 = self.site.deposit.cvv_2.input.value
        self.assertEqual(actual_cvv2, tests.settings.master_card_cvv,
                         msg=f'Actual CVV2 "{actual_cvv2}" != Expected "{tests.settings.master_card_cvv}"')
        self.assertTrue(self.site.deposit.cvv_2.is_valid_with_green_tick(),
                        msg='"Green tick" is not displayed')

    def test_011_click_on_deposit_amount_currency_button(self):
        """
        DESCRIPTION: Click on 'DEPOSIT [amount][currency]' button
        DESCRIPTION: where [amount] = deposit amount entered
        DESCRIPTION: [currency] = currency selected during registration.
        EXPECTED: * Message 'Your deposit of [amount][currency] has been successful
        EXPECTED: * TRANSACTION DETAILS
        EXPECTED: * 'OK' button
        """
        self.site.deposit.deposit_button.click()
        try: # try and exception blocks added for browser stack run
            self.site.deposit.deposit_button.click()
        except Exception:
            self._logger.info('Deposit button is not available')
        expected = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.deposit_amount)
        actual = wait_for_result(lambda: self.site.deposit_transaction_details.successful_message,
                                 name='successful message to display',
                                 timeout=20)
        self.assertEqual(actual, expected,
                         msg=f'Actual message "{actual}" != Expected "{expected}"')
        ok_button = self.site.deposit_transaction_details.ok_button.is_displayed()
        self.assertTrue(ok_button, msg='"OK" button is not present')

    def test_012_click_ok_button(self):
        """
        DESCRIPTION: Click 'OK' button
        EXPECTED: Coral Home Page is opened.
        EXPECTED: User is logged in and balance is displayed on header with amount deposited on previous step.
        """
        wait_for_haul(2)
        self.site.deposit_transaction_details.ok_button.click()
        self.site.wait_logged_in(timeout=20)
        self.site.wait_content_state(state_name='Homepage')
        user_balance = self.site.header.user_balance
        self.verify_user_balance(expected_user_balance=user_balance)
