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
class Test_C2807972_HL_STG_Verify_Account_Reactivation_functionality(Common):
    """
    TR_ID: C2807972
    NAME: [HL/STG] Verify Account Reactivation functionality
    DESCRIPTION: This test case verifies Account Reactivation functionality
    DESCRIPTION: AUTOTEST [C9240787]
    PRECONDITIONS: * User's Account is closed (Navigate to Right Menu -> My Account -> select Responsible Gambling item -> Tap/click 'I want to close my Account' link within 'Account Closure' section)
    PRECONDITIONS: * Player Tag 'Account_Closed_By_Player' is set to 'True' for a user in IMS
    PRECONDITIONS: * Player Tag 'On_login_Account_Closed_Message' is set for a user in IMS (FE doesn't set this tag)
    PRECONDITIONS: * 'Reactivation' Log in message is created with the tag 'On_login_Account_Closed_Message' in IMS
    PRECONDITIONS: * The login pop up is set within IMS - configuration instructions can be found here https://drive.google.com/drive/u/2/folders/1pkGIbDBUp2rU_iWXh1ve18W0mwK71VMU
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * 'Reactivation' page is opened (via link on 'On login' pop-up or Right Hand menu)
    PRECONDITIONS: Design -> Reactivation -> https://app.zeplin.io/project/5bf56b032790467ebfb30d0f/dashboard
    """
    keep_browser_open = True

    def test_001_verify_the_reactivation_page_content(self):
        """
        DESCRIPTION: Verify the Reactivation page content
        EXPECTED: The Reactivation page consists of:
        EXPECTED: * 'Back' button and 'Reactivation' header
        EXPECTED: * 'Reactivate your account' sub header  and 'To reactivate your account please confirm with the password below:'  text message
        EXPECTED: * 'Password' field with 'Show' option
        EXPECTED: * 'Please note: after successful reactivation you will be automatically redirected to the Coral home page' text message under password field
        EXPECTED: * Inactive 'CONFIRM' button
        """
        pass

    def test_002__enter_at_least_one_symbol_to_password_field_verify_the_confirm_button(self):
        """
        DESCRIPTION: * Enter at least one symbol to 'Password' field
        DESCRIPTION: * Verify the 'CONFIRM' button
        EXPECTED: 'CONFIRM' button becomes enabled immediately
        """
        pass

    def test_003__delete_all_the_symbols_from_password_field_verify_the_confirm_button(self):
        """
        DESCRIPTION: * Delete all the symbols from 'Password' field
        DESCRIPTION: * Verify the 'CONFIRM' button
        EXPECTED: 'CONFIRM' button becomes disabled immediately
        """
        pass

    def test_004__enter_at_least_one_symbol_to_password_field_clicktap_show_option_within_password_field(self):
        """
        DESCRIPTION: * Enter at least one symbol to 'Password' field
        DESCRIPTION: * Click/tap 'SHOW' option within 'Password' field
        EXPECTED: * Characters within the 'Password' field become visible
        EXPECTED: * 'Hide' option is displayed instead of 'SHOW'
        """
        pass

    def test_005_clicktap_hide_option(self):
        """
        DESCRIPTION: Click/tap 'Hide' option
        EXPECTED: Characters within the 'Password' field are not visible
        """
        pass

    def test_006_enter_valid_password_in_password_field(self):
        """
        DESCRIPTION: Enter valid password in 'Password' field
        EXPECTED: * 'Password' field is populated with the value
        EXPECTED: * Characters within are hidden by default
        EXPECTED: * 'CONFIRM' button becomes enabled once at least one symbol is entered
        EXPECTED: * No error message is displayed
        """
        pass

    def test_007_clicktap_confirm_button(self):
        """
        DESCRIPTION: Click/tap 'CONFIRM' button
        EXPECTED: * 'Accout Reactivation' confirmation pop-up is shown
        EXPECTED: * User remains logged in
        """
        pass
