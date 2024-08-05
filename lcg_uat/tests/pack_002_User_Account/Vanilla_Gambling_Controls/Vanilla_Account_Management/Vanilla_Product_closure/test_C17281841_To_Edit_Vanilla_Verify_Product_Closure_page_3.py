import pytest
import tests
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.portal_only_test
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C17281841_To_Edit_Vanilla_Verify_Product_Closure_page_3(Common):
    """
    TR_ID: C17281841
    NAME: [To Edit] [Vanilla] Verify Product Closure page 3
    DESCRIPTION: This test case verifies the 2nd page after selecting the product to close with 'I want to close some/all products' option
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and **DON'T** have any closed products
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure & Reopening
    PRECONDITIONS: User selects 'I want to close my account or sections of it' option, selects which product to close, selects the duration & reason for closure
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
        options = self.site.account_closure.items_as_ordered_dict.get(vec.bma.ACCOUNT_CLOSURE_AND_REOPENING_OPTION_1)
        options.click()

    def test_001_click_the_continue_button(self):
        """
        DESCRIPTION: Click the **Continue** button
        EXPECTED: The confirmation screen of product closure is displayed:
        EXPECTED: - the title of the page is **Account Closure**,
        EXPECTED: - under the title there's a line:
        EXPECTED: ___You have selected to close the following product(s) until___ ___<selectedDate>, <time>, after which they will be___ ___reopened___,
        EXPECTED: - list of selected products (e.g. Casino, Poker, Sports),
        EXPECTED: - **Consequences of account closure** with bulletpoints telling the user what would happen after closure,
        EXPECTED: - **After confirmation** section with bulletpoints telling the user what will happen after closure in detail,
        EXPECTED: - "Continue" button,
        EXPECTED: - "Cancel" button
        """
        self.site.account_closure.continue_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        closure_details = self.site.service_closure.items_as_ordered_dict
        self.assertTrue(closure_details, msg='List of products isn\'t available to the user')
        products_list = list(closure_details.keys())
        expected_product_list = list(vec.account.EXPECTED_PRODUCT_LIST)
        self.assertCountEqual(products_list, expected_product_list,
                              msg=f'Actual list: "{products_list}" is not same as'
                                  f'Expected list: "{expected_product_list}".')
        product = list(closure_details.values())[0]
        product.close_button.click()
        consequence1 = self.site.service_closure.consequences.consequences_list[0].text
        consequence2 = self.site.service_closure.consequences.consequences_list[1].text
        self.assertEqual(consequence1, vec.bma.SERVICE_CLOSURE_CONSEQUENCES_1,
                         msg=f'Actual: "{consequence1}" is not same as Expected: "{vec.bma.SERVICE_CLOSURE_CONSEQUENCES_1}"')
        self.assertEqual(consequence2, vec.bma.SERVICE_CLOSURE_CONSEQUENCES_2,
                         msg=f'Actual: "{consequence2}" is not same as Expected: "{vec.bma.SERVICE_CLOSURE_CONSEQUENCES_2}"')
        reopening1 = self.site.service_closure.reopening.reopening_list[0].text
        reopening2 = self.site.service_closure.reopening.reopening_list[1].text
        self.assertEqual(reopening1, vec.bma.SERVICE_CLOSURE_REOPENING_1,
                         msg=f'Actual: "{reopening1}" is not same as Expected: "{vec.bma.SERVICE_CLOSURE_REOPENING_1}"')
        self.assertEqual(reopening2, vec.bma.SERVICE_CLOSURE_REOPENING_2,
                         msg=f'Actual: "{reopening2}" is not same as Expected: "{vec.bma.SERVICE_CLOSURE_REOPENING_2}"')
        self.assertTrue(self.site.service_closure.continue_button.is_displayed(),
                        msg='"Continue button" is not displayed')
        self.assertTrue(self.site.service_closure.cancel_button.is_displayed(),
                        msg='"Cancel button is not displayed"')

    def test_002_click_the_cancel_button(self):
        """
        DESCRIPTION: Click the **Cancel** button
        EXPECTED: Account closure action is cancelled.
        EXPECTED: The user is redirected back to the **Gambling Controls** page with **Deposit Limits** option highlighted by default.
        """
        self.site.service_closure.cancel_button.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/gamblingcontrols'.replace('beta2', 'beta')
        wait_for_result(lambda: self.device.get_current_url() == expected_url, name='Page to be loaded', timeout=40)
        page_url = self.device.get_current_url()
        self.assertEqual(page_url, expected_url,
                         msg=f'"Gambling Controls" page is not found. Page url is "{page_url}" instead of "{expected_url}"')
        expected_option_name = self.site.window_client_config.mobile_portal_spending_controls
        actual_option_name = self.site.gambling_controls_page.selected_option[0].name
        self.assertEqual(expected_option_name, actual_option_name,
                         msg=f'"{expected_option_name}" option, on "Gambling Controls" page is not selected by default.'
                             f'"{actual_option_name}" is selected instead.')
