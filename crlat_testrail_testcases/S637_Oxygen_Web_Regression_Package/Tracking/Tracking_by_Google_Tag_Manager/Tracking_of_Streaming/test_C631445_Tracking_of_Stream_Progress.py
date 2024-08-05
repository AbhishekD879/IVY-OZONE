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
class Test_C631445_Tracking_of_Stream_Progress(Common):
    """
    TR_ID: C631445
    NAME: Tracking of Stream Progress
    DESCRIPTION: This test case verifies tracking of Stream Progress
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * <Sport> / <Race> events with mapped streams are set up
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: NOTE: Stream tracking is not implemented for Greyhounds
    PRECONDITIONS: NOTE: Stream progress tracking is not implemented for both wrappers:
    PRECONDITIONS: https://jira.egalacoral.com/browse/BMAN-3497
    PRECONDITIONS: https://jira.egalacoral.com/browse/BMAN-3627
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
        EXPECTED: Video streaming is launched
        """
        pass

    def test_004_wait_1_second_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Wait 1 second, type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch video stream',
        EXPECTED: 'eventLabel' : '<<STREAM TYPE>>',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : 'start'
        EXPECTED: });
        """
        pass

    def test_005_wait_5_seconds_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Wait 5 seconds, type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch video stream',
        EXPECTED: 'eventLabel' : '<<STREAM TYPE>>',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : '5 seconds'
        EXPECTED: });
        """
        pass

    def test_006_verify_eventlabel_parameter(self):
        """
        DESCRIPTION: Verify 'eventLabel' parameter
        EXPECTED: * 'eventLabel = watch and bet' if user launched <Sport> stream
        EXPECTED: * 'eventLabel = bet and watch' if user launched Horse Race streaming
        """
        pass

    def test_007_verify_sportid_typeid_and_eventid_parameters(self):
        """
        DESCRIPTION: Verify 'sportID', 'typeID' and 'eventID' parameters
        EXPECTED: * 'sportID' corresponds to corresponding OB sport ID
        EXPECTED: * 'typeID' corresponds to corresponding OB type ID
        EXPECTED: * 'eventID' corresponds to corresponding OB event ID
        """
        pass

    def test_008_repeat_steps_1_7_and_wait_for_30_seconds_2_minutes_10_minutes_30_minutes___is_triggered_over_300000_over_30_minutes___is_triggered_over_305959(self):
        """
        DESCRIPTION: Repeat steps #1-7 and wait for:
        DESCRIPTION: * 30 seconds
        DESCRIPTION: * 2 minutes
        DESCRIPTION: * 10 minutes
        DESCRIPTION: * 30 minutes - is triggered over 30:00:00
        DESCRIPTION: * over 30 minutes - is triggered over 30:59:59
        EXPECTED: **'liveStreamProgress'** parameter corresponds to appropriate time value
        """
        pass

    def test_009_repeat_steps_1_4pause_video_streaming_and_stay_on_the_same_pagetype_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Repeat Steps #1-4
        DESCRIPTION: Pause video streaming and stay on the same page
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch video stream',
        EXPECTED: 'eventLabel' : '<<STREAM TYPE>>',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : 'pause'
        EXPECTED: });
        """
        pass

    def test_010_repeat_steps_1_4navigate_away_from_streaming_pagetype_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Repeat steps #1-4
        DESCRIPTION: Navigate away from streaming page
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch video stream',
        EXPECTED: 'eventLabel' : '<<STREAM TYPE>>',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : 'stop'
        EXPECTED: });
        """
        pass

    def test_011_repeat_steps_1_4wait_until_video_streaming_finishestype_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Repeat Steps #1-4
        DESCRIPTION: Wait until video streaming finishes
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch video stream',
        EXPECTED: 'eventLabel' : '<<STREAM TYPE>>',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : 'complete'
        EXPECTED: });
        """
        pass

    def test_012_load_oxygen_app_in_desktop_mode(self):
        """
        DESCRIPTION: Load Oxygen app in Desktop mode
        EXPECTED: * 'Live Stream' widget is displayed in Right/Left column
        EXPECTED: * Video streaming is launched automatically
        """
        pass

    def test_013_repeat_steps_1_10(self):
        """
        DESCRIPTION: Repeat steps #1-10
        EXPECTED: 
        """
        pass
