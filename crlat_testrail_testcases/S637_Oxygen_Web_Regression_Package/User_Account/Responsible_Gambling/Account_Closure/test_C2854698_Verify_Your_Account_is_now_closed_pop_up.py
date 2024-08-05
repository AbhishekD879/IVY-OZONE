import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.user_account
@vtest
class Test_C2854698_Verify_Your_Account_is_now_closed_pop_up(Common):
    """
    TR_ID: C2854698
    NAME: Verify 'Your Account is now closed' pop-up
    DESCRIPTION: This test case verifies 'Your Account is now closed' pop-up
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    PRECONDITIONS: * Select any option from 'Closure Reason' drop-down and click/tap 'CONTINUE' button on Account Closure step 1 page
    PRECONDITIONS: * Enter valid password in 'Password' field and click/tap 'CONTINUE' button on Account Closure step 2 page
    PRECONDITIONS: * Check 'Confirm' checkbox and click/tap 'YES' button on 'Confirmation of Account Closure' pop-up
    """
    keep_browser_open = True

    def test_001_verify_your_account_is_now_closed_pop_up(self):
        """
        DESCRIPTION: Verify 'Your Account is now closed' pop-up
        EXPECTED: 'Your Account is now closed' pop-up consists of the next elements:
        EXPECTED: * 'Your account is now closed' title
        EXPECTED: * The next hardcoded text message:
        EXPECTED: "Your account closure request was successfully submitted and you have been logged out of your account.
        EXPECTED: If you wish to reactivate your account in future please log and follow the instructions."
        EXPECTED: * 'OK' button
        """
        pass

    def test_002_clicktap_ok_button(self):
        """
        DESCRIPTION: Click/tap 'OK' button
        EXPECTED: 'Your Account is now closed' pop-up is closed
        """
        pass
