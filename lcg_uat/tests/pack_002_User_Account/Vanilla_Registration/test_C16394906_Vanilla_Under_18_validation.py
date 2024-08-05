import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.helpers import string_generator
from time import time
from faker import Faker
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C16394906_Vanilla_Under_18_validation(BaseUserAccountTest):
    """
    TR_ID: C16394906
    NAME: [Vanilla] Under 18 validation
    DESCRIPTION: This test case verifies whether it is possible to register a user who is not 18 years old yet
    PRECONDITIONS: User is logged out.
    PRECONDITIONS: Choosing the password should include following rules:
    PRECONDITIONS: - A letter
    PRECONDITIONS: - A number
    PRECONDITIONS: - 6 to 20 characters
    PRECONDITIONS: - Must not contain parts of your name or e-mail
    PRECONDITIONS: - Must not contain any of these special characters (‘ “ < > & % )
    """
    keep_browser_open = True
    user = {"social_title": "Mr.",
            "first_name": Faker().first_name_female(),
            "last_name": Faker().last_name_female(),
            "birth_date": "01-06-1977",
            "country": "United Kingdom",
            "email": f'test+{time()}@internalgvc.com',
            "username": f'{tests.settings.registration_pattern_prefix}{string_generator(size=5)}'[:15],
            "password": "Qwerty19",
            "currency": "GBP"}

    def test_000_load_vanilla_application(self):
        """
        DESCRIPTION: Load Vanilla application
        EXPECTED:
        """
        self.site.wait_content_state('HomePage')

    def test_001_tap_on_join_button(self):
        """
        DESCRIPTION: Tap on 'Join' button
        EXPECTED: Page 'Registration - Step 1 of 3' is shown
        """
        self.site.header.join_us.click()

        if self.brand == 'ladbrokes' and self.device_type != 'desktop':
            self.site.login_dialog.create_an_account.click()
        self.site.wait_content_state_changed()
        self.__class__.three_step_form = self.site.three_steps_registration
        self.assertTrue(self.three_step_form.form_step1, msg='Page "Registration - Step 1 of 3" is not shown')

    def test_002_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
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
        self.assertFalse(self.three_step_form.form_step1.country.has_error_message(False),
                         msg='Error message is displayed for country field')
        self.assertFalse(self.three_step_form.form_step1.currency.has_error_message(False),
                         msg='Error message is displayed for currency field')

    def test_003_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: - Each field is validated and any validation issues are reported
        EXPECTED: - Page 'Registration - Step 2 of 3' is shown
        """
        self.three_step_form.submit_step1()

    def test_004_dont_select_any_information_in_the_date_of_birth_field(self):
        """
        DESCRIPTION: Don't select any information in the 'Date of Birth' field
        EXPECTED:
        """
        self.__class__.step2 = self.three_step_form.form_step2
        self.step2.social_title.value = self.user['social_title']
        self.step2.first_name.input.value = self.user['first_name']
        self.step2.last_name.input.value = self.user['last_name']

        self.three_step_form.submit_step2()
        actual_error_message = self.step2.date_of_birth.year.error_message
        self.assertEqual(actual_error_message, vec.bma.VALIDATOR_TOOLTIPS_DATE_FORMAT_NO_ENTRY,
                         msg=f'Expected Error message is "{vec.bma.VALIDATOR_TOOLTIPS_DATE_FORMAT_NO_ENTRY}" but actual '
                             f'message on UI is shown as "{actual_error_message}')

    def test_005_fill_in_the_rest_fields_of_the_page_and_tap_on_continue_button(self):
        """
        DESCRIPTION: Fill in the rest fields of the page and tap on 'Continue' button
        EXPECTED: - Warning message appears *'Please provide your date of birth'*
        EXPECTED: - It is impossible to navigate to Next Page of Registration or complete registration
        """
        # covered in above step

    def test_006_enter_invalid_date_of_birth_and_repeat_step_6eg_default_value_daymonthyear_should_be_left_for_one_of_drop_down(self):
        """
        DESCRIPTION: Enter invalid 'Date of Birth' and repeat step 6
        DESCRIPTION: (e.g.: default value 'Day'/'Month'/'Year' should be left for one of drop down)
        EXPECTED: - Warning message appears *'Please provide your date of birth'*
        EXPECTED: - It is impossible to navigate to Next Page of Registration or complete registration
        """
        self.step2.date_of_birth.month.input.value = '10'
        self.step2.date_of_birth.year.input.value = '1970'

        actual_error_message = self.step2.date_of_birth.day.error_message
        self.assertEqual(actual_error_message, vec.bma.VALIDATOR_TOOLTIPS_DAY_FORMAT_NO_ENTRY,
                         msg=f'Expected Error message is "{vec.bma.VALIDATOR_TOOLTIPS_DAY_FORMAT_NO_ENTRY}" but actual '
                             f'message on UI is shown as "{actual_error_message}')

    def test_007_enter_date_of_birth_which_does_not_satisfy_criteria_of_18_years_old_and_repeat_step_6(self):
        """
        DESCRIPTION: Enter 'Date of Birth' which does NOT satisfy criteria of 18 years old and repeat step 6
        EXPECTED: - Warning message appears *'You must be over 18 to create an account'*
        EXPECTED: - It is impossible to navigate to Next Page of Registration or complete registration
        """
        self.step2.date_of_birth.value = (datetime.now() - relativedelta(years=10)).strftime('%d-%m-%Y')
        self.three_step_form.submit_step2()
        actual_error_message = self.step2.date_of_birth.year.error_message
        self.assertEqual(actual_error_message, vec.bma.VALIDATOR_TOOLTIPS_ADULT_AGE,
                         msg=f'Expected Error message is "{vec.bma.VALIDATOR_TOOLTIPS_ADULT_AGE}" but actual '
                             f'message on UI is shown as "{actual_error_message}')

    def test_008_enter_such_date_of_birth_as_if_a_user_has_hisher_birthday_tomorrow_and_repeat_step_6(self):
        """
        DESCRIPTION: Enter such 'Date of Birth' as if a user has his/her birthday tomorrow and repeat step 6
        EXPECTED: - Warning message appears *'You must be over 18 to create an account'*
        EXPECTED: - It is impossible to navigate to Next Page of Registration or complete registration
        """
        tomorrow_dob = (datetime.now() + timedelta(1) - relativedelta(years=18)).strftime('%d-%m-%Y')
        self.step2.date_of_birth.value = tomorrow_dob
        self.three_step_form.submit_step2()
        actual_error_message = self.step2.date_of_birth.year.error_message
        self.assertEqual(actual_error_message, vec.bma.VALIDATOR_TOOLTIPS_ADULT_AGE,
                         msg=f'Expected Error message is "{vec.bma.VALIDATOR_TOOLTIPS_ADULT_AGE}" but actual '
                             f'message on UI is shown as "{actual_error_message}"')

    def test_009_enter_18plus_date_of_birth_and_repeat_step_6(self):
        """
        DESCRIPTION: Enter 18+ 'Date of Birth' and repeat step 6
        EXPECTED: User is navigated to the Page 3 successfully
        """
        self.step2.date_of_birth.value = self.user['birth_date']
        self.three_step_form.submit_step2()
        self.assertTrue(self.three_step_form.form_step3,
                        msg='Page "Registration - Step 3 of 3" is  not shown')
