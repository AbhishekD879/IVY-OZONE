import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.gvc_exeption import GVCException


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
@pytest.mark.portal_only_test
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C17277681_To_edit_Vanilla_Verify_Account_Closure_long_time_page_3(BaseUserAccountTest):
    """
    TR_ID: C17277681
    NAME: {To edit} [Vanilla] Verify Account Closure long time page 3
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and DON'T have any closed products
    PRECONDITIONS: User opens My Account -> Settings -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'I'd like to close my account' option, selects which product to close, selects the duration & reason for closure and clicks the Continue button
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: App is loaded
        PRECONDITIONS: User is logged in and DON'T have any closed products
        PRECONDITIONS: User opens My Account -> Settings -> Gambling Controls -> Account Closure
        PRECONDITIONS: User selects 'I'd like to close my account' option, selects which product to close, selects the duration & reason for closure and clicks the Continue button
        """
        username = tests.settings.default_username
        password = tests.settings.default_password

        self.gambling_controls_data = self.gvc_wallet_user_client.get_gambling_controls_data(username=username,
                                                                                             password=password)
        if not self.gambling_controls_data:
            raise GVCException('Gambling Controls page is not configured on GVC side')

        self.site.login(username=username)

        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(item_name=self.site.window_client_config.gambling_controls_title)
        self.assertTrue(self.site.gambling_controls.is_displayed(timeout=10),
                        msg=f'"Gambling Controls" page is not opened')
        account_closure_and_reopening = next((item for item in self.gambling_controls_data.get('items', {})
                                              if item.get('targetPageUrl', '').endswith('accountclosure')), None)
        if not account_closure_and_reopening:
            raise GVCException('Cannot find "Account Closure & Reopening" in Gambling Controls')
        self.account_closure_and_reopening_option = account_closure_and_reopening.get('title')
        result = self.site.gambling_controls.select_option(option_name=self.account_closure_and_reopening_option)
        self.assertTrue(result,
                        msg=f'"{self.account_closure_and_reopening_option}" option, on "Gambling Controls" page is not selected after click')
        self.site.gambling_controls.choose_button.click()
        self.assertTrue(self.site.account_closure.is_displayed(), msg='Account Closure page is not opened')
        account_closure_data = self.gvc_wallet_user_client.get_account_closure_data(username=username,
                                                                                    password=password)
        if not account_closure_data:
            raise GVCException('Account Closure options are not configured on GVC side')

        self.account_options = [i['title'] for i in account_closure_data['items']]
        self.site.account_closure.select_option(option_name=self.account_options[0])
        continue_button = self.site.account_closure.continue_button
        continue_button.click()
        self.assertTrue(self.site.service_closure.is_displayed(), msg=f'"Service Closure" page is not opened')

    def test_001_click_the_close_products_button(self):
        """
        DESCRIPTION: Click the Close Products button
        EXPECTED: The chosen product(s) are closed for the selected duration.
        EXPECTED: A confirmation message is displayed on the Service Closure page.
        EXPECTED: Under the confirmation,  the list of products with states (open/closed) is displayed.
        """
        self.closure_details = self.site.service_closure.items_as_ordered_dict
        self.product_name, product = list(self.closure_details.items())[0]
        product.close_button.click()
        selected_product = self.site.service_closure.selected_product
        self.assertEqual(selected_product, self.product_name,
                         msg=f'User isn\'t taken to the page with the detailed information, selected product is "{selected_product}"')
