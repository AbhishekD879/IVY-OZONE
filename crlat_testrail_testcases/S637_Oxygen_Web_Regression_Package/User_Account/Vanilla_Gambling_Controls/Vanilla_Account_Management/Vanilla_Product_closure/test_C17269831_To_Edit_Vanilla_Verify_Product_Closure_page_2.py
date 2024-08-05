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
class Test_C17269831_To_Edit_Vanilla_Verify_Product_Closure_page_2(Common):
    """
    TR_ID: C17269831
    NAME: [To Edit] [Vanilla] Verify Product Closure page 2
    DESCRIPTION: This test case verifies the page after selecting the product to close with 'I want to close my account or sections of it' option
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and **DON'T** have any closed products
    PRECONDITIONS: User opens My Account -> Gambling Controls -> Account Closure & Reopening
    PRECONDITIONS: User selects 'I want to close my account or sections of it' option and selects which product to close
    """
    keep_browser_open = True

    def test_001_click_the_close_button(self):
        """
        DESCRIPTION: Click the **Close** button
        EXPECTED: The confirmation screen of product closure is displayed:
        EXPECTED: - the title of the page is ** Account Closure**,
        EXPECTED: - list of selected products (e.g. Casino, Poker, Sports),
        EXPECTED: - **Consequences of account closure** with bulletpoints telling the user what would happen after closure,
        EXPECTED: - **Reopening** section with bulletpoints telling the user that their account would be reopened automatically after selected duration expires and information that they still have an option to reopen the product before specified date,
        EXPECTED: - **Duration** with options: 1 week/ 1 month/ 3 months/ 6 months / until with inputs for day, month and year / indefinite closure
        EXPECTED: - **Reason for closure** with a few radio button selections,
        EXPECTED: - "Continue" button,
        EXPECTED: - "Cancel" button
        """
        pass

    def test_002_verify_continue_button(self):
        """
        DESCRIPTION: Verify **Continue** button
        EXPECTED: **Continue** button is disabled
        """
        pass

    def test_003_select_account_closure_duration_time(self):
        """
        DESCRIPTION: Select account closure duration time
        EXPECTED: **Continue** button is disabled
        """
        pass

    def test_004_select_closure_reason(self):
        """
        DESCRIPTION: Select closure reason
        EXPECTED: **Continue** button becomes enabled
        """
        pass

    def test_005_click_the_cancel_button(self):
        """
        DESCRIPTION: Click the **CANCEL** button
        EXPECTED: Account closure action is cancelled.
        EXPECTED: The user is redirected back to the **Gambling Controls** page with **Deposit Limits** option highlighted by default.
        """
        pass
