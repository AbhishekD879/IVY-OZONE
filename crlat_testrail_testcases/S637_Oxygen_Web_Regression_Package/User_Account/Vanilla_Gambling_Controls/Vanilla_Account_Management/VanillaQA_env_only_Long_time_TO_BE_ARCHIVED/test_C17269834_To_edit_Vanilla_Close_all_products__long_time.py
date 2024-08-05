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
class Test_C17269834_To_edit_Vanilla_Close_all_products__long_time(Common):
    """
    TR_ID: C17269834
    NAME: {To edit} [Vanilla] Close all products - long time
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and DON'T have any closed products
    PRECONDITIONS: User opens My Account -> Settings -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'I'd like to close my account' option and clicks the Continue button
    """
    keep_browser_open = True

    def test_001_click_the_close_all_button(self):
        """
        DESCRIPTION: Click the 'Close all' button
        EXPECTED: The confirmation screen of Service closure is displayed with closure duration and reason selections.
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
        """
        pass

    def test_006_click_the_close_my_account_button(self):
        """
        DESCRIPTION: Click the 'Close my account' button
        EXPECTED: All products are closed for the selected period of time.
        EXPECTED: A confirmation message:
        EXPECTED: 'Successfully closed: <prod1>, ...,<prodn>'
        EXPECTED: is displayed on the Service Closure page.
        EXPECTED: Under the confirmation, the list of products with states (all should be closed) is displayed.
        EXPECTED: There's the 'Reopen all' button under the list of products.
        """
        pass
