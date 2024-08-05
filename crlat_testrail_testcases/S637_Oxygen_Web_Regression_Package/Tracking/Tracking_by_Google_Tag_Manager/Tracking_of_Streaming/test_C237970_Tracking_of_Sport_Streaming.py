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
class Test_C237970_Tracking_of_Sport_Streaming(Common):
    """
    TR_ID: C237970
    NAME: Tracking of <Sport> Streaming
    DESCRIPTION: This Test Case verified tracking in the Google Analytic's data Layer due clicking on 'Watch Live' tab within the Event Details page.
    DESCRIPTION: Jira ticket: BMA-19205 Live Streaming Tracking
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * <Sport> events with mapped streams are set up
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in
        """
        pass

    def test_003_wait_for_the_event_to_start(self):
        """
        DESCRIPTION: Wait for the event to start
        EXPECTED: 
        """
        pass

    def test_004_navigate_to_the_event_details_page_with_mapped_stream(self):
        """
        DESCRIPTION: Navigate to the Event Details page with mapped stream
        EXPECTED: * 'Markets' tab is opened by default
        EXPECTED: * 'Watch Live' tab is shown on Event Details page
        """
        pass

    def test_005_click_on_watch_live_tab(self):
        """
        DESCRIPTION: Click on 'Watch Live' tab
        EXPECTED: Stream is successfully launched
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'watch video stream',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: });
        """
        pass

    def test_007_verify_parameters_that_present_in_current_object_in_datalayer(self):
        """
        DESCRIPTION: Verify parameters that present in current object in 'dataLayer'
        EXPECTED: * <OB category ID> = the Openbet numerical category ID.
        EXPECTED: * <OB type ID> = the Openbet numerical type ID.
        EXPECTED: * <OB event ID> = the Openbet numerical event ID that the <Sport> stream was launched for.
        """
        pass

    def test_008_collapse_video_object_and_repeat_steps_5_6(self):
        """
        DESCRIPTION: Collapse video object and repeat steps #5-6
        EXPECTED: The following event **is NOT present** in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'watch video stream',
        EXPECTED: 'sportID': '<< OB category ID >>',
        EXPECTED: 'typeID': '<< OB type ID >>',
        EXPECTED: 'eventID' : '<< OB event ID >>'
        EXPECTED: });
        """
        pass

    def test_009_repeat_steps_2_8_for_any_sport_that_have_live_streaming(self):
        """
        DESCRIPTION: Repeat steps #2-8 for any <Sport> that have Live streaming
        EXPECTED: 
        """
        pass
