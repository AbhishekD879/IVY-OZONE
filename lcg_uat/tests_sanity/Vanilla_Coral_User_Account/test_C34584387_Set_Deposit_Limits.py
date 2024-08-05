import tests
import datetime
import pytest
import voltron.environments.constants as vec

from time import sleep
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.gvc_exeption import GVCException
from voltron.utils.helpers import cleanhtml
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1782')
# @pytest.mark.sanity
@vtest
class Test_C34584387_Set_Deposit_Limits(Common):
    """
    TR_ID: C34584387
    NAME: Set Deposit Limits
    DESCRIPTION: Verify that the customer can successfully set "Deposit limits"
    PRECONDITIONS: - No limits are currently set to user
    """
    keep_browser_open = True
    limit_message = 'Set your  limit'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register user
        """
        username = self.generate_user()
        birth_date = '1-06-1977'
        now = datetime.datetime.now()
        shifted_year = str(now.year + 5)
        self.__class__.currencycode = 'GBP'
        self.__class__.card_date = f'{now.month:02d}/{shifted_year[2:]}'
        self.__class__.first_name = Faker().first_name_female()
        if tests.settings.gvc_wallet_env == 'prod':
            self.site.register_new_user(username=username, birth_date=birth_date, first_name=self.first_name, password=tests.settings.default_password)
            user = username
        else:
            user_info = self.gvc_wallet_user_client.register_new_user(firstname=self.first_name, password=tests.settings.default_password)
            user = user_info.username
            self.site.login(username=user)

        password = tests.settings.default_password

        self.__class__.deposit_limits_data = self.gvc_wallet_user_client.get_deposit_limits_data(username=user,
                                                                                                 password=password)
        if not self.deposit_limits_data:
            raise GVCException('Deposit limits page is not configured on GVC side')

    def test_001_login_to_oxygen_and_navigate_to_gambling_controls(self):
        """
        DESCRIPTION: Login to Oxygen and navigate to My Account menu -> Gambling Controls
        EXPECTED: 'Gambling Controls' page is displayed
        """
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(), msg='Right menu is not displayed')
        gambling_controls_title = self.site.window_client_config.gambling_controls_title
        self.site.right_menu.click_item(item_name=gambling_controls_title, timeout=30)
        self.__class__.gambling_controls_page = self.site.gambling_controls
        self.assertTrue(self.gambling_controls_page.is_displayed(),
                        msg=f'"{gambling_controls_title}" page is not displayed')

    def test_002_pick_deposit_limits_option_should_be_picked_by_default_and_tap_on_choose_button(self):
        """
        DESCRIPTION: Pick 'Deposit limits' option (should be picked by default) and tap on 'Choose' button
        EXPECTED: * 'Set deposit limits' page is displayed
        EXPECTED: * 'Daily', 'Weekly' and 'Monthly' deposit limit textfields are displayed with Current limit value under each textfield
        EXPECTED: ![](index.php?/attachments/get/11918116)
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
        self.__class__.daily_field = self.set_deposit_limits_page.daily_field
        self.assertTrue(self.daily_field.is_displayed(), msg='"Daily" deposit limit textfield is not displayed')
        self.assertTrue(self.daily_field.current_limit.is_displayed(),
                        msg='"Current Limit" value for "Daily" deposit limit field is not displayed')

        self.__class__.weekly_field = self.set_deposit_limits_page.weekly_field
        self.assertTrue(self.weekly_field.is_displayed(), msg='"Weekly" deposit limit textfield is not displayed')
        self.assertTrue(self.weekly_field.current_limit.is_displayed(),
                        msg='"Current Limit" value for "Weekly" deposit limit field is not displayed')

        self.__class__.monthly_field = self.set_deposit_limits_page.monthly_field
        self.assertTrue(self.monthly_field.is_displayed(), msg='"Monthly" deposit limit textfield is not displayed')
        self.assertTrue(self.monthly_field.current_limit.is_displayed(),
                        msg='"Current Limit" value for "Monthly" deposit limit field is not displayed')

    def test_003_enter_daily_limit_value_higher_than_the_weekly_deposit_limit(self):
        """
        DESCRIPTION: Enter 'Daily' limit value higher than the 'Weekly' Deposit limit
        EXPECTED: "Weekly deposit limit has to be equal or higher than daily deposit limit." - displayed under 'Weekly' limit dropdown
        """
        self.daily_field.input_field.value = '12'
        self.weekly_field.input_field.value = '11'
        actual_error = self.weekly_field.warning_message.text
        expected_error = self.deposit_limits_data['content']['limitsForm']['form']['weekly']['validation']['Min']
        self.assertEqual(actual_error, expected_error,
                         msg=f'Actual warning message for "Weekly" field: "{actual_error}" '
                             f'is not equal to expected: "{expected_error}"')

    def test_004_enter_monthly_limit_value_lower_than_the_weekly_deposit_limit(self):
        """
        DESCRIPTION: Enter 'Monthly' limit value lower than the 'Weekly' Deposit limit
        EXPECTED: "Monthly deposit limit has to be equal or higher than weekly deposit limit." - displayed under 'Monthly' limit dropdown
        """
        self.monthly_field.input_field.value = '10'
        actual_error = self.monthly_field.warning_message.text
        expected_error = self.deposit_limits_data['content']['limitsForm']['form']['monthly']['validation']['Min']
        self.assertEqual(actual_error, expected_error,
                         msg=f'Actual warning message for "Monthly" field: "{actual_error}" '
                             f'is not equal to expected: "{expected_error}"')

    def test_005_add_correct_daily_weekly_monthly_and_click_on_save_button(self):
        """
        DESCRIPTION: Add correct Daily/Weekly/Monthly (e.g. 100/500/1000) and click on "Save" button
        EXPECTED: * "DAILY DEPOSIT LIMIT,WEEKLY DEPOSIT LIMIT,MONTHLY DEPOSIT LIMIT: Your limits have been changed." message is displayed on green background with the tick icon
        EXPECTED: * 'Current limit' values are changed under each dropdown
        """
        self.__class__.daily_value = '100'
        self.daily_field.input_field.value = self.daily_value

        self.__class__.old_weekly_value = '101'
        self.weekly_field.input_field.value = self.old_weekly_value

        self.__class__.monthly_value = '102'
        self.monthly_field.input_field.value = self.monthly_value

        self.set_deposit_limits_page.save_button.click()
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

    def test_006_try_to_increase_the_monthly_deposit_limit(self):
        """
        DESCRIPTION: Try to increase the Weekly Deposit limit (e.g. 800)
        EXPECTED: * "Confirmation sent." header with "Your requested limits will be available within 24 hours." message and active 'Cancel the change request' button is displayed on blue background with information sign.
        EXPECTED: * 'Weekly' field is populated with the value entered  and greyed out
        EXPECTED: * 'Current limit' for 'Weekly' limit is still showing limit entered in step 5
        """
        self.__class__.new_weekly_value = '800'
        self.set_deposit_limits_page.weekly_field.input_field.value = self.new_weekly_value
        self.set_deposit_limits_page.save_button.click()

        actual_popup_header = self.set_deposit_limits_page.message_popup.header.text
        expected_popup_header, expected_popup_text = self.deposit_limits_data['content']['limitsDataForm']['messages']['LimitsPending'].split('</h3>')
        self.assertEqual(actual_popup_header, cleanhtml(expected_popup_header),
                         msg=f'"{actual_popup_header}" popup header is not '
                             f'equal to expected "{cleanhtml(expected_popup_header)}"')

        actual_popup_text = self.set_deposit_limits_page.message_popup.popup_text

        expected_popup_text = expected_popup_text.format(self.deposit_limits_data['time']).strip()
        self.assertEqual(actual_popup_text, expected_popup_text,
                         msg=f'"{actual_popup_text}" popup text is not equal to expected "{expected_popup_text}"')

        actual_link_text = self.set_deposit_limits_page.message_popup.link.name
        expected_link_text = self.deposit_limits_data['content']['limitsDataForm']['messages']['RemoveLimitsCancelLink']
        self.assertEqual(actual_link_text, expected_link_text,
                         msg=f'"{actual_link_text}" popup link is not equal to expected "{expected_link_text}"')

        self.assertTrue(self.set_deposit_limits_page.message_popup.link.is_enabled(),
                        msg=f'"{expected_link_text}" link is not enabled')

        actual_color = self.set_deposit_limits_page.message_popup.background_color_name
        self.assertEqual(actual_color, 'blue', msg=f'Instead of blue, actual color for '
                                                   f'"Your limits have been changed." popup is: "{actual_color}"')

        # Weekly field verifications
        actual_value = self.set_deposit_limits_page.weekly_field.input_field.value
        self.assertEqual(actual_value, self.new_weekly_value,
                         msg=f'Value for Weekly field is wrong. '
                             f'Actual: "{actual_value}". Expected: "{self.new_weekly_value}"')
        weekly_current_limit = self.set_deposit_limits_page.weekly_field.current_limit.name
        self.assertIn(self.old_weekly_value, weekly_current_limit,
                      msg=f'Weekly limit was not changed correctly. Expected: "{self.old_weekly_value}", '
                          f'but full message is: "{weekly_current_limit}"')
        self.assertFalse(self.set_deposit_limits_page.weekly_field.input_field.is_enabled(expected_result=False),
                         msg='Weekly field should not be active')

    def test_007_press_cancel_the_change_request_button_on_blue_information_message(self):
        """
        DESCRIPTION: Press 'Cancel the change request' button on blue information message
        EXPECTED: * 'Cancel limit change request' dialogue is displayed
        EXPECTED: * "You are about to cancel the recent requested change to your limits. Are you sure want to do that?" message is shown
        EXPECTED: * No/Yes buttons are displayed
        """
        self.assertTrue(self.set_deposit_limits_page.message_popup.is_displayed(),
                        msg='"Confirmation Sent" information message is not displayed')
        sleep(2)  # link is displayed but click does not work, so added sleep
        self.set_deposit_limits_page.message_popup.link.click()
        self.__class__.cancel_limit_change_request = self.site.cancel_limit_change_request
        self.assertTrue(self.cancel_limit_change_request.header.is_displayed(),
                        msg='"Cancel limit change request" dialogue is not displayed')
        actual_message = self.cancel_limit_change_request.message.text
        expected_message = cleanhtml(self.deposit_limits_data['content']['removeLimitsFormDialog']['text'])
        self.assertEqual(actual_message, expected_message,
                         msg=f'Actual "cancel limit change request" message: "{actual_message}" '
                             f'is not equal to expected: "{expected_message}"')
        self.assertTrue(self.cancel_limit_change_request.yes_button.is_displayed(),
                        msg='"Yes" button is not displayed for "Cancel limit change request"')
        self.assertTrue(self.cancel_limit_change_request.no_button.is_displayed(),
                        msg='"No" button is not displayed for "Cancel limit change request"')

    def test_008_press_yes_button(self):
        """
        DESCRIPTION: Press 'Yes' button
        EXPECTED: * "Your request was cancelled." header with "You can now change the limits again and confirm your new request." message is displayed on blue background with information sign.
        EXPECTED: * 'Weekly' field is populated with the value entered in step 5 and is active
        EXPECTED: * 'Current limit' for 'Weekly' limit is showing limit entered in step 5
        """
        self.cancel_limit_change_request.yes_button.click()
        expected_popup_header, expected_popup_text = self.deposit_limits_data['content']['limitsDataForm']['messages']['CanceledInfoMessage'].split('</h3>')
        result = wait_for_result(
            lambda: self.set_deposit_limits_page.message_popup.header.text == cleanhtml(expected_popup_header),
            expected_result=True,
            name='Popup dialog to change',
            timeout=15)
        self.assertTrue(result, msg=f'"{self.set_deposit_limits_page.message_popup.header.text}" popup header '
                                    f'is not equal to expected "{cleanhtml(expected_popup_header)}"')
        expected_popup_text = expected_popup_text.strip()
        actual_popup_text = self.set_deposit_limits_page.message_popup.popup_text
        self.assertEqual(actual_popup_text, expected_popup_text,
                         msg=f'"{actual_popup_text}" popup text is not equal to expected "{expected_popup_text}"')

        actual_color = self.set_deposit_limits_page.message_popup.background_color_name
        self.assertEqual(actual_color, 'blue', msg=f'Instead of blue, actual color for '
                                                   f'"Your limits have been changed." popup is: "{actual_color}"')

        # Weekly field verifications
        actual_value = self.set_deposit_limits_page.weekly_field.input_field.value
        self.assertEqual(actual_value, self.old_weekly_value,
                         msg=f'Value for Weekly field is wrong. '
                             f'Actual: "{actual_value}". Expected: "{self.old_weekly_value}"')
        weekly_current_limit = self.set_deposit_limits_page.weekly_field.current_limit.name
        self.assertIn(self.old_weekly_value, weekly_current_limit,
                      msg=f'Weekly limit was not changed correctly. Expected: "{self.old_weekly_value}", '
                          f'but full message is: "{weekly_current_limit}"')
        self.assertTrue(self.set_deposit_limits_page.weekly_field.is_enabled(), msg='Weekly field is not active')

    def test_009_press_on_remove_limits_green_button(self):
        """
        DESCRIPTION: Press on 'Remove limits' green button
        EXPECTED: * "Confirmation sent." header with "Your requested limits will be available within 24 hours." message and active 'Cancel the change request' button is displayed on blue background with information sign.
        EXPECTED: * All field are populated with the 'Set your <daily/weekly/monthly> limit' grey placeholder and are disabled
        EXPECTED: * 'Current limit' values are showing limits entered in step 5
        """
        self.set_deposit_limits_page.remove_limits.click()
        # need for page to reload
        sleep(5)
        self.__class__.set_deposit_limits_page = self.site.set_deposit_limits
        expected_popup_header, expected_popup_text = self.deposit_limits_data['content']['limitsDataForm']['messages'][
            'LimitsPending'].split('</h3>')
        result = wait_for_result(
            lambda: self.set_deposit_limits_page.message_popup.header.text == cleanhtml(expected_popup_header),
            expected_result=True,
            name='Popup dialog to change',
            timeout=15)
        self.assertTrue(result, msg=f'"{self.set_deposit_limits_page.message_popup.header.text}" popup header '
                                    f'is not equal to expected "{cleanhtml(expected_popup_header)}"')
        actual_popup_text = self.set_deposit_limits_page.message_popup.popup_text
        expected_popup_text = expected_popup_text.format(self.deposit_limits_data['time']).strip()
        self.assertEqual(actual_popup_text, expected_popup_text,
                         msg=f'"{actual_popup_text}" popup text is not equal to expected "{expected_popup_text}"')

        actual_link_text = self.set_deposit_limits_page.message_popup.link.name
        expected_link_text = self.deposit_limits_data['content']['limitsDataForm']['messages']['RemoveLimitsCancelLink']
        self.assertEqual(actual_link_text, expected_link_text,
                         msg=f'"{actual_link_text}" popup link is not equal to expected "{expected_link_text}"')

        self.assertTrue(self.set_deposit_limits_page.message_popup.link.is_enabled(),
                        msg=f'"{expected_link_text}" link is not enabled')

        actual_color = self.set_deposit_limits_page.message_popup.background_color_name
        self.assertEqual(actual_color, 'blue', msg=f'Instead of blue, actual color for '
                                                   f'"Your limits have been changed." popup is: "{actual_color}"')

        self.assertFalse(self.set_deposit_limits_page.daily_field.input_field.is_enabled(expected_result=False),
                         msg='Daily field should not be active')
        self.assertFalse(self.set_deposit_limits_page.weekly_field.input_field.is_enabled(expected_result=False),
                         msg='Weekly field should not be active')
        self.assertFalse(self.set_deposit_limits_page.monthly_field.input_field.is_enabled(expected_result=False),
                         msg='Monthly field should not be active')

        actual_daily_pl = self.set_deposit_limits_page.daily_field.input_field.placeholder
        limits_placeholder = self.deposit_limits_data['content']['limitsForm']['children']['setdepositlimitssection']['messages']['SetYourLimitsPlaceholder']
        expected_daily_pl = limits_placeholder.format('daily')
        self.assertTrue(actual_daily_pl in [expected_daily_pl, self.limit_message], msg=f'Actual placeholder "{actual_daily_pl}" is not equal 'f'to expected "{expected_daily_pl}" for "Daily" field"')

        actual_weekly_pl = self.set_deposit_limits_page.weekly_field.input_field.placeholder
        expected_weekly_pl = limits_placeholder.format('weekly')
        self.assertTrue(actual_weekly_pl in [expected_weekly_pl, self.limit_message],
                        msg=f'Actual placeholder "{actual_weekly_pl}" is not equal ' f'to expected "{expected_weekly_pl}" for "Weekly" field"')

        actual_monthly_pl = self.set_deposit_limits_page.monthly_field.input_field.placeholder
        expected_monthly_pl = limits_placeholder.format('monthly')
        self.assertTrue(actual_monthly_pl in [expected_monthly_pl, self.limit_message],
                        msg=f'Actual placeholder "{actual_monthly_pl}" is not equal ' f'to expected "{expected_monthly_pl}" for "Monthly" field"')

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

    def test_010_1_close_deposit_limit_page2_navigate_to_my_account_menu___cashier___deposit_and_try_to_deposit_an_amount_higher_than_the_daily_deposit_limit_set_in_step_5(self):
        """
        DESCRIPTION: 1) Close 'Deposit limit' page
        DESCRIPTION: 2) Navigate to My Account menu -> Cashier -> Deposit and try to deposit an amount Higher than the Daily Deposit Limit set in step 5
        EXPECTED: * "Warning: self-set deposit limit exceeded" header with message "{USERNAME} You have exceeded the daily deposit limit of
        EXPECTED: * {CURRENCY CODE and VALUE} previously set by you. Click the below button to increase your deposit limits.
        EXPECTED: * Click the Deposit button below to submit your request again with the revised deposit amount of {CURRENCY CODE and VALUE} (CURRENCY CODE and VALUE} excluding the 0.00 GBP fee).
        EXPECTED: * If you prefer, you can cancel this deposit request and return to the Deposits page" is displayed on blue background.
        EXPECTED: * DEPOSIT {CURRENCY CODE and VALUE} NOW button is displayed
        EXPECTED: * The deposit is not successful. The amount is not added to the customer's balance.
        """
        if self.device_type == 'mobile':
            self.set_deposit_limits_page.close_button.click()

        self.navigate_to_page(name='/')  # for tst endpoints
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

        # Since we only currently test with Visa card:
        deposit_option_name = 'visa'
        deposit_option = available_deposit_options.get(deposit_option_name)
        self.assertTrue(deposit_option, msg=f'Deposit option for "{deposit_option_name}" is absent')
        self.assertTrue(deposit_option.is_displayed(),
                        msg=f'"{deposit_option_name}" payment method is not displayed')
        deposit_option.click()
        self.assertTrue(self.site.deposit.is_displayed(),
                        msg='"Deposit page" is not displayed')

        self.site.deposit.add_new_card_and_deposit(amount='101',
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
        deposit_limit_warning_page.close_button.click()
        self.site.wait_content_state('HomePage')
        self.assertEqual(self.site.header.user_balance, 0, msg='The amount is added to the customer\'s balance.')
