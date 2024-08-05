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
class Test_C17277684_to_edit_Vanilla_Verify_Account_Closure_long_time_page_2(Common):
    """
    TR_ID: C17277684
    NAME: {to edit} [Vanilla] Verify Account Closure long time page 2
    DESCRIPTION: 
    PRECONDITIONS: App is loaded
    PRECONDITIONS: User is logged in and DON'T have any closed products
    PRECONDITIONS: User opens My Account -> Settings -> Gambling Controls -> Account Closure
    PRECONDITIONS: User selects 'I'd like to close my account' option, selects which product to close and clicks the Close button
    """
    keep_browser_open = True

    def test_001_click_the_continue_button(self):
        """
        DESCRIPTION: Click the Continue button
        EXPECTED: The confirmation screen of Service closure is displayed:
        EXPECTED: - the title of the page is Service Closure,
        EXPECTED: - the product list of selected options (e.g. Casino, Poker, Sports),
        EXPECTED: - consequences of service closure,
        EXPECTED: - account reactivation process (reopening),
        EXPECTED: - the option to select duration of self exclusion (1 week/ 1 month/ 3 months/ 6 months/ until with date selection/ indefinite)
        EXPECTED: - question about the reason for closure with some options to select,
        EXPECTED: - "Continue" button,
        EXPECTED: - "Cancel" button
        """
        pass

    def test_002_verify_continue_button(self):
        """
        DESCRIPTION: Verify Continue button
        EXPECTED: Continue button is disabled
        """
        pass

    def test_003_select_account_closure_duration_time(self):
        """
        DESCRIPTION: Select account closure duration time
        EXPECTED: Continue button is disabled
        """
        pass

    def test_004_select_closure_reason(self):
        """
        DESCRIPTION: Select closure reason
        EXPECTED: Continue button becomes enabled
        """
        pass

    def test_005_click_the_cancel_button(self):
        """
        DESCRIPTION: Click the CANCEL button
        EXPECTED: Account closure action is cancelled.
        EXPECTED: The user is redirected back to the Gambling controls page with Deposit Limits option highlighted by default.
        """
        pass
