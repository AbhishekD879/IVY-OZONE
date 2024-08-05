import datetime
import pytest
import tests
from faker import Faker
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.gvc_exeption import GVCException
from voltron.environments import constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C16367454_Vanilla_Verify_Decreasing_of_Users_Limits(Common):
    """
    TR_ID: C16367454
    NAME: [Vanilla ] Verify Decreasing of User's Limits
    DESCRIPTION: This test case verifies decreasing of Daily/Weekly/Monthly deposit limits
    PRECONDITIONS: User has deposit limits set up.
    """
    keep_browser_open = True
    limit_message = 'Set your  limit'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register user
        """
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[2:]}'
        self.__class__.first_name = Faker().first_name_female()
        user_info = self.gvc_wallet_user_client.register_new_user(firstname=self.first_name,
                                                                  password=tests.settings.default_password)
        self.__class__.username = user_info.username
        self.__class__.currencycode = user_info.currencycode
        password = user_info.password

        self.__class__.deposit_limits_data = self.gvc_wallet_user_client.get_deposit_limits_data(username=self.username,
                                                                                                 password=password)
        if not self.deposit_limits_data:
            raise GVCException('Deposit limits page is not configured on GVC side')

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in successfully
        """
        self.site.login(username=self.username)

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

    def test_005_decrease_daily_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Decrease **Daily** Deposit Limit and tap 'SAVE' button
        EXPECTED: * **'DAILY DEPOSIT LIMIT: Your limits have been changed..'** success message is shown
        EXPECTED: * Current limit is updated accordingly
        """
        self.__class__.daily_field = self.set_deposit_limits_page.daily_field
        self.assertTrue(self.daily_field.is_displayed(), msg='"Daily" deposit limit textfield is not displayed')
        self.daily_field.input_field.value = '12'
        self.set_deposit_limits_page.save_button.click()
        sleep(5)
        self.__class__.daily_field = self.set_deposit_limits_page.daily_field
        self.assertTrue(self.daily_field.is_displayed(), msg='"Daily" deposit limit textfield is not displayed')

        # decreasing limits
        daily_value = '10'
        self.daily_field.input_field.value = daily_value
        self.set_deposit_limits_page.save_button.click()
        sleep(3)
        actual_popup_text = self.set_deposit_limits_page.success_popup.message.text
        limit_changed_text = self.deposit_limits_data['content']['limitsForm']['messages']['IsLimitChangedDown']
        expected_popup_text = vec.gvc.DAILY_LIMITS_CHANGED_POPUP_TEXT.format(limit_changed_text)
        self.assertEqual(actual_popup_text, expected_popup_text, msg=f'"{actual_popup_text}" successful popup text is '
                                                                     f'not equal to expected "{expected_popup_text}"')

        actual_color = self.set_deposit_limits_page.success_popup.message.background_color_name
        self.assertEqual(actual_color, 'green', msg=f'Instead of green, actual color for '
                                                    f'"Your limits have been changed." popup is: "{actual_color}"')

        daily_current_limit = self.set_deposit_limits_page.daily_field.current_limit.name
        self.assertIn(daily_value, daily_current_limit,
                      msg=f'Daily limit was not changed correctly. Expected: "{daily_value}", '
                          f'but full message is: "{daily_current_limit}"')

    def test_006_decrease_weekly_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Decrease **Weekly** Deposit Limit and tap 'SAVE' button
        EXPECTED: * **'WEEKLY DEPOSIT LIMIT: Your limits have been changed.'** success message is shown
        EXPECTED: * Current limit is updated accordingly
        """
        self.__class__.weekly_field = self.set_deposit_limits_page.weekly_field
        self.assertTrue(self.weekly_field.is_displayed(), msg='"Weekly" deposit limit textfield is not displayed')
        self.weekly_field.input_field.value = '22'
        self.set_deposit_limits_page.save_button.click()
        sleep(5)
        self.__class__.weekly_field = self.set_deposit_limits_page.weekly_field
        self.assertTrue(self.weekly_field.is_displayed(), msg='"Weekly" deposit limit textfield is not displayed')

        # decreasing limits
        weekly_value = '20'
        self.weekly_field.input_field.value = weekly_value
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
        self.assertIn(weekly_value, weekly_current_limit,
                      msg=f'Weekly limit was not changed correctly. Expected: "{weekly_value}", '
                          f'but full message is: "{weekly_current_limit}"')

    def test_007_decrease_monthly_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Decrease **Monthly** Deposit Limit and tap 'SAVE' button
        EXPECTED: * **'MONTHLY DEPOSIT LIMIT: Your limits have been changed.'** success message is shown
        EXPECTED: * Current limit is updated accordingly
        """
        self.__class__.monthly_field = self.set_deposit_limits_page.monthly_field
        self.assertTrue(self.monthly_field.is_displayed(), msg='"Monthly" deposit limit textfield is not displayed')
        self.monthly_field.input_field.value = '32'
        self.set_deposit_limits_page.save_button.click()
        sleep(5)
        self.__class__.monthly_field = self.set_deposit_limits_page.monthly_field
        self.assertTrue(self.monthly_field.is_displayed(), msg='"Monthly" deposit limit textfield is not displayed')

        # decreasing limits
        monthly_value = '30'
        self.monthly_field.input_field.value = monthly_value
        self.set_deposit_limits_page.save_button.click()
        sleep(3)
        actual_popup_text = self.set_deposit_limits_page.success_popup.message.text
        limit_changed_text = self.deposit_limits_data['content']['limitsForm']['messages']['IsLimitChangedDown']
        expected_popup_text = vec.gvc.MONTHLY_LIMITS_CHANGED_POPUP_TEXT.format(limit_changed_text)
        self.assertEqual(actual_popup_text, expected_popup_text, msg=f'"{actual_popup_text}" successful popup text is '
                                                                     f'not equal to expected "{expected_popup_text}"')

        actual_color = self.set_deposit_limits_page.success_popup.message.background_color_name
        self.assertEqual(actual_color, 'green', msg=f'Instead of green, actual color for '
                                                    f'"Your limits have been changed." popup is: "{actual_color}"')

        monthly_current_limit = self.set_deposit_limits_page.monthly_field.current_limit.name
        self.assertIn(monthly_value, monthly_current_limit,
                      msg=f'Monthly limit was not changed correctly. Expected: "{monthly_value}", '
                          f'but full message is: "{monthly_current_limit}"')

    def test_008_decrease_daily_and_monthly_and_monthly_deposit_limit_and_tap_save_button(self):
        """
        DESCRIPTION: Decrease **Daily** and **Monthly** and **Monthly** Deposit Limit and tap 'SAVE' button
        EXPECTED: * **'DAILY DEPOSIT LIMIT,WEEKLY DEPOSIT LIMIT,MONTHLY DEPOSIT LIMIT: Your limits have been changed..'** success message is shown
        EXPECTED: * Current limit is updated accordingly
        """
        self.__class__.daily_field = self.set_deposit_limits_page.daily_field
        self.__class__.weekly_field = self.set_deposit_limits_page.weekly_field
        self.__class__.monthly_field = self.set_deposit_limits_page.monthly_field
        self.__class__.daily_value = '8'
        self.daily_field.input_field.value = self.daily_value

        self.__class__.old_weekly_value = '18'
        self.weekly_field.input_field.value = self.old_weekly_value

        self.__class__.monthly_value = '28'
        self.monthly_field.input_field.value = self.monthly_value

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

        daily_current_limit = self.set_deposit_limits_page.daily_field.current_limit.name
        self.assertIn(self.daily_value, daily_current_limit,
                      msg=f'Daily limit was not changed correctly. Expected: "{self.daily_value}", '
                          f'but full message is: "{daily_current_limit}"')
        weekly_current_limit = self.set_deposit_limits_page.weekly_field.current_limit.name
        self.assertIn(self.old_weekly_value, weekly_current_limit,
                      msg=f'Weekly limit was not changed correctly. Expected: "{self.old_weekly_value}", '
                          f'but full message is: "{weekly_current_limit}"')
        monthly_current_limit = self.set_deposit_limits_page.monthly_field.current_limit.name
        self.assertIn(self.monthly_value, monthly_current_limit,
                      msg=f'Monthly limit was not changed correctly. Expected: "{self.monthly_value}", '
                          f'but full message is: "{monthly_current_limit}"')

    def test_009_open_deposit_limits_and_verify_limits_from_point_6_9_by_doing_a_deposit_that_is_greater_than_dailyweeklymonthly_limits_but_lower_than_previous_limits(
            self):
        """
        DESCRIPTION: Open 'DEPOSIT LIMITS' and verify limits from point 6-9 by doing a deposit that is greater than Daily/Weekly/Monthly limits but lower than previous limits.
        EXPECTED: Error message: **"SELF-SET DEPOSIT LIMIT EXCEEDED You have exceeded the daily deposit limit previously set by you." ** is shown
        """
        if self.device_type == 'mobile':
            self.set_deposit_limits_page.close_button.click()

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
        sleep(3)
        deposit_limit_warning_page = self.site.deposit_limit_warning
        warning_message_title = deposit_limit_warning_page.warning_message_title
        self.assertEqual(warning_message_title, vec.gvc.DEPOSIT_LIMIT_WARNING_MESSAGE_TITLE,
                         msg=f'Deposit limit warning message header is not equal to expected. '
                             f'\nActual: {warning_message_title}",\n'
                             f'Expected: {vec.gvc.DEPOSIT_LIMIT_WARNING_MESSAGE_TITLE}')
        warning_message = deposit_limit_warning_page.warning_message
        expected_warning_message = vec.gvc.DEPOSIT_LIMIT_WARNING_MESSAGE.format(firstname=self.first_name.upper(),
                                                                                currencycode=self.currencycode,
                                                                                value="{0:.2f}".format(
                                                                                    int(self.daily_value)))
        self.assertIn(expected_warning_message, warning_message,
                      msg=f'Deposit limit warning part message \n"{expected_warning_message}"\n '
                          f'is not present in\n"{warning_message}"')
        expected_button_name = vec.gvc.DEPOSIT_NOW_BUTTON_NAME.format(currencycode=self.currencycode,
                                                                      value="{0}".format(int(self.daily_value)))
        deposit_now_button = deposit_limit_warning_page.deposit_now_button
        self.assertTrue(deposit_now_button.is_displayed(), msg=f'"{expected_button_name}" button is not displayed'),
        self.assertEqual(deposit_now_button.name, expected_button_name,
                         msg=f'Button name "{deposit_now_button.name}" is not equal to expected "{expected_button_name}"')
        deposit_limit_warning_page.close_button.click()
