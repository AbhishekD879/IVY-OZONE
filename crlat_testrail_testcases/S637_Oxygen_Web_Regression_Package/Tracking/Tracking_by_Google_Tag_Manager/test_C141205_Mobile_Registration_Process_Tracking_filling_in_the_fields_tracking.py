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
class Test_C141205_Mobile_Registration_Process_Tracking_filling_in_the_fields_tracking(Common):
    """
    TR_ID: C141205
    NAME: Mobile Registration Process Tracking: filling in the fields tracking
    DESCRIPTION: This test case verifies Registration Process Step Tracking by GTM.
    DESCRIPTION: JIRA Tickets:
    DESCRIPTION: BMA-15432 Registration Process Step Tracking
    PRECONDITIONS: 1. Test Case should be executed on mobile devices
    PRECONDITIONS: 2. Browser console should be opened
    PRECONDITIONS: 3. Instruction for mobile devices debugging: https://confluence.egalacoral.com/display/SPI/How+to+debug+emulator%2C+real+iOS+and+Android+devices
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_tap_join_button(self):
        """
        DESCRIPTION: Tap 'Join' button
        EXPECTED: 'Registration - Step 1' page is opened
        """
        pass

    def test_003_fill_in_first_name_field_with_valid_datatype_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Fill in 'First Name' field with valid data.
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'registration',
        EXPECTED: 'eventAction' : 'field completion',
        EXPECTED: 'eventLabel' : 'first name'
        EXPECTED: });
        """
        pass

    def test_004_repeat_step3_for_all_fields_including_date_picker_within_registration_process(self):
        """
        DESCRIPTION: Repeat step3 for all fields including date picker within Registration process
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'registration',
        EXPECTED: 'eventAction' : 'field completion',
        EXPECTED: 'eventLabel' : '<< FIELD NAME >>'
        EXPECTED: });
        """
        pass

    def test_005_repeat_steps_1_2(self):
        """
        DESCRIPTION: Repeat steps 1-2
        EXPECTED: 
        """
        pass

    def test_006_fill_in_first_name_field_with_invalid_data(self):
        """
        DESCRIPTION: Fill in 'First Name' field with invalid data.
        EXPECTED: Error message with appropriate info is displayed for the user
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'registration',
        EXPECTED: 'eventAction' : 'field error',
        EXPECTED: 'eventLabel' : '<< FIELD NAME >>',
        EXPECTED: 'errorMessage' : '<< ERROR MESSAGE >>',
        EXPECTED: 'errorCode' : '<< ERROR CODE >>'
        """
        pass

    def test_008_repeat_step_6_for_all_fields_including_date_pickertype_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Repeat step 6 for all fields including date picker.
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'registration',
        EXPECTED: 'eventAction' : 'field error',
        EXPECTED: 'eventLabel' : '<< FIELD NAME >>',
        EXPECTED: 'errorMessage' : '<< ERROR MESSAGE >>',
        EXPECTED: 'errorCode' : '<< ERROR CODE >>'
        """
        pass
