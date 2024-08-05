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
class Test_C2696885_STG2HLVerify_Short_Time_Out_functionality(Common):
    """
    TR_ID: C2696885
    NAME: [STG2][HL]Verify 'Short Time Out' functionality
    DESCRIPTION: This test case verifies 'Short Time Out' functionality
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed on the page
    PRECONDITIONS: *Note:*
    PRECONDITIONS: * 'Responsible Gambling' page with all sections are CMS configurable. Please, take a look at https://ladbrokescoral.testrail.com/index.php?/cases/view/28369 to get acquainted with the instruction how to create or update content on 'Responsible Gambling' page.
    PRECONDITIONS: * 'Take a short break' link should be set in Static Block for 'Short Time-Out' section.
    """
    keep_browser_open = True

    def test_001_clicktap_on_take_a_short_break_link(self):
        """
        DESCRIPTION: Click/Tap on 'Take a short break' link
        EXPECTED: * 'Time Out' page is opened
        EXPECTED: * 'Please select' placeholder is displayed within the 'Select period of time-out' dropdown by default
        EXPECTED: * There is NO 'Reason for time-out' checkbox selected by default
        EXPECTED: * 'Continue' button is disabled
        EXPECTED: * 'Cancel' button is active
        """
        pass

    def test_002_select_any_value_from_the_select_period_of_time_out_dropdown(self):
        """
        DESCRIPTION: Select any value from the 'Select period of time-out' dropdown
        EXPECTED: * Selected value is displayed within the dropdown
        EXPECTED: * 'Continue' button is still disabled
        """
        pass

    def test_003_tick_any_reason_for_time_out_checkbox(self):
        """
        DESCRIPTION: Tick any 'Reason for time-out' checkbox
        EXPECTED: * Checkbox is ticked (only one checkbox can be ticked at a time)
        EXPECTED: * 'Continue' button becomes active
        """
        pass

    def test_004_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: * 'Time-Out Password' page is opened
        EXPECTED: * 'Password' field is displayed on the page
        EXPECTED: * 'Continue' button is disabled
        EXPECTED: * 'Cancel' button is active
        """
        pass

    def test_005_enter_correct_user_password_in_password_field_for_approving_the_timeout_request(self):
        """
        DESCRIPTION: Enter correct user password in 'Password' field for approving the timeout request
        EXPECTED: * Password is displayed in the field
        EXPECTED: * Password characters are hidden by default
        EXPECTED: * 'Continue' button becomes active and clickable
        """
        pass

    def test_006_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: * 'Confirmation of Time-Out' pop-up appears over the page
        EXPECTED: * 'Confirmation of Time-Out' checkbox is unticked by default
        EXPECTED: * 'Yes' button is disabled
        EXPECTED: * 'Cancel' button is active
        """
        pass

    def test_007_tick_confirmation_of_time_out_checkbox(self):
        """
        DESCRIPTION: Tick 'Confirmation of Time-Out' checkbox
        EXPECTED: * The checkbox is ticked
        EXPECTED: * 'Yes' button becomes active
        """
        pass

    def test_008_clicktap_on_yes_button(self):
        """
        DESCRIPTION: Click/Tap on 'Yes' button
        EXPECTED: * 'Time-Out Period Successful' pop-up appears instead of  'Confirmation of Time-Out' pop-up
        EXPECTED: * 'Ok' button is active
        EXPECTED: * The user is logged out automatically
        """
        pass

    def test_009_clicktap_on_ok_button(self):
        """
        DESCRIPTION: Click/Tap on 'Ok' button
        EXPECTED: * 'Time-Out Period Successful' pop-up disappears
        EXPECTED: * Time-out period is set successfully
        """
        pass
