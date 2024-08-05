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
class Test_C2841193_Verify_Account_Closure_step_2_page_content(Common):
    """
    TR_ID: C2841193
    NAME: Verify Account Closure step 2 page content
    DESCRIPTION: This test case verifies Account Closure step 2 page content
    DESCRIPTION: **Auto tests:**
    DESCRIPTION: Mobile - [C3224786](https://ladbrokescoral.testrail.com/index.php?/cases/view/3224786)
    DESCRIPTION: Desktop - [C3233951](https://ladbrokescoral.testrail.com/index.php?/cases/view/3233951)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    PRECONDITIONS: * Select any option from 'Closure Reason' drop-down and click/tap 'CONTINUE' button
    """
    keep_browser_open = True

    def test_001_verify_account_closure_step_2_page_content(self):
        """
        DESCRIPTION: Verify Account Closure Step 2 page content
        EXPECTED: Account Closure Step 2 page consists of:
        EXPECTED: * 'Back' button and 'Account Closure' header
        EXPECTED: * The next text message:
        EXPECTED: 'You are about to close your account' -in bold
        EXPECTED: 'Please confirm with your account'
        EXPECTED: * 'Password' field and 'Show' option within the it
        EXPECTED: * The next text message:
        EXPECTED: 'Consequences of Account Closure - in bold
        EXPECTED: You will no longer to be able to:
        EXPECTED: Deposit funds in your account
        EXPECTED: Bet with real or play money stakes
        EXPECTED: After Confirmation - in bold
        EXPECTED: You should close any open gaming sessions
        EXPECTED: You will not be able to add funds to open gaming
        EXPECTED: session'
        EXPECTED: * 'CONTINUE' and 'CANCEL' buttons
        """
        pass

    def test_002_verify_password_field(self):
        """
        DESCRIPTION: Verify 'Password' field
        EXPECTED: * 'Password' field is empty by default
        EXPECTED: * 'Password' placeholder is displayed within field
        """
        pass

    def test_003_verify_continue_button(self):
        """
        DESCRIPTION: Verify 'CONTINUE' button
        EXPECTED: 'CONTINUE' button is disabled and not clickable by default
        """
        pass

    def test_004_clicktap_back_button(self):
        """
        DESCRIPTION: Click/tap 'Back' button
        EXPECTED: * User is navigated to Account Closure Step 1 page
        EXPECTED: * 'Closure Reason' drop-down has no selected reason
        """
        pass

    def test_005_select_any_option_in_closure_reason_drop_down_and_clicktap_continue_button_on_account_closure_step_1_page(self):
        """
        DESCRIPTION: Select any option in 'Closure Reason' drop-down and click/tap 'CONTINUE' button on Account Closure Step 1 page
        EXPECTED: Account Closure Step 2 page is opened again
        """
        pass

    def test_006_clicktap_cancel_button(self):
        """
        DESCRIPTION: Click/tap 'CANCEL' button
        EXPECTED: The user is navigated to 'Responsible Gambling' page
        """
        pass
