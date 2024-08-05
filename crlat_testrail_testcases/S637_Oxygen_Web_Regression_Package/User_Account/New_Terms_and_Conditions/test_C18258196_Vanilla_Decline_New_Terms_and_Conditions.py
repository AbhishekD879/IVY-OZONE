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
class Test_C18258196_Vanilla_Decline_New_Terms_and_Conditions(Common):
    """
    TR_ID: C18258196
    NAME: [Vanilla] Decline New Terms and Conditions
    DESCRIPTION: This test case verifies declining new terms and conditions.
    PRECONDITIONS: Terms & Conditions have been changed
    PRECONDITIONS: NOTE: if other pop-up messages are expected after log in then the order of pop-up appearing should be the following:
    PRECONDITIONS: Terms and Conditions -> Verify Your Account (Netverify) -> Deposit Limits -> Quick Deposit
    """
    keep_browser_open = True

    def test_001_open_application_and_tab_login_button(self):
        """
        DESCRIPTION: Open application and Tab "LOGIN' button
        EXPECTED: 
        """
        pass

    def test_002_complete_username_and_password_with_valid_credentials_and_tab_log_in_button(self):
        """
        DESCRIPTION: Complete username and password with valid credentials and tab 'LOG IN' button
        EXPECTED: 
        """
        pass

    def test_003_verify_pop_up_that_is_shown(self):
        """
        DESCRIPTION: Verify pop-up that is shown
        EXPECTED: 'General Terms and Conditions acceptance' page is open that contains:
        EXPECTED: * Information that 'You must accept the TAC before proceeding!'.
        EXPECTED: * Information that some changes have been done with link to 'General Terms and Conditions'
        EXPECTED: * 'ACCEPT' button
        EXPECTED: * Close button 'X' in the header
        """
        pass

    def test_004_click_x_button_to_close_tc_pop_up(self):
        """
        DESCRIPTION: Click 'X' button to close T&C pop-up
        EXPECTED: * user is redirected to main page
        EXPECTED: * user is logged out
        """
        pass
