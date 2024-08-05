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
class Test_C2727295_STG2HLVerify_Short_Time_Out_functionality_with_entering_an_incorrect_password(Common):
    """
    TR_ID: C2727295
    NAME: [STG2][HL]Verify 'Short Time Out' functionality with entering an incorrect password
    DESCRIPTION: This test case verifies  'Short Time Out' functionality with entering an incorrect password
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: * Click/Tap on 'Take a short break' link
    PRECONDITIONS: * 'Time-Out' page is opened
    PRECONDITIONS: * Select any value from the 'Select period of time-out' dropdown and Tick any 'Reason for time-out' checkbox
    PRECONDITIONS: * Click/Tap on 'Continue' button
    PRECONDITIONS: * 'Time-Out Password' page is opened
    """
    keep_browser_open = True

    def test_001_enter_incorrect_user_password_in_password_field_for_approving_the_timeout_request(self):
        """
        DESCRIPTION: Enter incorrect user password in 'Password' field for approving the timeout request
        EXPECTED: * Password is displayed in the field
        EXPECTED: * Password characters are hidden by default
        EXPECTED: * 'Continue' button becomes active and clickable
        """
        pass

    def test_002_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: 'Your password is invalid. Please try again' error message is displayed below 'Password' field
        """
        pass
