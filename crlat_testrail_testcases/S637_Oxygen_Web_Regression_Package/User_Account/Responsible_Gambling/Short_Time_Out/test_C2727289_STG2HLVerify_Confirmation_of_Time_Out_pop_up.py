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
class Test_C2727289_STG2HLVerify_Confirmation_of_Time_Out_pop_up(Common):
    """
    TR_ID: C2727289
    NAME: [STG2][HL]Verify 'Confirmation of Time-Out' pop-up
    DESCRIPTION: This test case verifies 'Confirmation of Time-Out' pop-up
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

    def test_001_verify_confirmation_of_time_out_pop_up(self):
        """
        DESCRIPTION: Verify 'Confirmation of Time-Out' pop-up
        EXPECTED: * 'Deposit Limits' and 'Game play Reminder' links
        EXPECTED: * 'Confirmation of Time-Out' checkbox is unticked by default
        EXPECTED: * 'Yes' button is disabled
        EXPECTED: * 'Cancel' button is active
        """
        pass

    def test_002_clicktap_on_deposit_limits_link(self):
        """
        DESCRIPTION: Click/Tap on 'Deposit Limits' link
        EXPECTED: The user is taken to https://sports.coral.co.uk/limits page
        """
        pass

    def test_003_back_to_pop_up_and_clicktap_on_game_play_reminder_link(self):
        """
        DESCRIPTION: Back to pop-up and click/tap on 'Game play Reminder' link
        EXPECTED: The user is taken to https://sports.coral.co.uk/limits page
        """
        pass

    def test_004_back_to_pop_up_and_tick_confirmation_of_time_out_checkbox(self):
        """
        DESCRIPTION: Back to pop-up and tick 'Confirmation of Time-Out' checkbox
        EXPECTED: * The checkbox is displayed as ticked
        EXPECTED: * 'Yes' button becomes active
        """
        pass

    def test_005_verify_time_out_expiration_date(self):
        """
        DESCRIPTION: Verify Time-Out expiration date
        EXPECTED: Time-Out expiration date is based on values set by the user on 'Time-Out' page
        """
        pass

    def test_006_clicktap_on_yes_button(self):
        """
        DESCRIPTION: Click/Tap on 'Yes' button
        EXPECTED: * 'Time-Out Period Successful' pop-up appears instead of  'Confirmation of Time-Out' pop-up
        EXPECTED: * The user is logged out automatically
        """
        pass
