import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.registration
@pytest.mark.user_account
@pytest.mark.desktop
@pytest.mark.uat
@vtest
class Test_C44870127_Verify_successful_registration_process_for_new_user_and_user_is_autologged_in_to_site(Common):
    """
    TR_ID: C44870127
    NAME: Verify successful registration process for new user and user is autologged in to site
    """
    keep_browser_open = True

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Application page is loaded
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_on_log_in(self):
        """
        DESCRIPTION: Tap on 'Log in'
        EXPECTED: Login overlay is loaded with
        EXPECTED: 'REGISTER' option available on this page as well.
        EXPECTED: On clicking 'REGISTER' the user is navigated to the registration page (Step 3)
        """
        self.site.header.sign_in.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(dialog, msg='No login dialog present on page')
        self.assertTrue(dialog.create_an_account.is_displayed(),
                        msg='"create account button" is not present in login dailog')
        dialog.create_an_account.click()
        expected_url = f'https://{tests.HOSTNAME}/en/mobileportal/register'.replace('beta2', 'beta')
        wait_for_result(lambda: expected_url in self.device.get_current_url(), name='Page to be loaded', timeout=10)
        register_form = self.site.three_steps_registration
        self.assertTrue(register_form, msg='Registration form is not displayed')
        self.navigate_to_page('Homepage')

    def test_003_tap_on_join_button(self):
        """
        DESCRIPTION: Tap on 'Join' button
        EXPECTED: Page 'Registration - Step 1(About)' is shown
        """
        self.site.register_new_user(birth_date='01-06-1977')
        self.assertTrue(self.site.wait_logged_in(timeout=2), msg='User is not logged in')

    def test_004_enter_correct_data_to_all_required_fields(self):
        """
        DESCRIPTION: Enter correct data to all required fields
        EXPECTED: All mandatory fields are filled
        EXPECTED: None of fields are highlighted in red
        """
        # This step is covered in test step 3

    def test_005_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: Each field is validated and any validation issues are reported.
        EXPECTED: Page 'Registration' - Step 2 (Name & Date of Birth) is shown
        """
        # This step is covered in test step 3

    def test_006_enter_correct_data_to_all_required_fields(self):
        """
        DESCRIPTION: Enter correct data to all required fields
        EXPECTED: All mandatory fields are filled.
        EXPECTED: None of fields are highlighted in red
        """
        # This step is covered in test step 3

    def test_007_tap_on_continue_button(self):
        """
        DESCRIPTION: Tap on 'Continue' button
        EXPECTED: Each field is validated and any validation issues are reported.
        EXPECTED: Page 'Registration - Step 3(Address,Contact Info & Marketing preferences)' is shown
        """
        # This step is covered in test step 3

    def test_008_enter_correct_data_to_all_required_fields(self):
        """
        DESCRIPTION: Enter correct data to all required fields
        EXPECTED: All mandatory fields are filled.
        EXPECTED: None of fields are highlighted in red
        """
        # This step is covered in test step 3

    def test_009_tap_on_create_account_button(self):
        """
        DESCRIPTION: Tap on 'Create Account' button
        EXPECTED: Set your deposit limits & Fund Protection policy are ticked
        """
        # This step is covered in test step 3

    def test_010_tap_on_submit_button(self):
        """
        DESCRIPTION: Tap on 'Submit' button
        EXPECTED: User is registered successfully and logged in automatically
        EXPECTED: Deposit page should be opened once user saves the preferences
        """
        # This step is covered in test step 3
