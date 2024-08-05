import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
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
        pass

    def test_002_click_the_cancel_button(self):
        """
        DESCRIPTION: Click the **Cancel** button
        EXPECTED: Account closure action is cancelled.
        EXPECTED: The user is redirected back to the **Gambling Controls** page with **Deposit Limits** option highlighted by default.
        """
        pass
