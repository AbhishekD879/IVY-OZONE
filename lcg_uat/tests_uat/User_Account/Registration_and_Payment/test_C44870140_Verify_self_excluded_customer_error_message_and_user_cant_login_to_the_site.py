import datetime
import pytest
import tests
from selenium.webdriver.support.select import Select
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result
from time import sleep


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.uat
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870140_Verify_self_excluded_customer_error_message_and_user_cant_login_to_the_site(BaseBetSlipTest):
    """
    TR_ID: C44870140
    NAME: Verify self excluded customer error message and user can't login to the site.
    PRECONDITIONS: User should be logged in to view the 'Self Exclusion' form
    """
    keep_browser_open = True
    deposit_amount = 20.00
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'
    wrong_password = "Ivy@1234"

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.__class__.user_name = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_payment_card_and_deposit(amount=self.deposit_amount, card_number=tests.settings.master_card,
                                                                 card_type='mastercard', expiry_month=self.expiry_month,
                                                                 expiry_year=self.expiry_year, cvv=tests.settings.master_card_cvv)
        self.site.login(username=self.user_name)
        self.site.wait_content_state("Homepage")

    def test_002_tap_my_account_item(self):
        """
        DESCRIPTION: Tap 'My account' item
        EXPECTED: 'My account' page is opened with full list of items
        """
        self.site.header.right_menu_button.click()
        list_of_right_menu_items = self.site.right_menu.items_names
        self.assertTrue((item in vec.bma.EXPECTED_LIST_OF_RIGHT_MENU for item in list_of_right_menu_items),
                        msg=f'Actual right menu items: "{list_of_right_menu_items}" are not same as Expected right menu items: "{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU}"')

    def test_003_tap_gambling_controls(self):
        """
        DESCRIPTION: Tap 'Gambling controls'
        EXPECTED: The 'Gambling controls' page is opened
        """
        self.site.right_menu.click_item(vec.bma.GAMBLING_CONTROLS.upper())
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=20)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"{vec.bma.GAMBLING_CONTROLS}" page is not found')

    def test_004_select_account_closure__reopening___choose(self):
        """
        DESCRIPTION: Select 'Account Closure & Reopening'  & Choose
        EXPECTED: Account Closure & Reopening page  is displayed
        EXPECTED: With two options
        EXPECTED: 1. I want to close my account or sections of it
        EXPECTED: 2. I'd like to take an irreversible time-out or exclude myself from gaming.
        """
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        options = self.site.account_closure.items_names
        self.assertTrue(options, msg=f'Expected options: "{options}" not available')
        self.assertEqual(options[0], vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1,
                         msg=f'Expected option: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1}" is not same as Actual option: "{options[0]}"')
        self.assertEqual(options[1], vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2,
                         msg=f'Expected option: "{vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2}" is not same as Actual option: "{options[1]}"')

    def test_005_verify_cancel_button(self):
        """
        DESCRIPTION: Verify Cancel button
        EXPECTED: Cancel button is active and user is redirected to the previous page (Gambling controls) when clicks on Cancel
        """
        self.assertTrue(self.site.account_closure.cancel_button.is_enabled(), msg=f'"{vec.account.CANCEL}" button is not active')
        self.site.account_closure.cancel_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg=f'"{vec.bma.GAMBLING_CONTROLS}" page is not found')

    def test_006_select_account_closure__reopening___choose(self):
        """
        DESCRIPTION: Select 'Account Closure & Reopening'  & Choose
        EXPECTED: Account Closure & Reopening page  is displayed
        EXPECTED: With two options
        EXPECTED: 1. I want to close my account or sections of it
        EXPECTED: 2. I'd like to take an irreversible time-out or exclude myself from gaming.
        """
        self.test_004_select_account_closure__reopening___choose()

    def test_007_select_id_like_to_take_an_irreversible_time_out_or_exclude_myself_from_gaming(self):
        """
        DESCRIPTION: Select 'I'd like to take an irreversible time-out or exclude myself from gaming.
        EXPECTED: Option is selected and Continue button becomes active
        """
        self.site.account_closure.click_item(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2)
        self.assertTrue(self.site.account_closure.continue_button.is_enabled(), msg=f'"{vec.account.CONTINUE}" button is not enabled')

    def test_008_verify_continue_button(self):
        """
        DESCRIPTION: Verify Continue button
        EXPECTED: User is taken to Take a short time-out page with options & reason for taking break
        EXPECTED: Note: For 'Self-Exclusion' the user has to click the 'Self-exclusion' link at the bottom.
        """
        self.site.account_closure.continue_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/selfexclusion'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=10)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url, msg='"Take a short time-out" page is not found')
        self.site.wait_splash_to_hide(7)

    def test_009_click_on_the_self_exclusion_link(self):
        """
        DESCRIPTION: Click on the Self Exclusion link
        EXPECTED: The user is taken to next page with Self-exclusion & Gamstop options
        """
        self.site.self_exclusion.self_exclusion_link.scroll_to()
        self.site.self_exclusion.self_exclusion_link.click()
        self.site.wait_splash_to_hide(3)
        self.__class__.images = self.site.self_exclusion_selection.image
        self.assertTrue(self.images, msg='"Self-exclusion & Gamstop options" are not available')

    def test_010_select_self_exclusion_and_choose(self):
        """
        DESCRIPTION: Select 'Self-exclusion' and Choose
        EXPECTED: Self-exclusion page is opened with options of select the Period to be excluded and brand to select with drop down.
        """
        self.images[0].click()
        self.site.self_exclusion_selection.choose_button.click()
        self.__class__.duration = self.site.self_exclusion_options.duration_options
        self.assertTrue(self.duration, msg='"Duration options" are not available')
        self.__class__.reason = self.site.self_exclusion_options.reason_options
        self.assertTrue(self.duration, msg='"Reason options" are not available')
        self.__class__.brands = Select(self.site.self_exclusion_options.brand)
        self.assertTrue(self.brands, msg='"Brand" is not available')

    def test_011_verify_select_the_brand_you_wish_to_exclude_from_from_the_drop_down_a(self):
        """
        DESCRIPTION: Verify 'Select the brand you wish to exclude from' from the drop down, select the Period to be excluded and tick box
        EXPECTED: User is able to select the brand from where they want to be excluded
        EXPECTED: Once selected, the "Continue" button becomes active.
        """
        self.brands.select_by_index("1")
        self.duration[0].click()
        click(self.reason[0])
        self.assertTrue(self.site.self_exclusion_options.continue_button.is_enabled(),
                        msg=f'"{vec.account.CONTINUE}" button is not enabled')

    def test_012_select_continue_after_choosing_time_brand_to_be_self_exculded__tick_box(self):
        """
        DESCRIPTION: Select "Continue" after choosing time, brand to be self-exculded & tick box
        EXPECTED: User is taken to the next page asking to enter "Password"
        EXPECTED: "Self-exclude" tab is inactive when no password is entered.
        """
        self.site.self_exclusion_options.continue_button.click()
        self.assertFalse(self.site.self_exclusion_options.self_exclude_button.is_enabled(expected_result=False),
                         msg='"Self-exclude" button is not enabled')

    def test_013_enter_a_invalid_password_into_password_field_and_select_self_exclude(self):
        """
        DESCRIPTION: Enter a invalid password into "Password" field and select "Self-Exclude"
        EXPECTED: Error message "Incorrect password" (field is highlighted with red colour)
        """
        self.site.self_exclusion_options.password_input(self.wrong_password)
        self.site.self_exclusion_options.self_exclude_button.click()
        self.assertTrue(self.site.self_exclusion_options.info_message.is_displayed(),
                        msg='"Incorrect Password" info message is not displayed')

    def test_014_enter_a_valid_password_into_password_link_and_select_self_exclude(self):
        """
        DESCRIPTION: Enter a valid password into "Password" link and select "Self-exclude"
        EXPECTED: Confirmation of self exclusion box is opened with
        EXPECTED: two tick boxes
        EXPECTED: 1. I confirm that I wish to self-exclude.......
        EXPECTED: 2. I understand that during this period...........
        EXPECTED: with "YES" button inactive
        """
        self.site.self_exclusion_options.password_input(tests.settings.default_password)
        self.site.self_exclusion_options.self_exclude_button.click()

        # TODO: Commented code can be removed after steps got updated
        # self.assertTrue(self.site.self_exclusion_dialog.confirm_checkbox.is_enabled(),
        #                 msg=f'Confirmation text: "{vec.bma.SELF_EXCLUSION_USER_CONFIRMATION_TEXT_1}" is not displayed')
        # self.assertTrue(self.site.self_exclusion_dialog.understand_checkbox.is_enabled(),
        #                 msg=f'Confirmation text: "{vec.bma.SELF_EXCLUSION_USER_CONFIRMATION_TEXT_1}" is not displayed')
        # self.assertFalse(self.site.self_exclusion_dialog.yes.is_enabled(),
        #                  msg='"Yes" button is enabled')

    def test_015_select_both_the_tick_boxes_and_tap_yes(self):
        """
        DESCRIPTION: Select both the tick boxes and tap "Yes"
        EXPECTED: The confirmation pop up message is shown
        EXPECTED: "You have successfully excluded from all our products"
        EXPECTED: User is not logged out of the app.
        """
        # TODO: Commented code can be removed after steps got updated
        # self.site.self_exclusion_dialog.confirm_checkbox.click()
        # self.site.self_exclusion_dialog.understand_checkbox.click()
        # self.site.self_exclusion_dialog.yes.click()
        actual_text = self.site.self_exclusion_options.info_message.text
        self.assertEqual(actual_text, vec.bma.SELF_EXCLUDED_INFO_MESSAGE,
                         msg=f'Actual self-excluded message: "{actual_text}" is not same as Expected self-excluded message: "{vec.bma.SELF_EXCLUDED_INFO_MESSAGE}"')
        self.assertFalse(self.site.wait_logged_out(), msg='"User" is logged out of the application')

    def test_016_navigate_to_the_homepage_and_try_placing_any_bets(self):
        """
        DESCRIPTION: Navigate to the Homepage and try placing any bets
        EXPECTED: User will not be able to place bets.
        """
        self.navigate_to_page("Homepage")
        selection_ids = self.get_active_event_selections_for_category()
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])
        self.place_and_validate_single_bet()
        sleep(3)  # getting attribute error due to synchronization issue
        actual_message = self.get_betslip_content().suspended_account_warning_message.text
        self.assertEqual(actual_message, vec.betslip.ACCOUNT_SUSPENDED,
                         msg=f'Actual suspension message: "{actual_message}" is not same as expected suspension message: "{vec.betslip.ACCOUNT_SUSPENDED}"')

    def test_017_log_off_and_try_to_log_in_with_the_same_credentials(self):
        """
        DESCRIPTION: Log off and try to log in with the same credentials
        EXPECTED: User cannot log in
        EXPECTED: error message shown stating
        EXPECTED: "Your account is locked because you have chosen to self-exclude......."
        """
        self.navigate_to_page("Homepage")
        self.site.logout()
        self.site.wait_logged_out(15)
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        dialog.username = self.user_name
        dialog.password = tests.settings.default_password
        dialog.click_login()
        actual_error_message = wait_for_result(lambda: self.site.login_dialog.error_message,
                                               name='error message will be displayed')
        self.assertEqual(actual_error_message, vec.bma.SELF_EXCLUDED_LOGIN_ERROR_MESSAGE,
                         msg=f'User: "{self.user_name}" is not excluded from Products')
