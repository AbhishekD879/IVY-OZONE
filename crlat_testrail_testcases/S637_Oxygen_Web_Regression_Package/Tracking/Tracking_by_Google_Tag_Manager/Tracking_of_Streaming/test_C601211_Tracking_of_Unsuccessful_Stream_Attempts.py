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
class Test_C601211_Tracking_of_Unsuccessful_Stream_Attempts(Common):
    """
    TR_ID: C601211
    NAME: Tracking of Unsuccessful Stream Attempts
    DESCRIPTION: This test case verifies tracking of Unsuccessful Stream Attempts
    PRECONDITIONS: * Test case should be run on **Mobile, Tablet, Desktop and Wrappers**
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * User is logged out
    PRECONDITIONS: * To check response use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: where, XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_event_details_page_of_any_sportrace_for_the_event_with_streaming(self):
        """
        DESCRIPTION: Go Event Details page of any <Sport>/<Race> for the event with streaming
        EXPECTED: 
        """
        pass

    def test_003_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: * User is not able to watch the stream
        EXPECTED: * "In order to watch this stream, you must be logged in and have a positive balance or have placed a sportsbook bet in the last 24 hours." message is displayed
        """
        pass

    def test_004_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters **is present** in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Livestream',
        EXPECTED: 'eventAction' : 'error',
        EXPECTED: 'liveStreamError' : 'In order to watch this stream, you must be logged in and have a positive balance or have placed a sportsbook bet in the last 24 hours.'
        EXPECTED: });
        """
        pass

    def test_005_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is logged in
        """
        pass

    def test_006_go_event_details_page_of_any_sportrace_for_the_event_with_streaming(self):
        """
        DESCRIPTION: Go Event Details page of any <Sport>/<Race> for the event with streaming
        EXPECTED: 
        """
        pass

    def test_007_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: * User is not able to watch the stream
        EXPECTED: * "In order to view this event you need to place a bet greater than or equal to £1" message is displayed
        """
        pass

    def test_008_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters **is present** in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Livestream',
        EXPECTED: 'eventAction' : 'error',
        EXPECTED: 'liveStreamError' : 'In order to view this event you need to place a bet greater than or equal to £1'
        EXPECTED: });
        """
        pass

    def test_009_go_event_details_page_of_any_sportrace_for_the_event_that_should_be_more_than_5_min_left_to_event_start_time(self):
        """
        DESCRIPTION: Go Event Details page of any <Sport>/<Race> for the event that should be more than 5 min left to event start time
        EXPECTED: 
        """
        pass

    def test_010_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: * User is not able to watch the stream
        EXPECTED: * "This stream has not yet started. Please try again soon." message is displayed
        """
        pass

    def test_011_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters **is present** in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Livestream',
        EXPECTED: 'eventAction' : 'error',
        EXPECTED: 'liveStreamError' : 'This stream has not yet started. Please try again soon.'
        EXPECTED: });
        """
        pass

    def test_012_open_event_details_page_of_any_sportrace_for_the_event_that_is_finished(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport>/<Race> for the event that is finished
        EXPECTED: 
        """
        pass

    def test_013_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: * User is not able to watch the stream
        EXPECTED: * "This event is over." message is displayed
        """
        pass

    def test_014_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters **is present** in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Livestream',
        EXPECTED: 'eventAction' : 'error',
        EXPECTED: 'liveStreamError' : 'This event is over.'
        EXPECTED: });
        """
        pass

    def test_015_open_event_details_page_of_any_sportrace_for_the_event_for_which_streaming_is_not_mapped_however_one_of_attribute_drilldowntagnames_evflag_ivm_evflag_pvm_evflag_ava_evflag_rva_evflag_rpm_evflag_gvmis_present_in_ss_response(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport>/<Race> for the event for which streaming is not mapped, however, one of attribute **'drilldownTagNames'**
        DESCRIPTION: * 'EVFLAG_IVM'
        DESCRIPTION: * 'EVFLAG_PVM'
        DESCRIPTION: * 'EVFLAG_AVA'
        DESCRIPTION: * 'EVFLAG_RVA'
        DESCRIPTION: * 'EVFLAG_RPM'
        DESCRIPTION: * 'EVFLAG_GVM'
        DESCRIPTION: is present in SS response
        EXPECTED: 
        """
        pass

    def test_016_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: * User is not able to watch the stream
        EXPECTED: * "The Stream for this event is currently not available." message is displayed
        """
        pass

    def test_017_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters **is present** in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'Livestream',
        EXPECTED: 'eventAction' : 'error',
        EXPECTED: 'liveStreamError' : 'The Stream for this event is currently not available.'
        EXPECTED: });
        """
        pass

    def test_018_go_event_details_page_of_any_sportrace_for_the_event_that_returns_an_error_from_any_streaming_providerapi_error(self):
        """
        DESCRIPTION: Go Event Details page of any <Sport>/<Race> for the event that returns an error from any streaming provider/API error
        EXPECTED: 
        """
        pass

    def test_019_repeat_steps_16_17(self):
        """
        DESCRIPTION: Repeat steps #16-17
        EXPECTED: 
        """
        pass

    def test_020_go_to_live_stream_widget_and_find_an_event_that_returns_an_error_from_any_streaming_providerapi_error(self):
        """
        DESCRIPTION: Go to Live Stream widget and find an event that returns an error from any streaming provider/API error
        EXPECTED: 
        """
        pass

    def test_021_repeat_steps_16_17(self):
        """
        DESCRIPTION: Repeat steps #16-17
        EXPECTED: 
        """
        pass
