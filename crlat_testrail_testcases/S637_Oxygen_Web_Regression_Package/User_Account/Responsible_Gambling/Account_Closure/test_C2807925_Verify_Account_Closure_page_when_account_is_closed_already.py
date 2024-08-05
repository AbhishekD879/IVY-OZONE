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
class Test_C2807925_Verify_Account_Closure_page_when_account_is_closed_already(Common):
    """
    TR_ID: C2807925
    NAME: Verify Account Closure page when account is closed already
    DESCRIPTION: This test case verifies Account Closure page when account is closed already
    DESCRIPTION: **Auto-tests:**
    DESCRIPTION: Mobile - [C3234084](https://ladbrokescoral.testrail.com/index.php?/cases/view/3234084)
    DESCRIPTION: Desktop - [C3233952](https://ladbrokescoral.testrail.com/index.php?/cases/view/3233952)
    PRECONDITIONS: * Load app and log in with user that has closed his account already
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    """
    keep_browser_open = True

    def test_001_verify_account_closure_page(self):
        """
        DESCRIPTION: Verify Account Closure page
        EXPECTED: Account Closure page consists of:
        EXPECTED: * 'Back' button and 'Account Closure' header
        EXPECTED: * 'You have already closed your account. If you wish to reactivate your account, please go to Reactivation.' message
        EXPECTED: where 'please go to Reactivation' - hyperlink
        EXPECTED: * 'CONTINUE' and 'CANCEL' buttons
        """
        pass

    def test_002_verify_continue_button(self):
        """
        DESCRIPTION: Verify 'CONTINUE' button
        EXPECTED: 'CONTINUE' button is always disabled and not clickable
        """
        pass

    def test_003_clicktap_please_go_to_reactivation_hyperlink(self):
        """
        DESCRIPTION: Click/tap 'please go to Reactivation' hyperlink
        EXPECTED: 'Reactivation Password' page is opened
        """
        pass
