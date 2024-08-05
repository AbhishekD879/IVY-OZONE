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
class Test_C2727290_STG2HLVerify_Period_drop_down_and_Reason_checkboxes_on_Time_Out_page(Common):
    """
    TR_ID: C2727290
    NAME: [STG2][HL]Verify 'Period' drop-down and 'Reason' checkboxes on 'Time-Out' page
    DESCRIPTION: This test case verifies 'Period' drop-down and 'Reason' checkboxes on 'Time-Out' page
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: * Click/Tap on 'Take a short break' link
    PRECONDITIONS: * 'Time Out' page is opened
    PRECONDITIONS: *Note:*
    PRECONDITIONS: 'Responsible Gambling' page with all sections are CMS configurable. Please, take a look at https://ladbrokescoral.testrail.com/index.php?/cases/view/28369 to get acquainted with the instruction how to create or update content on 'Responsible Gambling' page.
    PRECONDITIONS: To verify values displayed within 'Select period of time-out' dropdown, perform the following steps:
    PRECONDITIONS: 1) open network >WS
    PRECONDITIONS: 2) select "openapi-stg1.egalacoral.com/socket.io/1/websocket/9e73af79-a4fb-4372-9d9d-92f76e932da0" (differ depending on endpoints)
    PRECONDITIONS: 3) check values in **timeoutConfigurationItems** response (id:32943)
    """
    keep_browser_open = True

    def test_001_verify_time_out_page(self):
        """
        DESCRIPTION: Verify 'Time Out' page
        EXPECTED: * 'Please select' placeholder is displayed within the 'Select period of time-out' dropdown by default
        EXPECTED: * There is NO 'Reason for time-out' checkbox selected by default
        EXPECTED: * 'Continue' button is disabled
        EXPECTED: * 'Cancel' button is active
        """
        pass

    def test_002_click_on_select_period_of_time_out_dropdown(self):
        """
        DESCRIPTION: Click on 'Select period of time-out' dropdown
        EXPECTED: List of received values in WS from IMS is displayed within the dropdown in the next format:
        EXPECTED: 1 hour
        EXPECTED: 1 day
        EXPECTED: 1 week
        EXPECTED: 3 weeks
        EXPECTED: etc.
        EXPECTED: *(see preconditions as how to verify)*
        """
        pass

    def test_003_select_any_value_from_the_select_period_of_time_out_dropdown(self):
        """
        DESCRIPTION: Select any value from the 'Select period of time-out' dropdown
        EXPECTED: * Selected value is displayed within the dropdown
        EXPECTED: * 'Continue' button is still disabled
        EXPECTED: * 'Cancel' button is active
        """
        pass

    def test_004_tick_any_reason_for_time_out_checkbox(self):
        """
        DESCRIPTION: Tick any 'Reason for time-out' checkbox
        EXPECTED: * Checkbox is ticked
        EXPECTED: * 'Continue' button becomes active
        """
        pass

    def test_005_tick_any_other_reason_for_time_out_checkbox(self):
        """
        DESCRIPTION: Tick any other 'Reason for time-out' checkbox
        EXPECTED: * Checkbox is ticked
        EXPECTED: * Previously ticked checkbox becomes unticked
        EXPECTED: * Only one checkbox can be ticked at a time (single-select)
        """
        pass

    def test_006_untick_reason_for_time_out_checkbox(self):
        """
        DESCRIPTION: Untick 'Reason for time-out' checkbox
        EXPECTED: * Checkbox is unticked
        EXPECTED: * 'Continue' button becomes disabled
        """
        pass

    def test_007_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step 4
        EXPECTED: * Checkbox is ticked
        EXPECTED: * 'Continue' button becomes active
        """
        pass

    def test_008_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: 'Time-Out Password' page is opened
        """
        pass
