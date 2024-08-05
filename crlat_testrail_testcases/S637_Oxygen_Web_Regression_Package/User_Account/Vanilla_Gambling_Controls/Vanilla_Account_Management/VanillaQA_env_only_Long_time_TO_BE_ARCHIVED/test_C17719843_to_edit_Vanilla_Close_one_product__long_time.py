import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C17719843_to_edit_Vanilla_Close_one_product__long_time(Common):
    """
    TR_ID: C17719843
    NAME: {to edit} [Vanilla] Close one product - long time
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and **DON'T** have any closed products
    PRECONDITIONS: User opens My Account -> Settings -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'I'd like to close my account' option and clicks the Continue button
    """
    keep_browser_open = True

    def test_001_click_the_close_button_of_one_of_the_open_products_eg_sports(self):
        """
        DESCRIPTION: Click the Close button of one of the open products (e.g. Sports)
        EXPECTED: The confirmation screen of Service closure is displayed with closure duration and reason selections.
        EXPECTED: Chosen product name is correctly displayed.
        """
        pass

    def test_002_verify_continue_button(self):
        """
        DESCRIPTION: Verify 'Continue' button
        EXPECTED: 'Continue' button is disabled
        """
        pass

    def test_003_select_account_closure_duration_time(self):
        """
        DESCRIPTION: Select account closure duration time
        EXPECTED: 'Continue' button is disabled
        """
        pass

    def test_004_select_closure_reason(self):
        """
        DESCRIPTION: Select closure reason
        EXPECTED: 'Continue' button is enabled
        """
        pass

    def test_005_click_the_continue_button(self):
        """
        DESCRIPTION: Click the 'Continue' button
        EXPECTED: Another confirmation screen of Service closure is displayed.
        EXPECTED: There's the 'Close <productName>' button, where <productName> is a correct name of the chosen product (e.g. Close Sports).
        """
        pass

    def test_006_click_the_close_productname_button(self):
        """
        DESCRIPTION: Click the 'Close <productName>' button
        EXPECTED: Product is closed for the selected period of time.
        EXPECTED: A confirmation message:
        EXPECTED: 'Successfully closed: <productName>'
        EXPECTED: is displayed on the Service Closure page.
        EXPECTED: Under the confirmation, the list of products with states (chosen product should be closed) is displayed.
        EXPECTED: There are 'Reopen all' and 'Close all' buttons under the list of products
        """
        pass
