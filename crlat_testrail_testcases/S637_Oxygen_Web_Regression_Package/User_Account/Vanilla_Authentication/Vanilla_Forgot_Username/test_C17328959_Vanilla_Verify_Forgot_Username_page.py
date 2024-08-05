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
class Test_C17328959_Vanilla_Verify_Forgot_Username_page(Common):
    """
    TR_ID: C17328959
    NAME: [Vanilla] Verify Forgot Username page
    DESCRIPTION: This test case verifies 'Forgotten Username' section
    PRECONDITIONS: Make sure you have registered user account.
    """
    keep_browser_open = True

    def test_001_tap_login_button(self):
        """
        DESCRIPTION: Tap 'LOGIN' button
        EXPECTED: 'LOGIN' pop-up appears
        """
        pass

    def test_002_clicktap_on_i_forgot_my_username_link(self):
        """
        DESCRIPTION: Click/Tap on 'I forgot my Username' link
        EXPECTED: 'FORGOTTEN USERNAME' page is opened
        """
        pass

    def test_003_verify_forgot_username_page(self):
        """
        DESCRIPTION: Verify 'Forgot username' page
        EXPECTED: 'Forgot username' page consists of:
        EXPECTED: - 'FORGOTTEN USERNAME' title
        EXPECTED: - 'Email' field
        EXPECTED: - 'Date of birth' field
        EXPECTED: - 'SUBMIT' button
        EXPECTED: - 'LIVE CHAT' button
        EXPECTED: - 'CONTACT US' button
        """
        pass

    def test_004_verify_email_field(self):
        """
        DESCRIPTION: Verify 'Email' field
        EXPECTED: - Field is mandatory
        EXPECTED: - 'Email' field is empty by default
        EXPECTED: - Permitted values: correct email address format: (XXX@XXX.XXX)
        """
        pass

    def test_005_enter_invalid_email_address(self):
        """
        DESCRIPTION: Enter invalid email address
        EXPECTED: 'Please enter a valid email address' red text message appears under Email field
        """
        pass

    def test_006_verify_date_of_birth_drop_down(self):
        """
        DESCRIPTION: Verify 'Date of birth' drop-down
        EXPECTED: 'Date of Birth' field consist of 3 drop-down buttons:
        EXPECTED: - 'Day' drop-down: 1-31
        EXPECTED: - 'Month' drop-down: each months are shown in 3 letter abbreviations (Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)
        EXPECTED: - 'Year' drop -down: Current - 18 to 1900***
        """
        pass

    def test_007_verify_validation_messages_appearance_after_clicktap_on_submit_button_when_all_fields_are_empty(self):
        """
        DESCRIPTION: Verify validation messages appearance after click/tap on 'SUBMIT' button when all fields are empty
        EXPECTED: 'SUBMIT' button is disabled
        """
        pass

    def test_008_verify_validation_messages_appearance_after_clicktap_on_submit_button_when_some_fileds_are_empty(self):
        """
        DESCRIPTION: Verify validation messages appearance after click/tap on 'SUBMIT' button when some fileds are empty
        EXPECTED: 'SUBMIT' button is disabled
        """
        pass

    def test_009_tap_on_x_button(self):
        """
        DESCRIPTION: Tap on 'X' button
        EXPECTED: 'FORGOTTEN USERNAME' page is closed. Login popup is displayed again
        """
        pass
