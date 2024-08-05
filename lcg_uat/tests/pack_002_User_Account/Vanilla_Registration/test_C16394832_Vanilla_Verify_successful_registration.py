from time import time
from faker import Faker
import tests
import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.helpers import string_generator
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.user_journey_promo_1
@pytest.mark.user_journey_promo_2
@pytest.mark.user_account
@pytest.mark.user_password
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.pipelines
@pytest.mark.portal_dependant
@vtest
class Test_C16394832_Vanilla_Verify_successful_registration(BaseUserAccountTest):
    """
    TR_ID: C16394832
    NAME: Register new user
    DESCRIPTION: This test case verifies possibility of new user registration.
    PRECONDITIONS: Make sure you are logged out of the system.
    PRECONDITIONS: This test case should be tested on Desktop, Tablet and Mobile devices.
    PRECONDITIONS: **Choosing the password should include following rules:**
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True

    user = {"social_title": "Mr.",
            "first_name": Faker().first_name_female(),
            "last_name": Faker().last_name_female(),
            "birth_date": "01-06-1977",
            "country": "United Kingdom",
            "post_code": "PO16 7GZ",
            "address_one": "1 Owen Close",
            "city": "Fareham",
            "mobile": "+447537152317",
            "email": f'test{time()}@internalgvc.com',
            "username": f'{tests.settings.registration_pattern_prefix}{string_generator(size=5)}'[:15],
            "password": "Qwerty19",
            "currency": "GBP",
            "deposit_limit": None,
            "terms_and_conditions": True, }

    def test_001_load_vanilla_application(self):
        """
        DESCRIPTION: Load Vanilla application
        """
        self.site.wait_content_state('HomePage')

    def test_002_tap_on_join_button(self):
        """
        DESCRIPTION: Tap on 'Join' button
        EXPECTED: - Page 'Registration - Step 1 of 3' is shown
        """
        self.site.header.join_us.click()
        self.site.wait_content_state_changed(timeout=60)
        wait_for_result(lambda: self.site.three_steps_registration,
                        name='Page "Registration - Step 1 of 3" to be displayed ')
        self.__class__.three_step_form = self.site.three_steps_registration
        self.assertTrue(self.three_step_form.form_step1,
                        msg='Page "Registration - Step 1 of 3" is not shown')

    def test_003_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules
        EXPECTED: - All mandatory fields are filled
        EXPECTED: - None of fields are highlighted in red
        """
        self.three_step_form.form_step1.enter_values(
            country=self.user['country'],
            email=self.user['email'],
            username=self.user['username'],
            password=self.user['password'],
        )
        if self.brand != 'bma' and tests.settings.backend_env != 'tst2':
            self.assertFalse(self.three_step_form.form_step1.username.has_error_message(False),
                             msg='Error message is displayed for username field')
        self.assertFalse(self.three_step_form.form_step1.password.has_error_message(False),
                         msg='Error message is displayed for password field')
        self.assertFalse(self.three_step_form.form_step1.email.has_error_message(False),
                         msg='Error message is displayed for email field')

    def test_004_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Each field is validated and any validation issues are reported.
        EXPECTED: - Page 'Registration - Step 2 of 3' is shown
        """
        self.three_step_form.submit_step1()

    def test_005_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules
        EXPECTED: - All mandatory fields are filled
        EXPECTED: - None of fields are highlighted in red
        """
        self.three_step_form.form_step2.enter_values(
            social_title=self.user['social_title'],
            first_name=self.user['first_name'],
            last_name=self.user['last_name'],
            birth_date=self.user['birth_date'],
        )
        self.assertFalse(self.three_step_form.form_step2.first_name.has_error_message(False),
                         msg='Error message is displayed for error message field')
        self.assertFalse(self.three_step_form.form_step2.last_name.has_error_message(False),
                         msg='Error message is displayed for last name field')
        self.assertFalse(self.three_step_form.form_step2.date_of_birth.day.has_error_message(False),
                         msg='Error message is displayed birth date field')
        self.assertFalse(self.three_step_form.form_step2.date_of_birth.month.has_error_message(False),
                         msg='Error message is displayed birth month field')
        self.assertFalse(self.three_step_form.form_step2.date_of_birth.year.has_error_message(False),
                         msg='Error message is displayed birth year field')

    def test_006_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Each field is validated and any validation issues are reported.
        EXPECTED: - Page 'Registration - Step 3 of 3' is shown
        """
        self.three_step_form.submit_step2()

    def test_007_tap_on_step_one_button_verify_saved_data(self):
        """
        DESCRIPTION: Tap on 'Step 1' button
        EXPECTED: - Page 'Registration - Step 1' is shown
        EXPECTED: - All  previously entered data is saved and shown.
        """
        buttons = self.site.three_steps_registration.registration_steps.items_as_ordered_dict
        first = buttons.get('1')
        first.click()
        country = self.three_step_form.form_step1.country.dropdown.value
        self.assertEqual(country, self.user['country'],
                         msg=f'Actual country field value "{country}" does not match expected {self.user["country"]}')
        currency_name = self.three_step_form.form_step1.currency.dropdown.value
        self.assertEqual(currency_name, self.user["currency"],
                         msg=f'Actual currency selected "{currency_name}" not equal to {self.user["currency"]}')
        email = self.three_step_form.form_step1.email.input.value
        self.assertEqual(email, self.user['email'],
                         msg=f'Actual email field value "{email}" does not match expected {self.user["email"]}')
        if self.brand != 'bma' and tests.settings.backend_env != 'tst2':
            username = self.three_step_form.form_step1.username.input.value
            self.assertEqual(username, self.user["username"],
                             msg=f'Username "{username}" not equal to {self.user["username"]}')
        password = self.three_step_form.form_step1.password.input.value
        self.assertEqual(password, self.user["password"],
                         msg=f'Password "{password}" not equal to {self.user["password"]}')

    def test_008_tap_on_continue_button_verify_saved_data(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Page 'Registration - Step 2' is shown
        EXPECTED: - All previously entered data is saved and shown.
        """
        self.three_step_form.submit_step1()
        first_name = self.three_step_form.form_step2.first_name.input.value
        self.assertEqual(first_name, self.user['first_name'],
                         msg=f'Actual first name field value "{first_name}" does not match expected {self.user["first_name"]}')
        last_name = self.three_step_form.form_step2.last_name.input.value
        self.assertEqual(last_name, self.user['last_name'],
                         msg=f'Actual last name field value "{last_name}" does not match expected {self.user["last_name"]}')
        date_of_birth = self.three_step_form.form_step2.date_of_birth.value
        self.assertEqual(date_of_birth, self.user['birth_date'],
                         msg=f'Actual date of birth field value "{date_of_birth}" does not match expected {self.user["birth_date"]}')

    def test_009_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Each field is validated and any validation issues are reported.
        EXPECTED: - Page 'Registration - Step 3 of 3' is shown
        """
        self.three_step_form.submit_step2()

    def test_010_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules
        EXPECTED: - All mandatory fields are filled.
        EXPECTED: - None of fields are highlighted in red
        """
        self.three_step_form.form_step3.enter_values()
        self.assertFalse(self.three_step_form.form_step3.city.has_error_message(False),
                         msg='Error message is displayed for city field')
        self.assertFalse(self.three_step_form.form_step3.post_code.has_error_message(False),
                         msg='Error message is displayed for post code field')
        self.assertFalse(self.three_step_form.form_step3.mobile.mobile_number.has_error_message(False),
                         msg='Error message is displayed for mobile field')
        self.three_step_form.submit_step3()

    def test_011_set_deposit_limit(self):
        """
        DESCRIPTION: Select suitable Limits field
        EXPECTED: - All mandatory fields are filled.
        EXPECTED: - None of fields are highlighted in red
        """
        self.site.set_your_deposit_limits.set_limits()

    def test_012_tap_on_close(self):
        """
        DESCRIPTION: Tap on close icon
        EXPECTED: - Home page is shown
        """
        self.site.wait_content_state_changed(timeout=20)
        self.site.select_deposit_method.close_button.click()
        self.site.wait_content_state('HomePage')
