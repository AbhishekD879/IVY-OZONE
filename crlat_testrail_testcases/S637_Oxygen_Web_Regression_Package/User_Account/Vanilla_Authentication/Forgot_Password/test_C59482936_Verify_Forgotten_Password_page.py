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
class Test_C59482936_Verify_Forgotten_Password_page(Common):
    """
    TR_ID: C59482936
    NAME: Verify Forgotten Password page
    DESCRIPTION: This test case verifies Reset Password displaying
    PRECONDITIONS: 1. Make sure you have registered user account.
    PRECONDITIONS: 2. Load Oxygen application and make sure user is NOT logged in
    PRECONDITIONS: 3. Choosing the password should include following rules:
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True

    def test_001_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up appears
        """
        pass

    def test_002_clicktap_on_forgot_password_link(self):
        """
        DESCRIPTION: Click/Tap on 'Forgot password?' link
        EXPECTED: 'Forgotten Password' page is opened
        """
        pass

    def test_003_verify_reset_password_page(self):
        """
        DESCRIPTION: Verify 'Reset Password' page
        EXPECTED: 'Reset Password' page consists of:
        EXPECTED: - 'Forgotten Password' title
        EXPECTED: Info box with text: "If you have forgotten your Connect card pin please contact our support team."
        EXPECTED: - 'Username', field
        EXPECTED: - 'SUBMIT' button
        EXPECTED: - 'LIVE CHAT' button
        EXPECTED: - 'CONTACT US' button
        """
        pass

    def test_004_verify_username_field(self):
        """
        DESCRIPTION: Verify 'Username' field
        EXPECTED: - 'Username' field contains the login of the last logged in user.
        """
        pass

    def test_005_verify_validation_messages_appearance_when_username_field_is_empty(self):
        """
        DESCRIPTION: Verify validation messages appearance when Username field is empty
        EXPECTED: Field is highlighted in red and validation message is displayed:
        EXPECTED: - Please insert your Username in the text field.
        EXPECTED: SUBMIT button is disabled
        """
        pass

    def test_006_enter_incorrect_username_into_appropriate_field_e_g_short_username__6_symbols_and_click_submit_button(self):
        """
        DESCRIPTION: Enter incorrect username into appropriate field (e. g. short username (< 6 symbols)) and click SUBMIT button.
        EXPECTED: Error message appears.
        EXPECTED: "The Email/User ID does not match any existing account."
        """
        pass

    def test_007_clicktap_live_chat_button(self):
        """
        DESCRIPTION: Click/tap LIVE CHAT button
        EXPECTED: LIVE CHAT panel appears on the right.
        """
        pass

    def test_008_clicktap_contact_us_button(self):
        """
        DESCRIPTION: Click/tap CONTACT US button
        EXPECTED: User is redirected to 'How can we help you?' page (<Environment>/en/mobileportal/contact)
        """
        pass
