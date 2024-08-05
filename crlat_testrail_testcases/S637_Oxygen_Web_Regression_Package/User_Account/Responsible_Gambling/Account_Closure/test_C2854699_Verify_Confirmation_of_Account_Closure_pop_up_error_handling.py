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
class Test_C2854699_Verify_Confirmation_of_Account_Closure_pop_up_error_handling(Common):
    """
    TR_ID: C2854699
    NAME: Verify 'Confirmation of Account Closure' pop-up error handling
    DESCRIPTION: This test case verifies 'Confirmation of Account Closure' pop-up error handling error handling
    DESCRIPTION: Note: cannot automate as we do not have the possibility to simulate connection loss during an automation test run
    PRECONDITIONS: * Load app and log in
    PRECONDITIONS: * Navigate to Right Menu -> My Account -> select Responsible Gambling item
    PRECONDITIONS: * Tap/click 'I want to close my Account' link within 'Account Closure' section
    PRECONDITIONS: * Select any option from 'Closure Reason' drop-down and click/tap 'CONTINUE' button on Account Closure step 1 page
    PRECONDITIONS: * Enter valid password in 'Password' field and click/tap 'CONTINUE' button on Account Closure step 2 page
    """
    keep_browser_open = True

    def test_001_select_confirm_checkbox(self):
        """
        DESCRIPTION: Select 'Confirm' checkbox
        EXPECTED: 'Confirm' checkbox is checked
        """
        pass

    def test_002_trigger_error_received_from_open_api_response_eg_turn_off_internet_connection_and_tap_yes_button(self):
        """
        DESCRIPTION: Trigger error received from Open API response (e.g. turn off internet connection) and tap 'YES' button
        EXPECTED: "Sorry an Error occurred, please try again" error Message is displayed below 'Confirm' checkbox
        EXPECTED: **NOTE** if a loss of internet connection is triggered then 'Confirmation of Account Closure' pop-up will disappear after tapping 'YES' button as its general error handling for all pop-ups within app during connection loss
        """
        pass

    def test_003_tap_yes_with_the_checkbox_ticked_with_valid_conditions(self):
        """
        DESCRIPTION: Tap 'Yes' with the checkbox ticked with valid conditions
        EXPECTED: 'Your Account is now closed' pop-up is displayed
        """
        pass
