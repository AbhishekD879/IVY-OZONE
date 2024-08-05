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
class Test_C44870127_Verify_successful_registration_process_for_new_user_and_user_is_autologged_in_to_site(Common):
    """
    TR_ID: C44870127
    NAME: Verify successful registration process for new user and user is autologged in to site
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Application page is loaded
        """
        pass

    def test_002_tap_on_log_in(self):
        """
        DESCRIPTION: Tap on 'Log in'
        EXPECTED: Login overlay is loaded with
        EXPECTED: 'REGISTER' option available on this page as well.
        EXPECTED: On clicking 'REGISTER' the user is navigated to the registration page (Step 3)
        """
        pass

    def test_003_tap_on_join_button(self):
        """
        DESCRIPTION: Tap on 'Join' button
        EXPECTED: Page 'Registration - Step 1(About)' is shown
        """
        pass

    def test_004_enter_correct_data_to_all_required_fields(self):
        """
        DESCRIPTION: Enter correct data to all required fields
        EXPECTED: All mandatory fields are filled
        EXPECTED: None of fields are highlighted in red
        """
        pass

    def test_005_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: Each field is validated and any validation issues are reported.
        EXPECTED: Page 'Registration' - Step 2 (Name & Date of Birth) is shown
        """
        pass

    def test_006_enter_correct_data_to_all_required_fields(self):
        """
        DESCRIPTION: Enter correct data to all required fields
        EXPECTED: All mandatory fields are filled.
        EXPECTED: None of fields are highlighted in red
        """
        pass

    def test_007_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: Each field is validated and any validation issues are reported.
        EXPECTED: Page 'Registration - Step 3(Address,Contact Info & Marketing preferences)' is shown
        """
        pass

    def test_008_enter_correct_data_to_all_required_fields(self):
        """
        DESCRIPTION: Enter correct data to all required fields
        EXPECTED: All mandatory fields are filled.
        EXPECTED: None of fields are highlighted in red
        """
        pass

    def test_009_tap_on_create_account_button(self):
        """
        DESCRIPTION: Tap on 'Create Account' button
        EXPECTED: Set your deposit limits & Fund Protection policy are ticked
        """
        pass

    def test_010_tap_on_submit_button(self):
        """
        DESCRIPTION: Tap on 'Submit' button
        EXPECTED: User is registered successfully and logged in automatically
        EXPECTED: Deposit page should be opened once user saves the preferences
        """
        pass
