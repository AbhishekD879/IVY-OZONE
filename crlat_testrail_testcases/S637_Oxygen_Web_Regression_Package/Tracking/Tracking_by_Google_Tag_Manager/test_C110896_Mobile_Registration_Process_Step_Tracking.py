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
class Test_C110896_Mobile_Registration_Process_Step_Tracking(Common):
    """
    TR_ID: C110896
    NAME: Mobile Registration Process Step Tracking
    DESCRIPTION: This test case verifies Registration Process Step Tracking by GTM.
    PRECONDITIONS: 1. Test Case should be executed on mobile devices
    PRECONDITIONS: 2. Browser console should be opened
    PRECONDITIONS: 3. Instruction for mobile devices debugging:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log in' button
        EXPECTED: 'Log In' pop-up is displayed
        """
        pass

    def test_003_tap_join_button_on_log_in_pop_up(self):
        """
        DESCRIPTION: Tap 'Join' button on 'Log In' pop-up
        EXPECTED: 'Registration - Step 1' page is opened
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'registration',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'join now'
        EXPECTED: });
        """
        pass

    def test_005_go_back_go_homepage(self):
        """
        DESCRIPTION: Go back go Homepage
        EXPECTED: Homepage is opened
        """
        pass

    def test_006_tap_join_button_on_header(self):
        """
        DESCRIPTION: Tap 'Join' button on Header
        EXPECTED: 'Registration - Step 1' page is opened
        """
        pass

    def test_007_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: 
        """
        pass

    def test_008_fill_in_all_required_fields_with_valid_data_and_tapnext_step_button(self):
        """
        DESCRIPTION: Fill in all required fields with valid data and tap
        DESCRIPTION: 'Next Step' button
        EXPECTED: 'Registration - Step 2' page is opened
        """
        pass

    def test_009_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/signup/contact-details'
        EXPECTED: 'gtm.uniqueEventId'
        EXPECTED: });
        """
        pass

    def test_010_fill_in_all_required_fields_with_valid_data_for_step_2_and_tap_next_step_button(self):
        """
        DESCRIPTION: Fill in all required fields with valid data for step 2 and tap 'Next Step' button
        EXPECTED: 'Registration - Step 3' page is opened
        """
        pass

    def test_011_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/signup/account-details'
        EXPECTED: 'gtm.uniqueEventId'
        EXPECTED: });
        """
        pass

    def test_012_fill_in_all_required_fields_with_valid_data_for_step_3_and_tap_confirm_registration_button(self):
        """
        DESCRIPTION: Fill in all required fields with valid data for step 3 and tap 'Confirm Registration' button
        EXPECTED: 1. Registration process is successfully completed.
        EXPECTED: 2. Congratulation message is displayed for newly registered user
        """
        pass

    def test_013_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackPageview',
        EXPECTED: 'virtualUrl' : '/signup/complete'
        EXPECTED: 'gtm.uniqueEventId'
        EXPECTED: 'customerID: 12345678'
        EXPECTED: });
        """
        pass

    def test_014_check_that_customerid_is_the_same_as_in_response_31008_for_openapi_registration_request_websocket_response(self):
        """
        DESCRIPTION: Check that 'customerId' is the same as in response 31008 for OpenAPI registration request (WebSocket response)
        EXPECTED: CustomerId number should be the same
        """
        pass
