import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2745994_Tracking_in_the_Google_Analytics_data_Layer_of_users_navigation_to_Short_Time_Out_pop_ups(Common):
    """
    TR_ID: C2745994
    NAME: Tracking in the Google Analytic's data Layer of user's navigation to 'Short Time Out' pop-ups
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of user's navigation to 'Short Time Out' pop-ups
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    PRECONDITIONS: * Click/Tap on 'Take a short break' link for opening the 'Time-Out' page
    PRECONDITIONS: * Select any value from the 'Select period of time-out' dropdown and Tick any 'Reason for time-out' checkbox
    PRECONDITIONS: * Click/Tap on 'Continue' button to reach the 'Time-Out Password' page
    PRECONDITIONS: * Enter the valid password
    """
    keep_browser_open = True

    def test_001_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: 'Confirmation of Time-Out' pop-up appears
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {'event' : 'trackPageview', 'page' : '/gambling-controls/time-out/confirm' }
        EXPECTED: );
        """
        pass

    def test_003_clicktap_on_deposit_limits_or_game_play_reminder_link(self):
        """
        DESCRIPTION: Click/Tap on 'Deposit Limits' or 'Game play Reminder' link
        EXPECTED: The user is taken to https://sports.coral.co.uk/limits page
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackEvent',     'eventCategory' : 'gambling controls',     'eventAction' : 'timeout linkClick’',     'eventLabel : 'deposit link click’’ or ‘Game play Reminder link click”’ }
        EXPECTED: )
        """
        pass

    def test_005_clicktap_on_cancel_button(self):
        """
        DESCRIPTION: Click/Tap on 'Cancel' button
        EXPECTED: 'Confirmation of Time-Out' pop-up is closed
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackEvent',     'eventCategory' : 'gambling controls',     'eventAction' : ‘timeout confirm message click’,     'eventLabel : ' 'cancel button click in step 3’ }
        """
        pass

    def test_007_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step 1
        EXPECTED: 'Confirmation of Time-Out' pop-up appears
        """
        pass

    def test_008_tick_confirmation_of_time_out_checkbox(self):
        """
        DESCRIPTION: Tick 'Confirmation of Time-Out' checkbox
        EXPECTED: * The checkbox is displayed as ticked
        EXPECTED: * 'Yes' button becomes active
        """
        pass

    def test_009_clicktap_on_yes_button(self):
        """
        DESCRIPTION: Click/Tap on 'Yes' button
        EXPECTED: 'Time-Out Period Successful' pop-up appears instead of 'Confirmation of Time-Out' pop-up
        """
        pass

    def test_010_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: {     'event' : 'trackPageview',     'page' : '/gambling-controls/time-out/success' }
        EXPECTED: );
        """
        pass
