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
class Test_C363806_Tracking_of_International_Tote_Meeting_Navigator(Common):
    """
    TR_ID: C363806
    NAME: Tracking of International Tote Meeting Navigator
    DESCRIPTION: This Test Case verifies tracking in the Google Analytic's data Layer due user selects an option from the meeting navigator on the International Tote Event Details page.
    DESCRIPTION: **Jira ticket**
    DESCRIPTION: * BMA-19374 International Tote: Google Analytics Tracking
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * A couple of International Tote meetings should be available
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_navigate_to_the_international_tote_page_and_open_event_details(self):
        """
        DESCRIPTION: Navigate to the International Tote page and open Event Details
        EXPECTED: * International Tote Event Details page is opened
        EXPECTED: * 'Meeting Navigator' with all available meetings is present
        """
        pass

    def test_003_select_some_option_from_meeting_navigator(self):
        """
        DESCRIPTION: Select some option from 'Meeting Navigator'
        EXPECTED: * Respective Meeting is selected
        EXPECTED: * Relevant International Tote Event Details page is opened
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'international tote',
        EXPECTED: 'eventAction' : 'select meeting',
        EXPECTED: 'eventLabel' : '<< USER SELECTION >>',
        EXPECTED: });
        """
        pass

    def test_005_verify_eventlabel_parameter_that_present_in_current_object_in_datalayer_(self):
        """
        DESCRIPTION: Verify 'eventLabel' parameter that present in current object in 'dataLayer' :
        EXPECTED: * 'eventLabel' = The value chosen from the 'Meeting Navigator' dropdown
        """
        pass

    def test_006_repeat_steps_1_5_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat steps 1-5 for Logged In user
        EXPECTED: 
        """
        pass
