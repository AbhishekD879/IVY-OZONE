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
class Test_C88436_Tracking_of_Horse_Racing_Streaming(Common):
    """
    TR_ID: C88436
    NAME: Tracking of Horse Racing Streaming
    DESCRIPTION: This test case verifies tracking of successful launching of a stream for Horse Racing events
    PRECONDITIONS: 1. Test case should be run on **Mobile, Tablet, Desktop and Wrappers**
    PRECONDITIONS: 2. Browser console should be opened
    PRECONDITIONS: 3. Horse Racing events with mapped streams are set up
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

    def test_003_place_a_bet__1_gpb_on_horse_racing_event_with_mapped_stream_to_qualify_for_stream_watching(self):
        """
        DESCRIPTION: Place a bet (>= 1 GPB) on Horse Racing event with mapped stream to qualify for stream watching
        EXPECTED: 
        """
        pass

    def test_004_wait_for_the_event_to_start(self):
        """
        DESCRIPTION: Wait for the event to start
        EXPECTED: 
        """
        pass

    def test_005_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: Stream is successfully launched
        """
        pass

    def test_006_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
        EXPECTED: The following event with corresponding parameters **is present** in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'click',
        EXPECTED: 'eventLabel' : 'watch video stream',
        EXPECTED: 'sportID': '<< OB category ID >>',
        EXPECTED: 'typeID': '<< OB type ID >>',
        EXPECTED: 'eventID' : '<< OB event ID >>'
        EXPECTED: });
        EXPECTED: Parameters 'sportID', 'typeID' and 'eventID' correspond to event that stream was launched for
        """
        pass

    def test_007_collapse_video_object_and_repeat_steps_5_6(self):
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

    def test_008_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: 
        """
        pass

    def test_009_open_oxygen_app_in_a_new_browser_tab(self):
        """
        DESCRIPTION: Open Oxygen app in a new browser tab
        EXPECTED: 
        """
        pass

    def test_010_open_the_same_horse_racing_event(self):
        """
        DESCRIPTION: Open the same Horse Racing event
        EXPECTED: 
        """
        pass

    def test_011_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: Message, that user should be logged in to watch the stream, is displayed
        """
        pass

    def test_012_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter'
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

    def test_013_log_in_with_the_user_who_has_not_placed_a_bet_on_the_same_horse_racing_event(self):
        """
        DESCRIPTION: Log in with the user who has NOT placed a bet on the same Horse Racing event
        EXPECTED: 
        """
        pass

    def test_014_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: Message, that user is not qualified to watch the stream, is displayed
        """
        pass

    def test_015_repeat_step_12(self):
        """
        DESCRIPTION: Repeat step #12
        EXPECTED: 
        """
        pass

    def test_016_open_horse_racing_event_with_mapped_stream_which_is_not_started_yet(self):
        """
        DESCRIPTION: Open Horse Racing event with mapped stream which is not started yet
        EXPECTED: 
        """
        pass

    def test_017_tap_video_stream_button(self):
        """
        DESCRIPTION: Tap 'Video Stream' button
        EXPECTED: Message, that stream is not started yet, is displayed
        """
        pass

    def test_018_repeat_step_12(self):
        """
        DESCRIPTION: Repeat step #12
        EXPECTED: 
        """
        pass
