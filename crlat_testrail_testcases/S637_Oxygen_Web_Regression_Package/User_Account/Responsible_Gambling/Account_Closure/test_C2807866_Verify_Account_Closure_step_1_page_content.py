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
class Test_C2807866_Verify_Account_Closure_step_1_page_content(Common):
    """
    TR_ID: C2807866
    NAME: Verify Account Closure step 1 page content
    DESCRIPTION: This test case verifies Account Closure step 1 page content
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C9698207](https://ladbrokescoral.testrail.com/index.php?/cases/view/9698207)
    DESCRIPTION: Desktop - [C9698072](https://ladbrokescoral.testrail.com/index.php?/cases/view/C9698072)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    """
    keep_browser_open = True

    def test_001_verify_account_closure_step_1_page_content(self):
        """
        DESCRIPTION: Verify Account Closure Step 1 page content
        EXPECTED: Account Closure Step 1 page consists of:
        EXPECTED: * 'Back' button and 'Account Closure' header
        EXPECTED: * 'What would you like to do?' text message
        EXPECTED: * 'Closure Reason' drop-down
        EXPECTED: * 'CONTINUE' and 'CANCEL' buttons
        """
        pass

    def test_002_verify_cancel_button(self):
        """
        DESCRIPTION: Verify 'CANCEL' button
        EXPECTED: 'CANCEL' button is active and clickable by default
        """
        pass

    def test_003_verify_continue_button(self):
        """
        DESCRIPTION: Verify 'CONTINUE' button
        EXPECTED: 'CONTINUE' button is disabled and not clickable by default
        """
        pass

    def test_004_verify_closure_reason_drop_down(self):
        """
        DESCRIPTION: Verify 'Closure Reason' drop-down
        EXPECTED: * There is no predefined reason selected in the drop-down
        EXPECTED: * 'Please select an option' text is displayed within the drop-down
        """
        pass

    def test_005_clicktap_closure_reason_drop_down_and_verify_its_content(self):
        """
        DESCRIPTION: Click/tap 'Closure Reason' drop-down and verify its content
        EXPECTED: 'Closure Reason' drop-down consists of following reasons:
        EXPECTED: * 'Do not have time to gamble'
        EXPECTED: * 'Not interested in online gambling anymore'
        EXPECTED: * 'Not happy with your product'
        EXPECTED: * 'Not happy with your offers'
        EXPECTED: * 'I now use another provider'
        EXPECTED: * 'Prefer not to specify'
        """
        pass

    def test_006_clicktap_back_button(self):
        """
        DESCRIPTION: Click/tap 'Back' button
        EXPECTED: The user is navigated to 'Responsible Gambling' page
        """
        pass

    def test_007_clicktap_i_want_to_close_my_account_link_within_account_closure_section(self):
        """
        DESCRIPTION: Click/tap 'I want to close my Account' link within 'Account Closure' section
        EXPECTED: Verify Account Closure Step 1 page is opened again
        """
        pass

    def test_008_clicktap_cancel_button(self):
        """
        DESCRIPTION: Click/tap 'CANCEL' button
        EXPECTED: The user is navigated to 'Responsible Gambling' page
        """
        pass
