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
class Test_C2854693_Verify_Confirmation_of_Account_Closure_pop_up(Common):
    """
    TR_ID: C2854693
    NAME: Verify 'Confirmation of Account Closure' pop-up
    DESCRIPTION: This test case verifies 'Confirmation of Account Closure' pop-up window
    DESCRIPTION: **Autotests:**
    DESCRIPTION: Mobile - [C8141085](https://ladbrokescoral.testrail.com/index.php?/cases/view/8141085)
    DESCRIPTION: Desktop - [8141145](https://ladbrokescoral.testrail.com/index.php?/cases/view/8141145)
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    PRECONDITIONS: * Select any option from 'Closure Reason' drop-down and click/tap 'CONTINUE' button on Account Closure step 1 page
    PRECONDITIONS: * Enter valid password in 'Password' field on Account Closure step 2 page
    """
    keep_browser_open = True

    def test_001_clicktap_continue_button_on_account_closure_step_2_page(self):
        """
        DESCRIPTION: Click/tap 'CONTINUE' button on Account Closure step 2 page
        EXPECTED: Confirmation of account Closure" pop-up is shown
        """
        pass

    def test_002_verify_confirmation_pop_up(self):
        """
        DESCRIPTION: Verify confirmation pop-up
        EXPECTED: The confirmation pop-up consists of the next elements:
        EXPECTED: * 'Confirmation of account closure' header
        EXPECTED: *  The next hardcoded text message:
        EXPECTED: "If you don't feel that Account Closure is the correct option for you please try 'TimeOut' or 'Reality Check'',
        EXPECTED: where 'TimeOut', 'Reality Check' - hyperlinks
        EXPECTED: * Checkbox and "I confirm that I wish to Close my Coral Account" text
        EXPECTED: * 'Please, select the box to confirm' error message
        EXPECTED: * 'CANCEL' and 'YES' buttons
        """
        pass

    def test_003_verify_yes_button(self):
        """
        DESCRIPTION: Verify 'YES' button
        EXPECTED: 'YES' button is disabled by default
        """
        pass

    def test_004_clicktap_cancel_button(self):
        """
        DESCRIPTION: Click/tap 'CANCEL' button
        EXPECTED: * Confirmation of account Closure" pop-up is closed
        EXPECTED: * User stays on Account Closure step 2 page
        """
        pass

    def test_005_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step #1
        EXPECTED: 
        """
        pass

    def test_006_clicktap_on_timeout_link(self):
        """
        DESCRIPTION: Click/tap on 'TimeOut' link
        EXPECTED: * Confirmation of account Closure" pop-up is closed
        EXPECTED: * User is navigated to 'Period and Reason' page
        """
        pass

    def test_007_clicktap_back_button(self):
        """
        DESCRIPTION: Click/tap 'Back' button
        EXPECTED: The user navigates to Account Closure step 2 page
        """
        pass

    def test_008_enter_valid_password_password_field_and_repeat_step_1(self):
        """
        DESCRIPTION: Enter valid password 'Password' field and repeat step #1
        EXPECTED: 
        """
        pass

    def test_009_clicktap_on_reality_checks_link(self):
        """
        DESCRIPTION: Click/tap on 'Reality Checks' link
        EXPECTED: * Confirmation of account Closure" pop-up is closed
        EXPECTED: * User is navigated to 'Limits' page
        """
        pass

    def test_010_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step #7
        EXPECTED: 
        """
        pass
