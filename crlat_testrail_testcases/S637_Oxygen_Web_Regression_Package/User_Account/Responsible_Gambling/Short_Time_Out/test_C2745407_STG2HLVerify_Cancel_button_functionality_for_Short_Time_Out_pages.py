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
class Test_C2745407_STG2HLVerify_Cancel_button_functionality_for_Short_Time_Out_pages(Common):
    """
    TR_ID: C2745407
    NAME: [STG2][HL]Verify 'Cancel' button functionality for 'Short Time-Out' pages
    DESCRIPTION: This test case verifies 'Cancel' button functionality for 'Short Time-Out' pages
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: *Note:*
    PRECONDITIONS: * 'Responsible Gambling' page with all sections are CMS configurable. Please, take a look at https://ladbrokescoral.testrail.com/index.php?/cases/view/28369 to get acquainted with the instruction how to create or update content on 'Responsible Gambling' page.
    """
    keep_browser_open = True

    def test_001_clicktap_on_take_a_short_break_link(self):
        """
        DESCRIPTION: Click/Tap on 'Take a short break' link
        EXPECTED: 'Time Out' page is opened
        """
        pass

    def test_002_select_any_value_from_the_select_period_of_time_out_dropdown_and_tick_any_reason_for_time_out_checkbox(self):
        """
        DESCRIPTION: Select any value from the 'Select period of time-out' dropdown and tick any 'Reason for time-out' checkbox
        EXPECTED: * Selected value is displayed within the dropdown
        EXPECTED: * Checkbox is ticked
        EXPECTED: * 'Continue' button becomes active
        """
        pass

    def test_003_clicktap_on_cancel_button(self):
        """
        DESCRIPTION: Click/Tap on 'Cancel' button
        EXPECTED: The user is taken to the 'Responsible Gambling' page
        """
        pass

    def test_004_clicktap_on_take_a_short_break_link(self):
        """
        DESCRIPTION: Click/Tap on 'Take a short break' link
        EXPECTED: * 'Time Out' page is opened
        EXPECTED: * Previous set changes are NOT remembered on the 'Time Out' page
        """
        pass

    def test_005_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: * Selected value is displayed within the dropdown
        EXPECTED: * Checkbox is ticked
        EXPECTED: * 'Continue' button becomes active
        """
        pass

    def test_006_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: * 'Time-Out Password' page is opened
        EXPECTED: * 'Password' field is displayed with 'Password' placeholder inside it
        """
        pass

    def test_007_fill_in_password_field(self):
        """
        DESCRIPTION: Fill in 'Password' field
        EXPECTED: Entered characters are displayed in 'Password' field
        """
        pass

    def test_008_clicktap_on_cancel_button(self):
        """
        DESCRIPTION: Click/Tap on 'Cancel' button
        EXPECTED: The user is taken to the 'Responsible Gambling' page
        """
        pass

    def test_009_repeat_steps_4_7(self):
        """
        DESCRIPTION: Repeat steps 4-7
        EXPECTED: 
        """
        pass

    def test_010_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: 'Confirmation of Time-Out' pop-up appears over the page
        """
        pass

    def test_011_tick_confirmation_of_time_out_checkbox(self):
        """
        DESCRIPTION: Tick 'Confirmation of Time-Out' checkbox
        EXPECTED: 'Confirmation of Time-Out' checkbox is ticked
        """
        pass

    def test_012_clicktap_on_cancel_button(self):
        """
        DESCRIPTION: Click/Tap on 'Cancel' button
        EXPECTED: 'Confirmation of Time-Out' pop-up is closed
        """
        pass

    def test_013_repeat_step_10(self):
        """
        DESCRIPTION: Repeat step 10
        EXPECTED: * 'Confirmation of Time-Out' pop-up appears over the page
        EXPECTED: * Previous set changes are NOT remembered
        """
        pass
