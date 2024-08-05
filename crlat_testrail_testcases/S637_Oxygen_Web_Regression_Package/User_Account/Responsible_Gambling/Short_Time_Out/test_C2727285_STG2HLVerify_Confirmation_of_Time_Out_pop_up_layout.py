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
class Test_C2727285_STG2HLVerify_Confirmation_of_Time_Out_pop_up_layout(Common):
    """
    TR_ID: C2727285
    NAME: [STG2][HL]Verify 'Confirmation of Time-Out' pop-up layout
    DESCRIPTION: This test case verifies 'Confirmation of Time-Out' pop-up layout
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: * Click/Tap on 'Take a short break' link for opening the 'Time-Out' page
    PRECONDITIONS: * Select any value from the 'Select period of time-out' dropdown and Tick any 'Reason for time-out' checkbox
    PRECONDITIONS: * Click/Tap on 'Continue' button to reach the 'Time-Out Password' page
    PRECONDITIONS: * Enter the valid password and click 'Continue' button
    PRECONDITIONS: * 'Confirmation of Time-Out' pop-up appears
    """
    keep_browser_open = True

    def test_001_verify_confirmation_of_time_out_pop_up_layout(self):
        """
        DESCRIPTION: Verify 'Confirmation of Time-Out' pop-up layout
        EXPECTED: * Header with 'Confirmation of Time-Out' title
        EXPECTED: * 'Deposit Limits' link
        EXPECTED: * 'Game play Reminder' link
        EXPECTED: * 'Confirmation of Time-Out' checkbox
        EXPECTED: * Time-Out expiration date
        EXPECTED: * 'Cancel' button
        EXPECTED: * 'Yes' button
        """
        pass

    def test_002_verify_confirmation_of_time_out_checkbox(self):
        """
        DESCRIPTION: Verify 'Confirmation of Time-Out' checkbox
        EXPECTED: 'Confirmation of Time-Out' checkbox is NOT ticked by default
        """
        pass

    def test_003_verify_time_out_expiration_date(self):
        """
        DESCRIPTION: Verify Time-Out expiration date
        EXPECTED: Time-Out expiration date is displayed in the next format:
        EXPECTED: dd/mm/yyyy hh:mm
        """
        pass

    def test_004_verify_cancel_button(self):
        """
        DESCRIPTION: Verify 'Cancel' button
        EXPECTED: * Button is located at the bottom of the pop-up
        EXPECTED: * Button is active and clickable
        """
        pass

    def test_005_verify_yes_button(self):
        """
        DESCRIPTION: Verify 'Yes' button
        EXPECTED: * Button is located at the bottom of the pop-up next to 'Cancel' button
        EXPECTED: * Button is disabled and not clickable until 'Confirmation of Time-Out' checkbox is ticked
        """
        pass
