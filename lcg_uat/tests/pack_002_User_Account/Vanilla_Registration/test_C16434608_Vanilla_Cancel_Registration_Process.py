import tests
import pytest
from time import time, sleep
from faker import Faker
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import string_generator
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.reg167_fix
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C16434608_Vanilla_Cancel_Registration_Process(BaseUserAccountTest):
    """
    TR_ID: C16434608
    NAME: [Vanilla] Cancel Registration Process
    DESCRIPTION: This test case verifies canceling of registration process
    PRECONDITIONS: User is logged out.
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

    def test_002_click_on_join_button(self):
        """
        DESCRIPTION: Click on 'Join' button
        EXPECTED: Registration page is opened
        """
        self.site.header.join_us.click()
        sleep(2)
        self.site.wait_content_state_changed()
        self.__class__.three_step_form = wait_for_result(lambda:self.site.three_steps_registration,timeout=10, bypass_exceptions= VoltronException)
        self.assertTrue(self.three_step_form.form_step1,
                        msg='Page "Registration - Step 1 of 3" is not shown')

    def test_003_enter_correct_data_to_all_required_fields_due_to_validation_rules_for_3_registration_pages(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules for 3 registration pages
        EXPECTED: All mandatory fields are filled
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
        self.three_step_form.submit_step1()
        self.three_step_form.form_step2.enter_values(
            social_title=self.user['social_title'],
            first_name=self.user['first_name'],
            last_name=self.user['last_name'],
            birth_date=self.user['birth_date'],
        )
        self.assertFalse(self.three_step_form.form_step2.first_name.has_error_message(False),
                         msg='Error message is displayed for first name field')
        self.assertFalse(self.three_step_form.form_step2.last_name.has_error_message(False),
                         msg='Error message is displayed for last name field')
        self.assertFalse(self.three_step_form.form_step2.date_of_birth.day.has_error_message(False),
                         msg='Error message is displayed birth date field')
        self.assertFalse(self.three_step_form.form_step2.date_of_birth.month.has_error_message(False),
                         msg='Error message is displayed birth month field')
        self.assertFalse(self.three_step_form.form_step2.date_of_birth.year.has_error_message(False),
                         msg='Error message is displayed birth year field')
        self.three_step_form.submit_step2()
        self.three_step_form.form_step3.enter_values()
        self.assertFalse(self.three_step_form.form_step3.city.has_error_message(False),
                         msg='Error message is displayed for city field')
        self.assertFalse(self.three_step_form.form_step3.post_code.has_error_message(False),
                         msg='Error message is displayed for post code field')
        self.assertFalse(self.three_step_form.form_step3.mobile.mobile_number.has_error_message(False),
                         msg='Error message is displayed for mobile field')

    def test_004_clicktap_on_x_button_at_the_top_right_corner(self):
        """
        DESCRIPTION: Click/Tap on 'X' button at the top right corner
        EXPECTED: - Registration process is canceled
        EXPECTED: - Homepage is shown
        """
        self.site.three_steps_registration.header.close_button.click()
        self.site.wait_content_state('HomePage')
