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
class Test_C18258195_Vanilla_Accept_New_Terms_and_Conditions(Common):
    """
    TR_ID: C18258195
    NAME: [Vanilla] Accept New Terms and Conditions
    DESCRIPTION: This test case verifies accepting new terms and conditions.
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
        EXPECTED: User is logged in
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

    def test_004_tap_general_terms_and_conditions_button(self):
        """
        DESCRIPTION: Tap 'General Terms and Conditions' button
        EXPECTED: Terms & Conditions are opened in a separate browser tab
        """
        pass

    def test_005_when_tc_pop_up_appears_accept_the_changes(self):
        """
        DESCRIPTION: When T&C pop-up appears 'ACCEPT' the changes
        EXPECTED: * User is redirected to main page
        EXPECTED: * User is still logged in
        """
        pass

    def test_006_place_any_bet_while_logged_in(self):
        """
        DESCRIPTION: Place any bet while logged in
        EXPECTED: It is possible to place a bet if Terms and Conditions are accepted.
        """
        pass