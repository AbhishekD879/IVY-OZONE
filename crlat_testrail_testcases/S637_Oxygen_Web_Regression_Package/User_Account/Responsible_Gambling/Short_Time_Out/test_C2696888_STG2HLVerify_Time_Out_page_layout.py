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
class Test_C2696888_STG2HLVerify_Time_Out_page_layout(Common):
    """
    TR_ID: C2696888
    NAME: [STG2][HL]Verify 'Time Out' page layout
    DESCRIPTION: This test case verifies 'Time Out' page layout
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: * Click/Tap on 'Take a short break' link
    PRECONDITIONS: * 'Time Out' page is opened
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 'Responsible Gambling' page with all sections are CMS configurable. Please, take a look at https://ladbrokescoral.testrail.com/index.php?/cases/view/28369 to get acquainted with the instruction how to create or update content on 'Responsible Gambling' page.
    """
    keep_browser_open = True

    def test_001_verify_time_out_page_layout(self):
        """
        DESCRIPTION: Verify 'Time Out' page layout
        EXPECTED: * Header with 'Time Out' title and 'Back' button
        EXPECTED: * 'Select period of time-out' dropdown
        EXPECTED: * 'Reason for time-out' checkboxes
        EXPECTED: * 'Continue' button
        EXPECTED: * 'Cancel' button
        """
        pass

    def test_002_verify_select_period_of_time_out_dropdown(self):
        """
        DESCRIPTION: Verify 'Select period of time-out' dropdown
        EXPECTED: * 'Please select period of time that you wish time-out to apply:' text is displayed above dropdown
        EXPECTED: * 'Please select' placeholder is displayed within the dropdown by default
        EXPECTED: * The dropdown is clickable and contains the list of values
        """
        pass

    def test_003_verify_reason_for_time_out_checkboxes(self):
        """
        DESCRIPTION: Verify 'Reason for time-out' checkboxes
        EXPECTED: * 'Reason for time-out:' text is displayed above the checkboxes
        EXPECTED: * There is NO checkbox selected by default
        EXPECTED: * The checkbox is clickable
        """
        pass

    def test_004_verify_continue_button(self):
        """
        DESCRIPTION: Verify 'Continue' button
        EXPECTED: * Button is located below 'Reason for time-out' checkboxes
        EXPECTED: * Button is disabled and not clickable until value from 'Select period of time-out' drop-down and 'Reason for time-out' checkbox are selected
        """
        pass

    def test_005_verify_cancel_button(self):
        """
        DESCRIPTION: Verify 'Cancel' button
        EXPECTED: * Button is located below 'Continue' button
        EXPECTED: * Button is active and clickable
        """
        pass
