import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.streaming
@vtest
class Test_C1044402_Verify_Streaming_Progress_tracking_updates(Common):
    """
    TR_ID: C1044402
    NAME: Verify Streaming Progress tracking updates
    DESCRIPTION: This test case verifies Streaming Progress tracking updates
    PRECONDITIONS: 1. User is logged in
    PRECONDITIONS: 2. Browser console should be opened
    """
    keep_browser_open = True

    def test_001_navigate_to_sport_with_streaming_videos_available(self):
        """
        DESCRIPTION: Navigate to <Sport> with Streaming Videos available
        EXPECTED: <Sport> page is opened
        """
        pass

    def test_002_navigate_to_event_with_streaming_video_available(self):
        """
        DESCRIPTION: Navigate to <event> with Streaming Video available
        EXPECTED: <Event> page is opened
        """
        pass

    def test_003_place_a_bet_only_if_it_is_needed_to_watch_the_stream(self):
        """
        DESCRIPTION: Place a bet (only if it is needed to watch the stream)
        EXPECTED: Bet is placed
        """
        pass

    def test_004_tap_on_radio_button_to_start_streaming(self):
        """
        DESCRIPTION: Tap on Radio button to start streaming
        EXPECTED: Video stream is started
        """
        pass

    def test_005_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console 'dataLayer', tap 'Enter' and check the response
        EXPECTED: Objects are displayed within Console window
        """
        pass

    def test_006_expand_corresponding_object(self):
        """
        DESCRIPTION: Expand corresponding object
        EXPECTED: The next static parameters are present:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'streaming',
        EXPECTED: 'eventAction' : 'watch video stream',
        EXPECTED: 'eventLabel' : '<< STREAM TYPE >>'
        EXPECTED: 'sportID': '<< OB category ID >>',
        EXPECTED: 'typeID': '<< OB type ID >>',
        EXPECTED: 'eventID' : '<< OB event ID >>',
        EXPECTED: 'liveStreamProgress' : '<< STREAM PROGRESS >>'
        EXPECTED: });
        """
        pass

    def test_007_repeat_steps_1_6_choosing_a_pre(self):
        """
        DESCRIPTION: Repeat Steps #1-6 choosing a Pre
        EXPECTED: 
        """
        pass

    def test_008_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass

    def test_009_(self):
        """
        DESCRIPTION: 
        EXPECTED: 
        """
        pass
