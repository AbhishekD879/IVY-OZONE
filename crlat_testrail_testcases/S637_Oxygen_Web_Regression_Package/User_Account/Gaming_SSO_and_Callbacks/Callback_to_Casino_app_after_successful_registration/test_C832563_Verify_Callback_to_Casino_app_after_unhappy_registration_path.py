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
class Test_C832563_Verify_Callback_to_Casino_app_after_unhappy_registration_path(Common):
    """
    TR_ID: C832563
    NAME: Verify Callback to Casino app after unhappy registration path
    DESCRIPTION: This test case verifies the functionality of a callback to Casino after unhappy completion of the BMA registration
    PRECONDITIONS: *   User should be logged out
    PRECONDITIONS: *   No open tabs with BMA app should be present
    PRECONDITIONS: The general rule should be: if there is no cbURL attribute the stay within the BMA app, if there is a cbURL then take the user to the URL in a separate tab.
    PRECONDITIONS: BMA-5238
    PRECONDITIONS: **Choosing the password should include following rules:**
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True

    def test_001_call_url_httpsbma_urlsignupcburlcasino_urleghttpsinvictuscoralcouksignupcburlhttpmcasino_tst2coralcouk(self):
        """
        DESCRIPTION: Call URL https://BMA_url/#/**signup?cbURL=**<Casino_url>
        DESCRIPTION: (e.g.  https://invictus.coral.co.uk/#/signup?cbURL=http://mcasino-tst2.coral.co.uk)
        EXPECTED: * Oxygen registration form appears
        EXPECTED: * Page 'Join Us - Step 1 of  2' is shown
        """
        pass

    def test_002_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules
        EXPECTED: * All mandatory fields are filled.
        EXPECTED: * None of fields are highlighted in red
        """
        pass

    def test_003_tap_go_to_step_2_button(self):
        """
        DESCRIPTION: Tap 'Go to Step 2' button
        EXPECTED: Page 'Join Us - Step 2 of 2' is shown
        """
        pass

    def test_004_enter_incorrect_data_to_some_fields_of_registration_form(self):
        """
        DESCRIPTION: Enter incorrect data to some fields of Registration form
        EXPECTED: *   All mandatory fields are filled.
        EXPECTED: *   Invalid fields are highlihted in red
        EXPECTED: *   User stays on Registration page on BMA app
        """
        pass

    def test_005_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules
        EXPECTED: * All mandatory fields are filled.
        EXPECTED: * None of fields are highlihted in red
        """
        pass

    def test_006_trigger_an_error_on_deposit_limit_section(self):
        """
        DESCRIPTION: Trigger an error on 'Deposit Limit' section
        EXPECTED: * Error message is displayed
        EXPECTED: * User remains on the current form/page
        """
        pass

    def test_007_tap_complete_registration_button(self):
        """
        DESCRIPTION: Tap 'Complete Registration' button
        EXPECTED: *   Registration is successfully completed
        EXPECTED: *   User is redirected to Oxygen application
        EXPECTED: *   User is logged in there automaticaly
        """
        pass
