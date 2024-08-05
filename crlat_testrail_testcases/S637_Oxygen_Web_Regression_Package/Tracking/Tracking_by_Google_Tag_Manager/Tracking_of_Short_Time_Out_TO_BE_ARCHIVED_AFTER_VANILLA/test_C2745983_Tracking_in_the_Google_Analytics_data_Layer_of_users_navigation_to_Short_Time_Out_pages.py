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
class Test_C2745983_Tracking_in_the_Google_Analytics_data_Layer_of_users_navigation_to_Short_Time_Out_pages(Common):
    """
    TR_ID: C2745983
    NAME: Tracking in the Google Analytic's data Layer of user's navigation to 'Short Time Out' pages
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of user's navigation to 'Short Time Out' pages
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Oxygen app is loaded and the user is logged in
    PRECONDITIONS: * Navigate to 'Right Menu' -> 'My Account' -> 'Responsible Gambling'
    PRECONDITIONS: * 'Responsible Gambling' page is opened and 'Short Time Out' section is displayed
    """
    keep_browser_open = True

    def test_001_clicktap_on_take_a_short_break_link(self):
        """
        DESCRIPTION: Click/Tap on 'Take a short break' link
        EXPECTED: 'Time-Out' page is opened
        """
        pass

    def test_002_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackPageview', 'page' : '/gambling-controls/time-out/step-1' }
        EXPECTED: );
        """
        pass

    def test_003_clicktap_on_cancel_button(self):
        """
        DESCRIPTION: Click/Tap on 'Cancel' button
        EXPECTED: The user is taken to the 'Responsible Gambling' page
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent', 'eventCategory' : 'gambling controls', 'eventAction' : 'timeout cancel click', 'eventLabel : ' 'cancel button click step 1' }
        EXPECTED: );
        """
        pass

    def test_005_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step 1
        EXPECTED: 'Time-Out' page is opened
        """
        pass

    def test_006_select_any_value_from_the_select_period_of_time_out_dropdown_and_tick_any_reason_for_time_out_checkbox(self):
        """
        DESCRIPTION: Select any value from the 'Select period of time-out' dropdown and Tick any 'Reason for time-out' checkbox
        EXPECTED: * Selected value is displayed within the dropdown
        EXPECTED: * Checkbox is ticked
        EXPECTED: * 'Continue' button becomes active
        """
        pass

    def test_007_clicktap_on_continue_button(self):
        """
        DESCRIPTION: Click/Tap on 'Continue' button
        EXPECTED: 'Time-Out Password' page is opened
        """
        pass

    def test_008_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent', 'eventCategory' : ‘gambling controls' 'eventAction' : 'timeout select period', 'eventLabel : ' '<< TIME PERIOD >>' //e.g. 1 day, 7 days, etc. }
        EXPECTED: );
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent', 'eventCategory' : 'gambling controls', 'eventAction' : 'timeout select reason', 'eventLabel : ' '<< SELECTED REASON >>' //e.g. I spend too much time playing, I gave away too much money, etc. }
        EXPECTED: );
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackPageview', 'page' : '/gambling-controls/time-out/step-2' }
        EXPECTED: );
        """
        pass

    def test_009_clicktap_on_cancel_button(self):
        """
        DESCRIPTION: Click/Tap on 'Cancel' button
        EXPECTED: The user is taken to the 'Responsible Gambling' page
        """
        pass

    def test_010_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push(
        EXPECTED: { 'event' : 'trackEvent', 'eventCategory' : 'gambling controls', 'eventAction' : ‘timeout cancel click step 2’, 'eventLabel : ' 'cancel button click in step 2' }
        EXPECTED: );
        """
        pass
