import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.gvc_exeption import GVCException
from voltron.utils.helpers import cleanhtml


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C16446128_Verify_Short_Break_functionality(BaseUserAccountTest):
    """
    TR_ID: C16446128
    NAME: Verify Short Break functionality
    DESCRIPTION: This test case verifies 'Short Break' functionality
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Register user
        DESCRIPTION: Oxygen app is loaded and the user is logged in
        DESCRIPTION: Navigate to 'My Account' -> 'Gambling Control'
        DESCRIPTION: 'Gambling Controls' page is opened and 'Deposit Limits' option is selected by default
        DESCRIPTION: Please note that this feature is handled on GVC side ( text can be changed)
        """
        user_data = self.gvc_wallet_user_client.register_new_user()
        self.__class__.username = user_data.username
        self.__class__.password = user_data.password
        self.add_card_and_deposit(username=self.username,
                                  card_number=tests.settings.master_card,
                                  amount=tests.settings.min_deposit_amount)

        self.__class__.gambling_controls_data = self.gvc_wallet_user_client.get_gambling_controls_data(username=self.username,
                                                                                                       password=self.password)
        if not self.gambling_controls_data:
            raise GVCException('Gambling Controls page is not configured on GVC side')

        self.site.login(username=self.username)

        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.right_menu.is_displayed(timeout=3),
                        msg='User menu is not opened')
        self.site.right_menu.click_item(item_name=self.site.window_client_config.gambling_controls_title)
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=10),
                        msg=f'"Gambling Controls" page is not opened')

        deposit_limit_option = self.site.window_client_config.mobile_portal_spending_controls

        actual_option_name = self.site.gambling_controls.selected_option
        self.assertEqual(deposit_limit_option, actual_option_name,
                         msg=f'"{deposit_limit_option}" option, on "Gambling Controls" page is not selected by default.'
                         f'"{actual_option_name}" is selected instead.')

    def test_001_select_account_closure_option(self):
        """
        DESCRIPTION: Select 'Account Closure' option.
        EXPECTED: Option is selected and description is changed to 'Select this option if you would like to stop playing on some or all of our products'
        """
        account_closure_and_reopening = next((item for item in self.gambling_controls_data.get('items', {})
                                              if item.get('targetPageUrl', '').endswith('accountclosure')), None)
        if not account_closure_and_reopening:
            raise GVCException('Cannot find "Account Closure & Reopening" in Gambling Controls')
        account_closure_and_reopening_option = account_closure_and_reopening.get('title')
        result = self.site.gambling_controls.select_option(option_name=account_closure_and_reopening_option)

        self.assertTrue(result,
                        msg=f'"{account_closure_and_reopening_option}" option, on "Gambling Controls" page is not selected after click')

        account_closure_text = cleanhtml(account_closure_and_reopening.get('text'))
        expected_text = account_closure_text.replace('\n', '').replace('  ', '')
        actual_option_name = self.site.gambling_controls.option_content.replace('\n', '')
        self.assertEqual(actual_option_name, expected_text,
                         msg=f'Actual description: "{actual_option_name}" is not the same as from response: "{expected_text}"')

    def test_002_click_choose_button(self):
        """
        DESCRIPTION: Click 'CHOOSE' button.
        EXPECTED: Account Closure options are displayed as radio buttons:
        EXPECTED: - I’d like to take a short break
        EXPECTED: - I’d like to close my account
        EXPECTED: - I’d like to take an irreversible time-out or exclude myself from gaming.
        """
        self.site.gambling_controls.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')

        account_closure_data = self.gvc_wallet_user_client.get_account_closure_data(username=self.username,
                                                                                    password=self.password)
        if not account_closure_data:
            raise GVCException('Account Closure options are not configured on GVC side')

        self.__class__.account_options = [i['title'] for i in account_closure_data['items']]
        account_closure_options = self.site.account_closure.items_as_ordered_dict
        self.assertTrue(account_closure_options, msg='List of options isn\'t displayed on the page')
        list_products_names = [x for x in list(account_closure_options.keys()) if x]
        self.assertListEqual(self.account_options, list_products_names,
                             msg=f'Account closure options from response: \n"{self.account_options}" are not '
                             f'the same as on UI: \n"{list_products_names}"')

    def test_003_select_id_like_to_take_a_short_break_option_and_click_continue_button(self):
        """
        DESCRIPTION: Select 'I’d like to take a short break' option and click 'CONTINUE' button.
        EXPECTED: Service Closure page is displayed. It contains the list of products available to the user. Each product has its separate 'CLOSE' button.
        EXPECTED: At the bottom there is a 'CLOSE ALL' button to close all products.
        """
        self.site.account_closure.select_option(option_name=self.account_options[0])

        continue_button = self.site.account_closure.continue_button

        self.assertTrue(continue_button.is_displayed(), msg=f'"Continue" button is not displayed')
        self.assertTrue(continue_button.is_enabled(timeout=5), msg=f'"Continue" button is not enabled')
        continue_button.click()

        self.assertTrue(self.site.service_closure.is_displayed(), msg=f'"Service Closure" page is not opened')

        self.__class__.service_closure_resp = self.gvc_wallet_user_client.get_service_closure_data(username=self.username,
                                                                                                   password=self.password)

        warning_msg = self.service_closure_resp['content']['serviceclosure']['messages']['PlayMoneyUserBlockedMessage']
        if self.site.service_closure.has_warning_message_text(text=warning_msg):
            raise GVCException('Service Closure is not enabled on GVC side')
        else:
            self.__class__.closure_details = self.site.service_closure.items_as_ordered_dict
            self.assertTrue(self.closure_details, msg='List of products isn\'t available to the user')
            for product_name, product in self.closure_details.items():
                self.assertTrue(product.close_button.is_displayed(),
                                msg=f'"{product_name}" product doesn\'t have separate "CLOSE" button')
            self.assertTrue(self.site.service_closure.close_all_button.is_displayed(),
                            msg=f'There is no a "CLOSE ALL" button')

    def test_004_click_close__button_for_any_of_the_products(self):
        """
        DESCRIPTION: Click 'CLOSE'  button for any of the products.
        EXPECTED: User is taken to the page with the detailed information about service closure.
        """
        self.__class__.product_name, product = list(self.closure_details.items())[0]
        product.close_button.click()
        selected_product = self.site.service_closure.selected_product
        self.assertEqual(selected_product, self.product_name,
                         msg=f'User isn\'t taken to the page with the detailed information, selected product is "{selected_product}"')

    def test_005_select_any_duration_radio_button(self):
        """
        DESCRIPTION: Select any 'Duration' radio button.
        EXPECTED: Duration is selected.
        """
        duration_options = self.site.service_closure.duration_options.items_as_ordered_dict
        self.assertTrue(duration_options, msg='Duration radio buttons aren\'t displayed')
        duration_name, duration = list(duration_options.items())[0]
        duration.click()
        self.assertTrue(duration.is_checked(), msg=f'Duration "{duration_name}" is not selected')

    def test_006_select_any_reason_for_closure_radio_button(self):
        """
        DESCRIPTION: Select any 'Reason for closure' radio button.
        EXPECTED: Reason is selected.
        """
        reason_options = self.site.service_closure.reason_options.items_as_ordered_dict
        self.assertTrue(reason_options, msg='Reason radio buttons aren\'t displayed')
        reason_name, reason = list(reason_options.items())[0]
        reason.click()
        self.assertTrue(reason.is_checked(), msg=f'Reason "{reason_name}" is not selected')

    def test_007_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button.
        EXPECTED: User is taken to service closure confirmation page.
        """
        self.site.service_closure.continue_button.click()

        selected_product = self.site.service_closure.selected_product
        self.assertEqual(selected_product, self.product_name,
                         msg=f'User isn\'t taken to the page with the detailed information, selected product is "{selected_product}"')

    def test_008_click_close_product_name(self):
        """
        DESCRIPTION: Click 'CLOSE {PRODUCT_NAME}'
        EXPECTED: User is taken back to the page with the list of available products.
        EXPECTED: Information message says: Succesfully closed: {PRODUCT_NAME}.
        EXPECTED: Product is not listed in the list.
        """
        self.site.service_closure.close_button.click()
        available_products = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(available_products, msg='There are no list of available products on the page')
        self.assertNotIn(self.product_name, available_products.keys(),
                         msg=f'Product "{self.product_name}" is found in the list "{available_products.keys()}"')

        inf_msg_text = self.site.service_closure.info_message.text
        self.__class__.status_msg = self.service_closure_resp['content']['serviceclosureconfirmation']['messages']['CloseSuccessMessage']
        expected_status_msg = self.status_msg.format(self.product_name)
        self.assertEqual(inf_msg_text, expected_status_msg,
                         msg=f'Actual information message is: "{inf_msg_text}", but expected: "{expected_status_msg}"')

    def test_009_click_close_all_button_at_the_bottom(self):
        """
        DESCRIPTION: Click 'CLOSE ALL' button at the bottom.
        EXPECTED: User is taken to the page with the detailed information about service closure. It lists all the products about to be closed.
        """
        available_products = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(available_products, msg='Reason radio buttons aren\'t displayed')
        self.__class__.list_products_names = [x for x in list(available_products.keys()) if x]
        self.site.service_closure.close_all_button.click()

    def test_010_select_any_duration_and_reason_for_closure_radio_buttons(self):
        """
        DESCRIPTION: Select any 'Duration' and 'Reason for closure' radio buttons.
        EXPECTED: Duration and reason are selected.
        """
        self.test_005_select_any_duration_radio_button()
        self.test_006_select_any_reason_for_closure_radio_button()

    def test_011_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button.
        EXPECTED: User is taken to service closure confirmation page.
        """
        self.site.service_closure.continue_button.click()

    def test_012_click_close_my_account_button(self):
        """
        DESCRIPTION: Click 'CLOSE MY ACCOUNT' button.
        EXPECTED: User is taken back to the page with the list of available products.
        EXPECTED: Information message says: Successfully closed: {LIST OF ALL CLOSED PRODUCTS}.
        """
        self.site.service_closure.close_button.click()
        inf_msg_text = self.site.service_closure.info_message.text
        expected_status_msg = self.status_msg.format(', '.join(self.list_products_names))
        self.assertEqual(inf_msg_text, expected_status_msg,
                         msg=f'Actual information message is: "{inf_msg_text}", but expected: "{expected_status_msg}"')
