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
class Test_C640343_Tracking_of_Live_Sim_Stream_Progress(Common):
    """
    TR_ID: C640343
    NAME: Tracking of Live Sim Stream Progress
    DESCRIPTION: This test case verifies tracking of Live Sim Stream Progress
    PRECONDITIONS: * Test case should be run on Mobile, Tablet, Desktop and Wrappers
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * Make sure there is mapped race visualization for tested event
    PRECONDITIONS: * User is logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_horse_racing_icon_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'Horse Racing' icon on Module selector ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        pass

    def test_003_go_to_hr_event_details_page_of_event_from_uk__ire_group_if_it_is_5_minutes_left_before_the_race_off_time(self):
        """
        DESCRIPTION: Go to HR event details page of event from 'UK & IRE' group if it is 5 minutes left before the race off time
        EXPECTED: * The area below 'WATCH FREE' button is expanded automatically
        EXPECTED: * Visualization video object is shown
        EXPECTED: * Live sim visualization video is playing
        """
        pass

    def test_004_wait_1_second_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Wait 1 second, type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch live sim',
        EXPECTED: 'eventLabel' : '‘watch and bet',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : 'start'
        EXPECTED: });
        """
        pass

    def test_005_verify_sportid_typeid_and_eventid_parameters(self):
        """
        DESCRIPTION: Verify 'sportID', 'typeID' and 'eventID' parameters
        EXPECTED: 'sportID' corresponds to corresponding OB sport ID
        EXPECTED: 'typeID' corresponds to corresponding OB type ID
        EXPECTED: 'eventID' corresponds to corresponding OB event ID
        """
        pass

    def test_006_wait_5_seconds_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Wait 5 seconds, type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch live sim',
        EXPECTED: 'eventLabel' : '‘watch and bet',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : '5 seconds'
        EXPECTED: });
        """
        pass

    def test_007_repeat_steps_1_5collapse_video_object_expand_it_again(self):
        """
        DESCRIPTION: Repeat steps #1-5
        DESCRIPTION: Collapse video object, expand it again
        EXPECTED: The following event is NOT present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch live sim',
        EXPECTED: 'eventLabel' : 'watch and bet',
        EXPECTED: 'sportID': '<< OB category ID >>',
        EXPECTED: 'typeID': '<< OB type ID >>',
        EXPECTED: 'eventID' : '<< OB event ID >>'
        EXPECTED: 'liveStreamProgress' : 'start' / '5 seconds'
        EXPECTED: });
        """
        pass

    def test_008_repeat_steps_1_7_and_wait_for_30_seconds_2_minutes_10_minutes_30_minutes___is_triggered_over_300000_over_30_minutes___is_triggered_over_305959(self):
        """
        DESCRIPTION: Repeat steps #1-7 and wait for
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
        DESCRIPTION: Repeat steps #1-4
        DESCRIPTION: Pause video streaming and stay on the same page
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch live sim',
        EXPECTED: 'eventLabel' : '‘watch and bet',
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
        EXPECTED: 'eventAction' : 'watch live sim',
        EXPECTED: 'eventLabel' : '‘watch and bet',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : 'stop'
        EXPECTED: });
        """
        pass

    def test_011_repeat_steps_1_4wait_until_video_streaming_finishestype_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Repeat steps #1-4
        DESCRIPTION: Wait until video streaming finishes
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following object with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch live sim',
        EXPECTED: 'eventLabel' : '‘watch and bet',
        EXPECTED: 'sportID': '<OB category ID>',
        EXPECTED: 'typeID': '<OB type ID>',
        EXPECTED: 'eventID' : '<OB event ID>'
        EXPECTED: 'liveStreamProgress' : 'complete'
        EXPECTED: });
        """
        pass

    def test_012_log_in_and_repeat_steps_2_11(self):
        """
        DESCRIPTION: Log in and repeat steps #2-11
        EXPECTED: 
        """
        pass
