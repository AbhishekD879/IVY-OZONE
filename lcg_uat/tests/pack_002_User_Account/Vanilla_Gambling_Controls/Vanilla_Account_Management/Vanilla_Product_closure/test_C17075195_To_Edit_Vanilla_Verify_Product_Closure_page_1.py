import pytest
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C17075195_To_Edit_Vanilla_Verify_Product_Closure_page_1(Common):
    """
    TR_ID: C17075195
    NAME: [To Edit] [Vanilla] Verify Product Closure  page 1
    DESCRIPTION: This test case verifies the page after selecting 'I want to close my account or sections of it' option
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. User is logged in and have a closed product
    PRECONDITIONS: 3. User opens My Account -> Gambling Controls -> Account Closure & Reopening
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: User should be logged in
        """
        self.site.login()
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(item_name=vec.bma.GAMBLING_CONTROLS.upper())
        self.site.wait_content_state_changed()
        self.site.gambling_controls_page.select_option(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION)
        self.site.gambling_controls_page.choose_button.click()

    def test_001_select_i_want_to_close_my_account_or_sections_of_it_option(self):
        """
        DESCRIPTION: Select 'I want to close my account or sections of it' option
        EXPECTED: User is redirected to **Account Closure** page with:
        EXPECTED: - **Account Closure** header,
        EXPECTED: - message:
        EXPECTED: ___Control which sections of your account should be accessible through the options below.___,
        EXPECTED: - products list (e.g. Casino, Poker, Sports),
        EXPECTED: - button **CLOSE ALL** to close all products at once
        """
        options = self.site.account_closure.items_as_ordered_dict.get(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1)
        options.click()
        self.site.account_closure.continue_button.click()
        self.site.wait_content_state_changed()
        section_message = self.site.service_closure.control_section_message
        self.assertEqual(section_message, vec.account.ACCOUNT_CLOSURE_CONTROL_SECTION_MESSAGE,
                         msg=f'Actual Message:"{section_message}" is not same as'
                             f'Expected Message:"{vec.account.ACCOUNT_CLOSURE_CONTROL_SECTION_MESSAGE}"')

    def test_002_verify_products_list(self):
        """
        DESCRIPTION: Verify products list
        EXPECTED: There are:
        EXPECTED: - **CLOSE** button on the right hand side of each product,
        EXPECTED: - **Current status** of a product under each option with the label **open** and **the green dot icon** on the left hand side of the label
        """
        closure_details = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(closure_details, msg='List of products isn\'t available to the user')
        products_list = list(closure_details.keys())
        expected_product_list = list(vec.account.EXPECTED_PRODUCT_LIST)
        self.assertCountEqual(products_list, expected_product_list,
                              msg=f'Actual list: "{products_list}" is not same as'
                                  f'Expected list: "{expected_product_list}".')

        for product_name, product in closure_details.items():
            self.assertGreater(product.close_button.location['x'],
                               product.play_button.location['x'],
                               msg=f'"close" button is not right side of "{product_name}"')
            self.assertTrue(product.play_button_sign,
                            msg=f'"Play button" symbol is not on left side of "open"')
            self.assertEqual(product.current_status, vec.account.CURRENT_STATUS,
                             msg=f'Actual Status: "{product.current_status}" is not same as'
                                 f'Expected status: "{vec.account.CURRENT_STATUS}".')
        self.assertTrue(self.site.service_closure.close_all_button.is_displayed(),
                        msg=f'There is no a "CLOSE ALL" button')
