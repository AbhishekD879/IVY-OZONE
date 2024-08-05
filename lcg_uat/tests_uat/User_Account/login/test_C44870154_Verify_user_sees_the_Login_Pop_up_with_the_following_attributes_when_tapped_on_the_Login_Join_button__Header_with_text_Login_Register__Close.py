import datetime
import pytest
import tests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from faker import Faker
from time import time
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870154_Verify_user_sees_the_Login_Pop_up_with_the_following_attributes_when_tapped_on_the_Login_Join_button__Header_with_text_Login_Register__Close_button__Username_text_and_entry_area__Password_entry_and_entry_area_with_Show_text_Remember_M(Common):
    """
    TR_ID: C44870154
    NAME: ""Verify user sees the Login Pop up with the following attributes when tapped on the Login/Join button  - Header with text ""Login/Register""  - Close button - Username text and entry area  - Password entry and entry area with Show text Remember M
    PRECONDITIONS: User not logged in
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.datetime.now()
    shifted_year = str(now.year + 5)
    card_expiry_date = f'{now.month:02d}/{shifted_year[2:]}'
    user = {"social_title": 'Ms.',
            "first_name": Faker().first_name_female(),
            "last_name": Faker().last_name_female(),
            "username": f'{tests.settings.registration_pattern_prefix}{Faker().pyint(max_value=999)}{Faker().pystr(max_chars=5)}'[:15],
            "birth_date": '17-03-1997',
            "post_code": 'PO16 7GZ',
            "country": 'United Kingdom',
            "address_one": '1 Owen Close',
            "city": 'Fareham',
            "mobile": '+447233344457',
            "email": f'test_{time()}@internalgvc.com',
            "password": 'Lshiv@123',
            "currency": 'GBP',
            "monthly_deposit_limit": '50',
            "terms_and_conditions": True,
            }

    def test_001_launch_the_app(self):
        """
        DESCRIPTION: Launch the app
        """
        self.site.wait_content_state('HOMEPAGE')

    def test_002_tap_on_log_in(self):
        """
        DESCRIPTION: Tap on 'Log in'
        EXPECTED: Login overlay is loaded with
        EXPECTED: a)Online / b)Connect card
        EXPECTED: Options under Online
        EXPECTED: 1.Connect card
        EXPECTED: 2.Username
        EXPECTED: 3.Password
        EXPECTED: 4.Remember me check box
        EXPECTED: 5.Forgot Username
        EXPECTED: 6.Forgot Password
        EXPECTED: 7.Login
        EXPECTED: 8.Register
        EXPECTED: Under b)Connect card
        EXPECTED: 1. Connect card number
        EXPECTED: 2. 4 digit pin
        EXPECTED: 3. Remember me
        EXPECTED: 4. Forgot my 4 digit pin
        EXPECTED: 5. Login
        EXPECTED: 6. Register
        EXPECTED: On clicking 'REGISTER' the user is navigated to the registration page (Step 3)
        """
        self.site.header.sign_in.click(),
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='"login dialog" is not present on page')
        self.assertTrue(dialog.connect_card_toggle.is_displayed(),
                        msg='"connect card toggle" is not present in login dialog')
        self.assertTrue(dialog.username_field.is_displayed(),
                        msg='"username field" is not present in login dialog')
        self.assertTrue(dialog.password.is_displayed(),
                        msg='"password field" is not present in login dailog')
        self.assertTrue(dialog.remember_me.is_displayed(),
                        msg='"remember me checkbox" is not present in login dialog')
        self.assertTrue(dialog.forgot_password.is_displayed(),
                        msg='"forgot password link" is not present in login dialog')
        self.assertTrue(dialog.login_button.is_displayed(),
                        msg='"login button" is not present in login dailog')
        self.assertTrue(dialog.create_an_account.is_displayed(),
                        msg='"register button" is not present in login dailog')
        dialog.connect_card_toggle.click()
        self.assertTrue(dialog.connect_card_number_field.is_displayed(),
                        msg='"connect_card_number field" is not present in login dailog')
        self.assertTrue(dialog.connect_card_pin.is_displayed(),
                        msg='"connect_card_pin field" is not present in login dailog')
        self.assertTrue(dialog.remember_me.is_displayed(),
                        msg='"remember me checkbox" is not present in login dailog')
        self.assertTrue(dialog.forgot_four_digit_pin.is_displayed(),
                        msg='"four digit pin link" is not present in login dailog')
        self.assertTrue(dialog.login_button.is_displayed(),
                        msg='"login button" is not present in login dailog')
        dialog.close_dialog()
        self.navigate_to_page('homepage')

    def test_003_click_on_register_from_log_in_page_or_join_now_button_from_the_header(self):
        """
        DESCRIPTION: Click on 'REGISTER' from log in page or 'JOIN NOW' button from the header
        EXPECTED: Registration page is opened
        """
        self.site.header.join_us.click()
        wait_for_result(lambda: self.site.three_steps_registration.is_displayed(),
                        name='Registration Page is not displayed',
                        timeout=15)
        self.__class__.three_step_form = self.site.three_steps_registration
        self.assertTrue(self.three_step_form.form_step1,
                        msg='Page "Registration - Step 1 of 3" is  not shown')

    def test_004_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        EXPECTED: Country of residency
        EXPECTED: Currency
        EXPECTED: Email
        EXPECTED: Create Username
        EXPECTED: Create Password
        """
        self.assertTrue(self.three_step_form.form_step1.currency,
                        msg='"currency dropdown" is not present in registration form')
        self.assertTrue(self.three_step_form.form_step1.country,
                        msg='"country dropdown" is not present in registration form')
        self.assertTrue(self.three_step_form.form_step1.email,
                        msg='"email field" is not present in registration form')
        if tests.settings.backend_env != 'tst2' and self.brand != 'bma':
            self.assertTrue(self.three_step_form.form_step1.username,
                            msg='"username field" is not present in registration form')
        self.assertTrue(self.three_step_form.form_step1.password,
                        msg='"password field" is not present in registration form')
        self.three_step_form.form_step1.enter_values(
            country=self.user['country'],
            email=self.user['email'],
            username=self.user['username'],
            password=self.user['password'],
        )

    def test_005_click_next_step_button(self):
        """
        DESCRIPTION: Click 'Next Step' button
        EXPECTED: Registration Step 2 is opened
        """
        self.three_step_form.submit_step1()
        self.assertTrue(self.three_step_form.form_step2,
                        msg='registration form step 2 is not displayed')

    def test_006_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        EXPECTED: 1. Title - choose any option
        EXPECTED: 2. First name - random name
        EXPECTED: 3. Last name - random name
        EXPECTED: 4. Date of birth (random day/month/year, 18 years plus)
        """
        self.assertTrue(self.three_step_form.form_step2.social_title,
                        msg='"title field" is not present in registration form')
        self.assertTrue(self.three_step_form.form_step2.first_name,
                        msg='"first name field" is not present in registration form')
        self.assertTrue(self.three_step_form.form_step2.last_name,
                        msg='"last name field" is not present in registration form')
        self.assertTrue(self.three_step_form.form_step2.date_of_birth,
                        msg='"date of birth dropdown" is not present in registration form')
        self.three_step_form.form_step2.enter_values(
            social_title=self.user['social_title'],
            first_name=self.user['first_name'],
            last_name=self.user['last_name'],
            birth_date=self.user['birth_date'],
        )

    def test_007_click_next_step_button(self):
        """
        DESCRIPTION: Click 'Next Step' button
        EXPECTED: Registration Step 3 is opened
        """
        self.three_step_form.submit_step2()
        self.assertTrue(self.three_step_form.form_step3,
                        msg='"registration form step 3" is not displayed')

    def test_008_fill_in_the_required_data(self):
        """
        DESCRIPTION: Fill in the required data:
        EXPECTED: 1. UK Postcode (random UK Postcode) - after the UK Post code is added, click on Find button in order to automatically populate the Address fields (PLEASE NOTE THAT VPN CONNECTION SHOULD BE TURNED ON)
        EXPECTED: 2. Mobile number (random number - you can use 0000000000)
        EXPECTED: 3. Select Marketing Preferences
        """
        self.assertTrue(self.three_step_form.form_step3.post_code,
                        msg='"postcode field" is not present in registration form')
        self.assertTrue(self.three_step_form.form_step3.mobile,
                        msg='"mobile field" is not present in registration form')
        self.assertTrue(self.three_step_form.form_step3.all_marketing_options_checkbox,
                        msg='"marketing preferences checkbox" is not present in registration form')
        self.three_step_form.form_step3.enter_values(
            post_code=self.user['post_code'],
            mobile=self.user['mobile'],
            marketing_preferences=self.three_step_form.form_step3.all_marketing_options_checkbox.click())

    def test_009_click_crete_my_account_button(self):
        """
        DESCRIPTION: Click 'Crete my account' button
        EXPECTED: Set your deposit limits page opened
        EXPECTED: 1. Select limits
        EXPECTED: 2. Tick- Fund Protection policy.
        """
        ActionChains(self.device.driver).send_keys(Keys.TAB).perform()
        self.three_step_form.submit_step3()
        wait_for_result(lambda: self.site.set_your_deposit_limits.is_displayed(),
                        timeout=10,
                        name='Confirmation text to disappear')
        self.assertTrue(self.site.set_your_deposit_limits,
                        msg='"deposit limit" dialog is not present on page')

    def test_010_click_submit_button__deposit_page_opened(self):
        """
        DESCRIPTION: Click 'Submit' button > 'Deposit' page opened
        EXPECTED: Tap 'Add Debit/Credit Cards' tab & select payment option page is displayed with following fields:
        EXPECTED: Enter Amount (- / +)
        EXPECTED: Cardholder Name
        EXPECTED: Card Number
        EXPECTED: Expiration Date
        EXPECTED: CVV
        """
        self.site.set_your_deposit_limits.set_limits(deposit_limit=20)
        if self.brand == 'ladbrokes' and tests.settings.backend_env == 'tst2':
            self.site.select_deposit_method.debit_card_button.click()
        else:
            self.site.select_deposit_method.master_card_button.click()
        self.__class__.deposit = self.site.deposit
        self.assertTrue(self.deposit.card_number.is_displayed(), msg='Card number field is not displayed')
        self.assertTrue(self.deposit.expiry_date.is_displayed(), msg='Expiry Date field is not displayed')

    def test_011_clicktap_deposit_button(self):
        """
        DESCRIPTION: Click/Tap 'Deposit' button
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: Amount on message is displayed in decimal format
        EXPECTED: User stays on the 'My Payments' tab for few seconds and then taken to home page
        """
        if tests.settings.backend_env == 'prod':
            self.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=tests.settings.master_card,
                                                  cvv_2=tests.settings.master_card_cvv, expiry_date=self.card_expiry_date)
        else:
            self.site.deposit.add_new_card_and_deposit(amount=self.deposit_amount, card_number=4142731270314439,
                                                       cvv_2=tests.settings.master_card_cvv,
                                                       expiry_date=self.card_expiry_date)
        expected_deposit_message = vec.gvc.DEPOSIT_SUCCESSFUL_MESSAGE.format(self.deposit_amount)
        actual_deposit_message = self.site.deposit_transaction_details.successful_message
        self.assertEqual(actual_deposit_message, expected_deposit_message,
                         msg=f'Actual message: "{actual_deposit_message}" is not same as Expected: "{expected_deposit_message}"')
        wait_for_result(lambda: self.site.deposit_transaction_details.ok_button.is_displayed(),
                        name='OK button is displayed',
                        timeout=10)
        self.site.deposit_transaction_details.ok_button.click()
        self.assertTrue(self.site.wait_content_state('HOMEPAGE', timeout=15), msg='User is not navigated to homepage')
