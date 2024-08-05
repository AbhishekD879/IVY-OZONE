import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.medium
# @pytest.mark.sanity
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C16473694_Verify_Short_Break_Cancel_button(BaseUserAccountTest):
    """
    TR_ID: C16473694
    NAME: Verify Short Break 'Cancel' button
    DESCRIPTION: This test case verifies 'Short Break' 'Cancel' button.
    PRECONDITIONS: Oxygen app is loaded and the user is logged in
    PRECONDITIONS: Navigate to 'My Account' -> 'Settings' -> 'Gambling Control'
    PRECONDITIONS: 'Gambling Controls' page is opened and 'Deposit Limits' option is selected by default
    """
    keep_browser_open = True

    def test_001_select_account_closure_option(self):
        """
        DESCRIPTION: Select 'Account Closure' option.
        EXPECTED: Option is selected and description is changed to 'Select this option if you would like to stop playing on some or all of our products'
        """
        self.__class__.username = tests.settings.default_username
        self.site.login(username=self.username)
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item('Gambling Controls')
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=20),
                        msg=f'"Gambling Controls" page is not opened')
        deposit_limit_option = self.site.window_client_config.mobile_portal_spending_controls
        actual_option_name = self.site.gambling_controls.selected_option
        self.assertEqual(deposit_limit_option, actual_option_name,
                         msg=f'"{deposit_limit_option}" option, on "Gambling Controls" page is not selected by default.'
                             f'"{actual_option_name}" is selected instead.')

    def test_002_click_choose_button(self):
        """
        DESCRIPTION: Click 'CHOOSE' button.
        EXPECTED: Account Closure options are displayed as radio buttons:
        EXPECTED: - I’d like to close my account
        EXPECTED: - I’d like to take an irreversible time-out or exclude myself from gaming.
        """
        self.site.gambling_controls.account_closure.click()
        self.site.gambling_controls.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        account_closure_options = self.site.account_closure.items_as_ordered_dict
        self.assertTrue(account_closure_options, msg='List of options isn\'t displayed on the page')
        list_products_names = [x for x in list(account_closure_options.keys()) if x]
        expected_list = [vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1, vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_2]
        self.assertListEqual(expected_list, list_products_names,
                             msg=f'Account closure options from response: \n"{expected_list}" are not '
                                 f'the same as on UI: \n"{list_products_names}"')

    def test_003_click_cancel_button(self):
        """
        DESCRIPTION: Click 'CANCEL' button.
        EXPECTED: User returns to Gambling Controls page.
        EXPECTED: 'Deposit Limits' option is selected by default.
        """
        self.site.account_closure.cancel_button.click()
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=20),
                        msg=f'"Gambling Controls" page is not opened')
        deposit_limit_option = self.site.window_client_config.mobile_portal_spending_controls
        actual_option_name = self.site.gambling_controls.selected_option
        self.assertEqual(deposit_limit_option, actual_option_name,
                         msg=f'"{deposit_limit_option}" option, on "Gambling Controls" page is not selected by default.'
                             f'"{actual_option_name}" is selected instead.')

    def test_004_select_account_closure_option_and_click_choose_button(self):
        """
        DESCRIPTION: Select 'Account Closure' option and click 'CHOOSE' button.
        EXPECTED: Account Closure options are displayed as radio buttons:
        EXPECTED: - I’d like to close my account
        EXPECTED: - I’d like to take an irreversible time-out or exclude myself from gaming.
        """
        self.site.gambling_controls.account_closure.click()
        self.site.gambling_controls.choose_button.click()
        options = self.site.account_closure.items_as_ordered_dict
        self.assertTrue(options, msg="Account closure options are displayed")
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')

    def test_005_select_id_like_to_take_a_short_break_option_and_click_continue_button(self):
        """
        DESCRIPTION: Select 'I’d like to take a short break' option and click 'CONTINUE' button.
        EXPECTED: Service Closure page is displayed. It contains the list of products available to the user. Each product has its separate 'CLOSE' button.
        EXPECTED: At the bottom there is a 'CLOSE ALL' button to close all products.
        """
        self.site.account_closure.select_option(option_name=vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1)
        continue_button = self.site.account_closure.continue_button
        self.assertTrue(continue_button.is_displayed(), msg=f'"Continue" button is not displayed')
        self.assertTrue(continue_button.is_enabled(timeout=5), msg=f'"Continue" button is not enabled')
        continue_button.click()
        self.assertTrue(self.site.service_closure.is_displayed(), msg=f'"Service Closure" page is not opened')
        self.__class__.closure_details = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(self.closure_details, msg='List of products isn\'t available to the user')
        for product_name, product in self.closure_details.items():
            self.assertTrue(product.close_button.is_displayed(),
                            msg=f'"{product_name}" product doesn\'t have separate "CLOSE" button')
        self.assertTrue(self.site.service_closure.close_all_button.is_displayed(),
                        msg=f'There is no a "CLOSE ALL" button')

    def test_006_click_close__button_for_any_of_the_products(self):
        """
        DESCRIPTION: Click 'CLOSE'  button for any of the products.
        EXPECTED: User is taken to the page with the detailed information about service closure.
        """
        self.__class__.product_name, product = list(self.closure_details.items())[0]
        product.close_button.click()
        selected_product = self.site.service_closure.selected_product
        self.assertEqual(selected_product, self.product_name,
                         msg=f'User isn\'t taken to the page with the detailed information, selected product is "{selected_product}"')

    def test_007_click_cancel_button(self):
        """
        DESCRIPTION: Click 'CANCEL' button.
        EXPECTED: User returns to Gambling Controls page.
        EXPECTED: 'Deposit Limits' option is selected by default.
        """
        self.site.account_closure.cancel_button.click()
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=20),
                        msg=f'"Gambling Controls" page is not opened')
        deposit_limit_option = self.site.window_client_config.mobile_portal_spending_controls
        actual_option_name = self.site.gambling_controls.selected_option
        self.assertEqual(deposit_limit_option, actual_option_name,
                         msg=f'"{deposit_limit_option}" option, on "Gambling Controls" page is not selected by default.'
                             f'"{actual_option_name}" is selected instead.')

    def test_008_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps 4-6.
        EXPECTED: User is taken to the page with the detailed information about service closure.
        """
        self.test_004_select_account_closure_option_and_click_choose_button()
        self.test_005_select_id_like_to_take_a_short_break_option_and_click_continue_button()
        self.test_006_click_close__button_for_any_of_the_products()

    def test_009_select_any_duration_radio_button(self):
        """
        DESCRIPTION: Select any 'Duration' radio button.
        EXPECTED: Duration is selected.
        """
        duration_options = self.site.service_closure.duration_options.items_as_ordered_dict
        self.assertTrue(duration_options, msg='Duration radio buttons aren\'t displayed')
        duration_name, duration = list(duration_options.items())[0]
        duration.click()
        self.assertTrue(duration.is_checked(), msg=f'Duration "{duration_name}" is not selected')

    def test_010_select_any_reason_for_closure_radio_button(self):
        """
        DESCRIPTION: Select any 'Reason for closure' radio button.
        EXPECTED: Reason is selected.
        """
        reason_options = self.site.service_closure.reason_options.items_as_ordered_dict
        self.assertTrue(reason_options, msg='Reason radio buttons aren\'t displayed')
        reason_name, reason = list(reason_options.items())[0]
        reason.click()
        self.assertTrue(reason.is_checked(), msg=f'Reason "{reason_name}" is not selected')

    def test_011_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button.
        EXPECTED: Service Closure confirmation page is displayed.
        """
        self.site.service_closure.continue_button.click()
        selected_product = self.site.service_closure.selected_product
        self.assertEqual(selected_product, self.product_name,
                         msg=f'User isn\'t taken to the page with the detailed information, selected product is "{selected_product}"')

    def test_012_click_cancel_button(self):
        """
        DESCRIPTION: Click 'CANCEL' button.
        EXPECTED: User returns to Gambling Controls page.
        EXPECTED: 'Deposit Limits' option is selected by default.
        """
        self.site.account_closure.cancel_button.click()
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=20),
                        msg=f'"Gambling Controls" page is not opened')
        deposit_limit_option = self.site.window_client_config.mobile_portal_spending_controls
        actual_option_name = self.site.gambling_controls.selected_option
        self.assertEqual(deposit_limit_option, actual_option_name,
                         msg=f'"{deposit_limit_option}" option, on "Gambling Controls" page is not selected by default.'
                             f'"{actual_option_name}" is selected instead.')
