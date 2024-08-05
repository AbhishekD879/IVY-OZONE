import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from time import time
from faker import Faker
from voltron.utils.waiters import wait_for_result
from random import randint


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C36533576_Users_Marketing_Preferences(Common):
    """
    TR_ID: C36533576
    NAME: User's Marketing Preferences
    DESCRIPTION: Verify that the customer can set Marketing Preferences through New Registration journey and see them in Settings afterwards
    """
    keep_browser_open = True
    user = {'social_title': 'Mr.',
            'first_name': Faker().first_name_female(),
            'last_name': Faker().last_name_female(),
            'birth_date': f'{randint(1, 28)}-{randint(1, 12)}-{randint(1950, 2000)}',
            'country': 'United Kingdom',
            'post_code': 'PO16 7GZ',
            'address_one': '1 Owen Close',
            'city': 'Fareham',
            'mobile': '+447537152317',
            'email': f'test+{time()}@internalgvc.com',
            'username': '',
            'password': '',
            'currency': 'GBP',
            'deposit_limit': None,
            'terms_and_conditions': True, }

    def test_001_click_on_join_button(self):
        """
        DESCRIPTION: Click on Join button
        EXPECTED: Registration Page 1 is loaded
        """
        self.__class__.username = self.generate_user()
        self.__class__.password = tests.settings.default_password
        self.__class__.user['username'] = self.username
        self.__class__.user['password'] = self.password

        self.site.header.join_us.click()
        if self.device_type == 'mobile' and self.brand == 'ladbrokes':
            self.site.login_dialog.create_an_account.click()
        self.__class__.three_step_form = self.site.three_steps_registration
        self.assertTrue(self.three_step_form.form_step1,
                        msg='Page "Registration - Step 1 of 3" is  not shown')

    def test_002_fill_in_the_required_data_and_click_on_continue_button(self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Country of residence
        DESCRIPTION: 2. Currency type for the user
        DESCRIPTION: 3. Email address
        DESCRIPTION: 4. Username
        DESCRIPTION: 5. Password
        DESCRIPTION: 9. Click on "Continue" button
        EXPECTED: Registration Page 2 is opened
        """
        self.three_step_form.form_step1.enter_values(
            country=self.user['country'],
            email=self.user['email'],
            username=self.user['username'],
            password=self.user['password'],
        )

        self.three_step_form.submit_step1()
        self.assertTrue(self.three_step_form.form_step2,
                        msg='Page "Registration - Step 2 of 3" is  not shown')

    def test_003_fill_in_the_required_data1_choose_between_mr_and_ms2_first_name3_last_name4_date_of_birth5_click_on_continue_button(
            self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Choose between Mr. and Ms.
        DESCRIPTION: 2. First name
        DESCRIPTION: 3. Last name
        DESCRIPTION: 4. Date of birth
        DESCRIPTION: 5. Click on 'Continue' button
        EXPECTED: Registration Page 3 is opened
        """
        self.three_step_form.form_step2.enter_values(
            social_title=self.user['social_title'],
            first_name=self.user['first_name'],
            last_name=self.user['last_name'],
            birth_date=self.user['birth_date'],
        )

        self.three_step_form.submit_step2()
        self.assertTrue(self.three_step_form.form_step3,
                        msg='Page "Registration - Step 3 of 3" is  not shown')

    def test_004_fill_in_the_required_data1_postcode_eg_123452_mobile_number3__all_the_checkboxes_with_marketing_preferences_indexphpattachmentsget17649989click_on_create_my_account_button(
            self):
        """
        DESCRIPTION: Fill in the required data:
        DESCRIPTION: 1. Postcode (e.g. 12345)
        DESCRIPTION: 2. Mobile number
        DESCRIPTION: 3. ** All the checkboxes with Marketing Preferences **
        DESCRIPTION: ![](index.php?/attachments/get/17649989)
        DESCRIPTION: Click on 'Create my account' button
        EXPECTED: 'Set your deposit limits' page is opened
        """
        self.three_step_form.form_step3.enter_values(
            postcode=self.user['post_code'],
            mobile=self.user['mobile'],
        )

        self.three_step_form.form_step3.all_marketing_options_checkbox.click()
        self.three_step_form.submit_step3()
        self.assertTrue(self.site.set_your_deposit_limits.is_displayed(),
                        msg='Set your deposit limits page is not opened.')

    def test_005__choose_no_limit_option_for_the_user_put_a_tick_in_fund_protection_accepting_checkbox_press_on_submit_button(
            self):
        """
        DESCRIPTION: * Choose 'No limit option for the user'
        DESCRIPTION: * Put a tick in Fund Protection accepting checkbox
        DESCRIPTION: * Press on 'Submit' button
        EXPECTED: * 'You are registered!' green panel is displayed on Deposit page
        EXPECTED: * The customer is able to choose between available deposit methods
        """
        self.site.set_your_deposit_limits.set_limits()
        expected_registration_message = vec.gvc.YOU_ARE_REGISTERED_MESSAGE
        self.__class__.deposit_methods = self.site.select_deposit_method
        actual_registration_message = self.deposit_methods.successful_message
        self.assertIn(expected_registration_message, actual_registration_message,
                      msg=f'Registration success message does not contain "{expected_registration_message}" '
                          f'and is "{actual_registration_message}" instead.')

        self.assertTrue(self.deposit_methods.items_as_ordered_dict,
                        msg='Deposit payment methods are not displayed.')

    def test_006_close_the_deposit_dialogue_with_a_x_button(self):
        """
        DESCRIPTION: Close the Deposit dialogue with a 'X' button
        EXPECTED: User is redirected to the Homepage
        """
        self.deposit_methods.close_button.click()
        self.site.wait_content_state('HomePage')
        self.site.close_all_dialogs(async_close=False)

    def test_007_open_my_account_menu__settings__marketing_preferences(self):
        """
        DESCRIPTION: Open My Account menu > Settings > Marketing Preferences
        EXPECTED: * 'Communication preferences' page is opened
        EXPECTED: * All the checkboxes chosen in step 4 are still ticked
        EXPECTED: ![](index.php?/attachments/get/17649984)
        """
        self.site.header.user_panel.my_account_button.click()

        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        settings = self.site.window_client_config.settings_menu_title

        self.assertIn(settings, menu_items.keys(),
                      msg=f'"{settings}" not present in the Right column')

        self.site.right_menu.click_item(item_name=settings)
        result = wait_for_result(lambda: self.site.right_menu.header.is_displayed() and
                                 self.site.right_menu.header.title == settings,
                                 name='Wait for header title to change',
                                 timeout=3)
        self.assertTrue(result, msg=f'Header title does not change. Actual "{self.site.right_menu.header.title}", '
                        f'expected "{settings}"')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        marketing_preferences_menu_item = self.site.window_client_config.marketing_preferences_menu_title
        self.assertIn(marketing_preferences_menu_item, menu_items.keys(),
                      msg=f'"{marketing_preferences_menu_item}" not present in the Right column')
        self.site.right_menu.click_item(item_name=marketing_preferences_menu_item)
        self.site.wait_content_state_changed()
        if self.device_type == 'desktop':
            actual_title = self.site.marketing_preferences.title
            marketing_preferences_settings_title = vec.GVC.MARKETING_PREFERENCES_DESKTOP
        else:
            actual_title = self.site.marketing_preferences.header.title.name
            marketing_preferences_settings_title = vec.GVC.MARKETING_PREFERENCES_MOBILE
        self.assertEqual(actual_title, marketing_preferences_settings_title,
                         msg='Communication Preferences page is not open. '
                             f'Page name is "{actual_title}" instead of "{marketing_preferences_settings_title}"')

        communication_checkboxes = self.site.marketing_preferences.items_as_ordered_dict
        self.assertTrue(communication_checkboxes, msg='Communication Preferences checkboxes not found.')
        for name, checkbox in communication_checkboxes.items():
            self.assertTrue(checkbox.is_selected(),
                            msg=f'Communication checkbox "{name}" is not selected.')
