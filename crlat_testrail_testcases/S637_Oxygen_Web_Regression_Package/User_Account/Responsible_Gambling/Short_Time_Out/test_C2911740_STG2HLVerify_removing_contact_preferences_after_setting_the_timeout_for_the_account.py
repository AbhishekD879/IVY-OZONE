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
class Test_C2911740_STG2HLVerify_removing_contact_preferences_after_setting_the_timeout_for_the_account(Common):
    """
    TR_ID: C2911740
    NAME: [STG2][HL]Verify removing contact preferences after setting the timeout for the account
    DESCRIPTION: This test case verifies removing contact preferences after setting the timeout for the account
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Contact Preferences is set as 'true' for the next channels with Promotional type: email, SMS, phone, directMail
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: * Click/Tap on 'Take a short break' link for opening the 'Time-Out' page
    PRECONDITIONS: * Select any value from the 'Select period of time-out' dropdown and Tick any 'Reason for time-out' checkbox
    PRECONDITIONS: * Click/Tap on 'Continue' button to reach the 'Time-Out Password' page
    PRECONDITIONS: * Enter the valid password and click 'Continue' button
    PRECONDITIONS: * 'Confirmation of Time-Out' pop-up appears
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) For checking setting for email, SMS, phone, directMail channels open Dev Tools->Application->Local Storage->OX.USER->contactPreferences:
    PRECONDITIONS: * channel: "email"
    PRECONDITIONS: * preference: true
    PRECONDITIONS: * type: "promotional"
    PRECONDITIONS: * channel: "SMS"
    PRECONDITIONS: * preference: true
    PRECONDITIONS: * type: "promotional"
    PRECONDITIONS: * channel: "phone"
    PRECONDITIONS: * preference: true
    PRECONDITIONS: * type: "promotional"
    PRECONDITIONS: * channel: "directMail"
    PRECONDITIONS: * preference: true
    PRECONDITIONS: * type: "promotional"
    PRECONDITIONS: 2) For changing contact preferences open Oxygen app->'Right Menu'->'My account'->'Marketing Preferences'.
    PRECONDITIONS: 3) For checking requests and responses open Dev Tools->Network->WS:
    PRECONDITIONS: '89910' request is sent for setting Player Time Out Period
    PRECONDITIONS: '35513' request is sent for setting Player Contact Preferences
    """
    keep_browser_open = True

    def test_001_clicktap_on_yes_button(self):
        """
        DESCRIPTION: Click/Tap on 'Yes' button
        EXPECTED: * 'Time-Out Period Successful' pop-up appears instead of 'Confirmation of Time-Out' pop-up
        EXPECTED: * The user is logged out automatically
        EXPECTED: * '35513' request is sent in WS simultaneously with '89910'
        """
        pass

    def test_002_verify_sent_values_in_35513_request(self):
        """
        DESCRIPTION: Verify sent values in '35513' request
        EXPECTED: * channel: "email"
        EXPECTED: * preference: false
        EXPECTED: * type: "promotional"
        EXPECTED: * channel: "SMS"
        EXPECTED: * preference: false
        EXPECTED: * type: "promotional"
        EXPECTED: * channel: "phone"
        EXPECTED: * preference: false
        EXPECTED: * type: "promotional"
        EXPECTED: * channel: "directMail"
        EXPECTED: * preference:  false
        EXPECTED: * type: "promotional"
        """
        pass

    def test_003_verify_contact_preferences_values_in_local_storage(self):
        """
        DESCRIPTION: Verify contact preferences values in Local Storage
        EXPECTED: contactPreferences: null
        """
        pass

    def test_004_log_in_the_app_again_after_expiring_of_time_out_period_for_the_user(self):
        """
        DESCRIPTION: Log in the app again after expiring of Time-Out period for the user
        EXPECTED: The user is logged in successfully
        """
        pass

    def test_005_verify_set_values_for_contact_preferences_in_local_storage(self):
        """
        DESCRIPTION: Verify set values for contact preferences in Local Storage
        EXPECTED: * channel: "email"
        EXPECTED: * preference: false
        EXPECTED: * type: "promotional"
        EXPECTED: * channel: "SMS"
        EXPECTED: * preference: false
        EXPECTED: * type: "promotional"
        EXPECTED: * channel: "phone"
        EXPECTED: * preference: false
        EXPECTED: * type: "promotional"
        EXPECTED: * channel: "directMail"
        EXPECTED: * preference:  false
        EXPECTED: * type: "promotional"
        """
        pass
