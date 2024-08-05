import tests
import datetime
import pytest
import voltron.environments.constants as vec
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.utils.exceptions.gvc_exeption import GVCException


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C16367451_Vanilla_Set_deposit_limits_for_the_first_time(Common):
    """
    TR_ID: C16367451
    NAME: [Vanilla] Set deposit limits for the first time
    DESCRIPTION: This test case verifies set up of Daily/Weekly/Monthly deposit limits for the first time
    PRECONDITIONS: User has never set up deposit limits.
    """
    keep_browser_open = True
    limit_message = 'Set your  limit'
    first_name = []
    username = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register user
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[2:]}'
        for i in range(0, 2):
            first_name = Faker().first_name_female()
            self.first_name.append(first_name)
            user_info = self.gvc_wallet_user_client.register_new_user(firstname=first_name,
                                                                      password=tests.settings.default_password)
            username = user_info.username
            self.username.append(username)
            self.__class__.currencycode = user_info.currencycode
            password = user_info.password

            self.__class__.deposit_limits_data = self.gvc_wallet_user_client.get_deposit_limits_data(username=username,
                                                                                                     password=password)
        if not self.deposit_limits_data:
            raise GVCException('Deposit limits page is not configured on GVC side')

    def test_001_log_in_as_a_user_without_deposit_limits(self):
        """
        DESCRIPTION: Log in as a user without deposit limits
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=self.username[0])

    def test_002_tap_right_menu_icon___my_account_menu_item(self):
        """
        DESCRIPTION: Tap Right menu icon -> 'My Account' menu item
        EXPECTED: Tap Right menu icon -> 'My Account' menu item
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='Right menu is not displayed')

    def test_003_tap_gambling_controls(self):
        """
        DESCRIPTION: Tap 'GAMBLING CONTROLS'
        EXPECTED: Tap 'GAMBLING CONTROLS'
        """
        gambling_controls_title = self.site.window_client_config.gambling_controls_title
        self.site.right_menu.click_item(item_name=gambling_controls_title, timeout=10)
        self.__class__.gambling_controls_page = self.site.gambling_controls
        self.assertTrue(self.gambling_controls_page.is_displayed(),
                        msg=f'"{gambling_controls_title}" page is not displayed')

    def test_004_check_deposit_limits_image_and_tap_choose__button(self):
        """
        DESCRIPTION: Check 'Deposit Limits' image and tap 'CHOOSE ' button
        EXPECTED: 'DEPOSIT LIMITS' page is open and the is no set up for Daily/Weekly/Monthly limits
        """
        expected_option_name = self.site.window_client_config.mobile_portal_spending_controls
        actual_option_name = self.gambling_controls_page.selected_option
        self.assertEqual(expected_option_name, actual_option_name,
                         msg=f'"{expected_option_name}" option, on "Gambling Controls" page is not selected by default.'
                             f'"{actual_option_name}" is selected instead.')

        self.gambling_controls_page.choose_button.click()
        self.__class__.set_deposit_limits_page = self.site.set_deposit_limits
        self.assertTrue(self.set_deposit_limits_page.is_displayed(), msg='"Set deposit limits" page is not displayed')
        self.site.wait_splash_to_hide(timeout=10)

    def test_005_set_daily_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Set **Daily** limits and tap 'SAVE' button
        EXPECTED: There is a message that says that limits has been set up successfully: 'DAILY DEPOSIT LIMIT: Your limits have been changed.'
        """
        daily_field = self.set_deposit_limits_page.daily_field
        self.assertTrue(daily_field.is_displayed(), msg='"Daily" deposit limit textfield is not displayed')
        self.__class__.daily_value = '10'
        daily_field.input_field.value = self.daily_value
        self.set_deposit_limits_page.save_button.click()
        actual_popup_text = self.set_deposit_limits_page.success_popup.message.text
        limit_changed_text = self.deposit_limits_data['content']['limitsForm']['messages']['IsLimitChangedDown']
        expected_popup_text = vec.gvc.DAILY_LIMITS_CHANGED_POPUP_TEXT.format(limit_changed_text)
        self.assertEqual(actual_popup_text, expected_popup_text, msg=f'"{actual_popup_text}" successful popup text is '
                                                                     f'not equal to expected "{expected_popup_text}"')

        actual_color = self.set_deposit_limits_page.success_popup.message.background_color_name
        self.assertEqual(actual_color, 'green', msg=f'Instead of green, actual color for '
                                                    f'"Your limits have been changed." popup is: "{actual_color}"')

        daily_current_limit = self.set_deposit_limits_page.daily_field.current_limit.name
        self.assertIn(self.daily_value, daily_current_limit,
                      msg=f'Daily limit was not changed correctly. Expected: "{self.daily_value}", '
                          f'but full message is: "{daily_current_limit}"')

    def test_006_set_weekly_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Set **Weekly** limits and tap 'SAVE' button
        EXPECTED: There is a message that says that limits has been set up successfully: 'WEEKLY DEPOSIT LIMIT: Your limits have been changed.'
        """
        weekly_field = self.set_deposit_limits_page.weekly_field
        self.assertTrue(weekly_field.is_displayed(), msg='"Weekly" deposit limit textfield is not displayed')
        self.__class__.weekly_value = '20'
        weekly_field.input_field.value = self.weekly_value
        self.set_deposit_limits_page.save_button.click()
        sleep(5)
        actual_popup_text = self.set_deposit_limits_page.success_popup.message.text
        limit_changed_text = self.deposit_limits_data['content']['limitsForm']['messages']['IsLimitChangedDown']
        expected_popup_text = vec.gvc.WEEKLY_LIMITS_CHANGED_POPUP_TEXT.format(limit_changed_text)
        self.assertEqual(actual_popup_text, expected_popup_text, msg=f'"{actual_popup_text}" successful popup text is '
                                                                     f'not equal to expected "{expected_popup_text}"')

        actual_color = self.set_deposit_limits_page.success_popup.message.background_color_name
        self.assertEqual(actual_color, 'green', msg=f'Instead of green, actual color for '
                                                    f'"Your limits have been changed." popup is: "{actual_color}"')
        weekly_current_limit = self.set_deposit_limits_page.weekly_field.current_limit.name
        self.assertIn(self.weekly_value, weekly_current_limit,
                      msg=f'Weekly limit was not changed correctly. Expected: "{self.weekly_value}", '
                          f'but full message is: "{weekly_current_limit}"')

    def test_007_set_monthly_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Set **Monthly** limits and tap 'SAVE' button
        EXPECTED: There is a message that says that limits has been set up successfully: 'MONTHLY DEPOSIT LIMIT: Your limits have been changed.'
        """
        monthly_field = self.set_deposit_limits_page.monthly_field
        self.assertTrue(monthly_field.is_displayed(), msg='"Monthly" deposit limit textfield is not displayed')
        self.__class__.monthly_value = '30'
        monthly_field.input_field.value = self.monthly_value
        self.set_deposit_limits_page.save_button.click()
        sleep(5)
        actual_popup_text = self.set_deposit_limits_page.success_popup.message.text
        limit_changed_text = self.deposit_limits_data['content']['limitsForm']['messages']['IsLimitChangedDown']
        expected_popup_text = vec.gvc.MONTHLY_LIMITS_CHANGED_POPUP_TEXT.format(limit_changed_text)
        self.assertEqual(actual_popup_text, expected_popup_text, msg=f'"{actual_popup_text}" successful popup text is '
                                                                     f'not equal to expected "{expected_popup_text}"')

        actual_color = self.set_deposit_limits_page.success_popup.message.background_color_name
        self.assertEqual(actual_color, 'green', msg=f'Instead of green, actual color for '
                                                    f'"Your limits have been changed." popup is: "{actual_color}"')
        monthly_current_limit = self.set_deposit_limits_page.monthly_field.current_limit.name
        self.assertIn(self.monthly_value, monthly_current_limit,
                      msg=f'Monthly limit was not changed correctly. Expected: "{self.monthly_value}", '
                          f'but full message is: "{monthly_current_limit}"')

    def test_008_go_back_to_the_main_page_of_application_and_do_deposit_that_is_greater_than_dailyweeklymonthly_limit_that_has_been_set_up_in_steps_6_7(self, firstname=None):
        """
        DESCRIPTION: Go back to the main page of application and do deposit that is greater than Daily/Weekly/Monthly limit that has been set up in Steps 6-7
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown.
        """
        if firstname is None:
            firstname = self.first_name[0]
        self.navigate_to_page(name='/')
        self.site.wait_content_state('HomePage')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='Failed to open Right Menu')
        self.site.right_menu.click_item(item_name=self.site.window_client_config.cashier_menu_title)

        self.site.right_menu.click_item(item_name=self.site.window_client_config.deposit_menu_title)
        self.assertTrue(self.site.select_deposit_method.is_displayed(scroll_to=False),
                        msg='"Select a deposit method" page is not displayed')
        select_deposit_method = self.site.select_deposit_method
        available_deposit_options = select_deposit_method.items_as_ordered_dict
        self.assertTrue(available_deposit_options, msg='No deposit options available')

        deposit_option_name = 'visa'
        deposit_option = available_deposit_options.get(deposit_option_name)
        self.assertTrue(deposit_option, msg=f'Deposit option for "{deposit_option_name}" is absent')
        self.assertTrue(deposit_option.is_displayed(),
                        msg=f'"{deposit_option_name}" payment method is not displayed')
        deposit_option.click()
        self.assertTrue(self.site.deposit.is_displayed(),
                        msg='"Deposit page" is not displayed')

        self.site.deposit.add_new_card_and_deposit(amount='11',
                                                   cvv_2=tests.settings.visa_card_cvv,
                                                   card_number=tests.settings.visa_card,
                                                   expiry_date=self.card_date)
        sleep(5)
        deposit_limit_warning_page = self.site.deposit_limit_warning
        warning_message_title = deposit_limit_warning_page.warning_message_title
        self.assertEqual(warning_message_title, vec.gvc.DEPOSIT_LIMIT_WARNING_MESSAGE_TITLE,
                         msg=f'Deposit limit warning message header is not equal to expected. '
                             f'\nActual: {warning_message_title}",\n'
                             f'Expected: {vec.gvc.DEPOSIT_LIMIT_WARNING_MESSAGE_TITLE}')
        warning_message = deposit_limit_warning_page.warning_message
        expected_warning_message = vec.gvc.DEPOSIT_LIMIT_WARNING_MESSAGE.format(firstname=firstname.upper(),
                                                                                currencycode=self.currencycode,
                                                                                value="{0:.2f}".format(int(self.daily_value)))
        self.assertIn(expected_warning_message, warning_message,
                      msg=f'Deposit limit warning part message \n"{expected_warning_message}"\n '
                          f'is not present in\n"{warning_message}"')
        expected_button_name = vec.gvc.DEPOSIT_NOW_BUTTON_NAME.format(currencycode=self.currencycode,
                                                                      value="{0}".format(int(self.daily_value)))
        deposit_now_button = deposit_limit_warning_page.deposit_now_button
        self.assertTrue(deposit_now_button.is_displayed(), msg=f'"{expected_button_name}" button is not displayed'),
        self.assertEqual(deposit_now_button.name, expected_button_name,
                         msg=f'Button name "{deposit_now_button.name}" is not equal to expected "{expected_button_name}"')

    def test_009_log_out_and_log_in_with_the_another_user_that_has_no_limits_set_yet(self):
        """
        DESCRIPTION: Log out and log in with the another user that has no limits set yet.
        EXPECTED: User is logged in successfully.
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('HomePage')
        self.site.logout()
        self.site.login(username=self.username[1])

    def test_010_repeat_step_from_2_5_and_set_dailyweeklymonthly_limits_and_tap_save_button(self):
        """
        DESCRIPTION: Repeat step from 2-5 and set **Daily/Weekly/Monthly** limits and tap 'SAVE' button
        EXPECTED: There is a message that says that limits has been set up successfully: 'DAILY DEPOSIT LIMIT,WEEKLY DEPOSIT LIMIT,MONTHLY DEPOSIT LIMIT: Your limits have been changed.'
        """
        self.test_002_tap_right_menu_icon___my_account_menu_item()
        self.test_003_tap_gambling_controls()
        self.test_004_check_deposit_limits_image_and_tap_choose__button()
        daily_field = self.set_deposit_limits_page.daily_field
        self.assertTrue(daily_field.is_displayed(), msg='"Daily" deposit limit textfield is not displayed')
        daily_field.input_field.value = self.daily_value
        weekly_field = self.set_deposit_limits_page.weekly_field
        self.assertTrue(weekly_field.is_displayed(), msg='"Weekly" deposit limit textfield is not displayed')
        weekly_field.input_field.value = self.weekly_value
        monthly_field = self.set_deposit_limits_page.monthly_field
        self.assertTrue(monthly_field.is_displayed(), msg='"Monthly" deposit limit textfield is not displayed')
        monthly_field.input_field.value = self.monthly_value
        self.set_deposit_limits_page.save_button.click()
        sleep(5)
        actual_popup_text = self.set_deposit_limits_page.success_popup.message.text
        limit_changed_text = self.deposit_limits_data['content']['limitsForm']['messages']['IsLimitChangedDown']
        expected_popup_text = vec.gvc.LIMITS_CHANGED_POPUP_TEXT.format(limit_changed_text)
        self.assertEqual(actual_popup_text, expected_popup_text, msg=f'"{actual_popup_text}" successful popup text is '
                                                                     f'not equal to expected "{expected_popup_text}"')

        actual_color = self.set_deposit_limits_page.success_popup.message.background_color_name
        self.assertEqual(actual_color, 'green', msg=f'Instead of green, actual color for '
                                                    f'"Your limits have been changed." popup is: "{actual_color}"')

    def test_011_go_back_to_the_main_page_of_application_and_do_deposit_that_is_greater_than_dailyweeklymonthly_limit_that_has_been_set_up_in_step_11(
            self):
        """
        DESCRIPTION: Go back to the main page of application and do deposit that is greater than Daily/Weekly/Monthly limit that has been set up in Step 11
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown.
        """
        self.test_008_go_back_to_the_main_page_of_application_and_do_deposit_that_is_greater_than_dailyweeklymonthly_limit_that_has_been_set_up_in_steps_6_7(firstname=self.first_name[1])
