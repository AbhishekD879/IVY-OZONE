import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.environments import constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C17075196_To_edit_Vanilla_Verify_Account_Closure_long_time_page_1(BaseUserAccountTest):
    """
    TR_ID: C17075196
    NAME: {To edit} [Vanilla] Verify Account Closure long time page 1
    DESCRIPTION: This test case verifies the page after selecting 'I'd like to close my account' option
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in and have a closed product
    PRECONDITIONS: 3. User opens My Account -> Settings -> Gambling Controls -> Account Closure
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: 1. App is loaded
        PRECONDITIONS: 2. User is logged in and have a closed product
        PRECONDITIONS: 3. User opens My Account -> Settings -> Gambling Controls -> Account Closure
        """
        user_name = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=user_name)
        self.navigate_to_page(name='en/mobileportal/gamblingcontrols')
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        self.site.account_closure.items_as_ordered_dict.get(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1).click()
        self.site.account_closure.continue_button.click()
        self.site.wait_content_state_changed()
        closure_details = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(closure_details, msg='List of products isn\'t available to the user')
        product_name, product = list(closure_details.items())[0]
        self.assertTrue(product.close_button.is_displayed(), msg='"CLOSE button" is not displayed')
        product.close_button.click()
        duration_options = self.site.service_closure.duration_options.items_as_ordered_dict
        self.assertTrue(duration_options, msg='Duration radio buttons aren\'t displayed')
        reason_options = self.site.service_closure.reason_options.items_as_ordered_dict
        self.assertTrue(reason_options, msg='Reason radio buttons aren\'t displayed')
        list(duration_options.values())[0].click()
        list(reason_options.values())[0].click()
        self.site.service_closure.continue_button.click()
        self.site.service_closure.close_button.click()
        expected_info_text = f'Successfully closed: {product_name}'
        actual_info_text = self.site.service_closure.info_message.text
        self.assertEqual(actual_info_text, expected_info_text,
                         msg=f'Actual text: "{actual_info_text}" is not same as Expected text: "{expected_info_text}"')

        self.navigate_to_page('Home')
        self.site.wait_content_state('Homepage')
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(item_name=vec.bma.GAMBLING_CONTROLS.upper())
        self.site.wait_content_state_changed()
        sleep(1)
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')

    def test_001_select_id_like_to_close_my_account_option(self, option=vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1):
        """
        DESCRIPTION: Select 'I'd like to close my account' option
        EXPECTED: User is redirected to Service Closure page with:
        EXPECTED: - 'Service Closure' header,
        EXPECTED: - message to select the product that can be made unavailable,
        EXPECTED: - products list (e.g. Casino, Poker, Sports),
        EXPECTED: - button to close all products at once
        """
        sleep(2)
        options = self.site.account_closure.items_as_ordered_dict.get(option)
        options.click()
        self.site.account_closure.continue_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        section_message = self.site.service_closure.control_section_message
        self.assertEqual(section_message, vec.account.ACCOUNT_CLOSURE_CONTROL_SECTION_MESSAGE,
                         msg=f'Actual Message:"{section_message}" is not same as'
                             f'Expected Message:"{vec.account.ACCOUNT_CLOSURE_CONTROL_SECTION_MESSAGE}"')
        self.__class__.closure_details = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(self.closure_details, msg="List of products isn't available to the user")
        products_list = list(self.closure_details.keys())
        self.assertTrue(products_list, msg='No products available')
        if option == vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1:
            self.assertTrue(self.site.service_closure.close_all_button.is_displayed(),
                            msg='"CLOSE ALL" button to close all the products at once is not displayed')

    def test_002_verify_products_list(self):
        """
        DESCRIPTION: Verify products list
        EXPECTED: There are:
        EXPECTED: - buttons on the right hand side of each product (Close button - for open products, Open button - for closed products),
        EXPECTED: - current 'Customer status' of a product under each option with text (Closed/ open) and a red dot if closed/ green dot if open,
        EXPECTED: - closure date and time (for closed products),
        EXPECTED: - date and time to reopen the product (for closed products)
        """
        for product_name, product in self.closure_details.items():
            self.assertGreater(product.close_button.location['x'],
                               product.play_button.location['x'],
                               msg=f'"CLOSE" button is not right side of "{product_name}"')
            self.assertTrue(product.play_button_sign,
                            msg=f'"Play button" symbol is not on left side of "open"')
            self.assertEqual(product.current_status, vec.account.CURRENT_STATUS,
                             msg=f'Actual Status: "{product.current_status}" is not same as'
                                 f'Expected status: "{vec.account.CURRENT_STATUS}".')
        self.device.go_back()
        self.site.wait_content_state_changed(timeout=30)
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        self.test_001_select_id_like_to_close_my_account_option(option=vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_3)
        for product_name, product in self.closure_details.items():
            self.assertGreater(product.open_button.location['x'],
                               product.locked_button.location['x'],
                               msg=f'"OPEN" button is not right side of "{product_name}"')
            self.assertTrue(product.locked_button_sign,
                            msg=f'"Locked button" symbol is not on left side of "open"')
            self.assertEqual(product.current_status, vec.account.CURRENT_STATUS_CLOSED,
                             msg=f'Actual Status: "{product.current_status}" is not same as'
                                 f'Expected status: "{vec.account.CURRENT_STATUS_CLOSED}".')
            self.assertTrue(product.closed_date_time,
                            msg=f'Date and time to reopen is not displayed for product "{product_name}"')
