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
class Test_C2807966_HLSTG2_Verify_Account_Closure_functionality(Common):
    """
    TR_ID: C2807966
    NAME: [HL][STG2] Verify Account Closure functionality
    DESCRIPTION: This test case verifies Account Closure functionality
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    PRECONDITIONS: * To check response open DEvTools -> Network -> WS -> Frames -> select request to Open API
    """
    keep_browser_open = True

    def test_001_clicktap_i_want_to_close_my_account_link_within_account_closure_section(self):
        """
        DESCRIPTION: Click/tap 'I want to close my Account' link within 'Account Closure' section
        EXPECTED: * Account Closure step 1 page is opened
        EXPECTED: * 'Closure Reason' drop-down is present within the page
        EXPECTED: * CONTINUE' button on Account Closure step 1 page is disabled
        """
        pass

    def test_002_choose_any_option_from_closure_reason_drop_down(self):
        """
        DESCRIPTION: Choose any option from 'Closure Reason' drop-down
        EXPECTED: * Option is selected and displayed within 'Closure Reason' drop-down
        EXPECTED: * 'CONTINUE' button becomes enabled
        """
        pass

    def test_003_clicktap_continue_button(self):
        """
        DESCRIPTION: Click/tap 'CONTINUE' button
        EXPECTED: * Account Closure step 2 page is opened
        EXPECTED: * 'Password' field is present within the page
        EXPECTED: * CONTINUE' button on Account Closure step 2 page is disabled
        """
        pass

    def test_004_enter_valid_password_in_password_field(self):
        """
        DESCRIPTION: Enter valid password in 'Password' field
        EXPECTED: * 'Password' field is populated with the value
        EXPECTED: * Characters within are hidden by default
        EXPECTED: * No error message is displayed
        EXPECTED: * 'CONTINUE' button becomes enabled
        """
        pass

    def test_005_clicktap_show_option_within_password_field(self):
        """
        DESCRIPTION: Click/tap 'SHOW' option within 'Password' field
        EXPECTED: * Characters within the 'Password' field becomes visible
        EXPECTED: * 'SHOW' option becomes 'HIDE'
        """
        pass

    def test_006_clicktap_hide_option(self):
        """
        DESCRIPTION: Click/tap 'HIDE' option
        EXPECTED: * Characters within the 'Password' field are no more visible
        EXPECTED: * 'HIDE' option becomes 'SHOW'
        """
        pass

    def test_007_clicktap_continue_button(self):
        """
        DESCRIPTION: Click/tap 'CONTINUE' button
        EXPECTED: * 35574 request **password: "entered_pas"** parameter is sent to Open API in WS to validate user`s pass
        EXPECTED: * 'Accout Closure' confirmation pop-up is shown
        EXPECTED: * 'Confirm' checkbox is present on pop-up
        EXPECTED: * 'Please, select the box to confirm' error message is displayed on pop-up
        """
        pass

    def test_008_check_confirm_checkbox(self):
        """
        DESCRIPTION: Check 'Confirm' checkbox
        EXPECTED: * 'YES' button becomes enabled
        EXPECTED: * 'Please, select the box to confirm' error message disappears
        """
        pass

    def test_009_clicktap_yes_button(self):
        """
        DESCRIPTION: Click/tap 'YES' button
        EXPECTED: * 35544 request with
        EXPECTED: **Account_Closed_By_Player=true** tag is sent to Open API in WS
        EXPECTED: * User is logged out and navigated to Homepage automatically
        EXPECTED: * 'Your account is closed' confirmation pop-up is displayed
        EXPECTED: * 'OK' button is present on 'Your account is closed' confirmation pop-up
        """
        pass

    def test_010_clicktap_ok_button(self):
        """
        DESCRIPTION: Click/tap 'OK' button
        EXPECTED: * 'Your account is closed' confirmation pop-up is closed
        """
        pass
