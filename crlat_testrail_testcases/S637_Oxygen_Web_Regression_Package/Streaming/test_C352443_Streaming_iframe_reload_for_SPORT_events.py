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
class Test_C352443_Streaming_iframe_reload_for_SPORT_events(Common):
    """
    TR_ID: C352443
    NAME: Streaming iframe reload for <SPORT> events
    DESCRIPTION: This test case verifies Streaming video reload after losing and restoring the connection to the Internet or coming back from sleep mode/background for <SPORT> events
    PRECONDITIONS: * User is logged in to Oxygen application
    PRECONDITIONS: * There are <SPORT> events with mapped streaming from different providers (Perform, IMG, iGameMedia, etc)
    PRECONDITIONS: * User has placed bets on event with mapped streaming
    PRECONDITIONS: [How to Map Video Streams to Events] [1].
    PRECONDITIONS: [1]: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    """
    keep_browser_open = True

    def test_001_navigate_to_event_details_page_of_event_with_mapped_streaming_from_perform(self):
        """
        DESCRIPTION: Navigate to Event Details page of event with mapped streaming from Perform
        EXPECTED: * Event Details page is opened
        EXPECTED: * Stream button is present
        """
        pass

    def test_002_clicktap_on_stream_button(self):
        """
        DESCRIPTION: Click/Tap on Stream button
        EXPECTED: Video player is summoned and streaming is started
        """
        pass

    def test_003_lock_device_for_few_minutes_so_it_goes_to_sleep_mode(self):
        """
        DESCRIPTION: Lock device for few minutes, so it goes to sleep mode
        EXPECTED: 
        """
        pass

    def test_004_unlock_deviceverify_console(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify console
        EXPECTED: 'reload components' command is shown in console
        """
        pass

    def test_005_verify_page_and_video_behavior(self):
        """
        DESCRIPTION: Verify page and video behavior
        EXPECTED: * screen component(iframe) is reloaded
        EXPECTED: * video player is no longer shown
        """
        pass

    def test_006_clicktap_on_stream_button(self):
        """
        DESCRIPTION: Click/Tap on Stream button
        EXPECTED: * Video streaming is started and shows up-to-date information
        """
        pass

    def test_007_move_app_to_background_for_few_minutes(self):
        """
        DESCRIPTION: Move app to background for few minutes
        EXPECTED: 
        """
        pass

    def test_008_move_app_to_foregroundverify_console(self):
        """
        DESCRIPTION: Move app to foreground
        DESCRIPTION: Verify console
        EXPECTED: 'reload components' command is shown in console
        """
        pass

    def test_009_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps 5-6
        EXPECTED: 
        """
        pass

    def test_010_make_device_lose_internet_connection_and_wait_few_minutes(self):
        """
        DESCRIPTION: Make device lose internet connection and wait few minutes
        EXPECTED: * Pop-up about loosing internet appears
        EXPECTED: * Video stream stops playing
        """
        pass

    def test_011_restore_internet_connection_it_may_take_some_timeverify_console(self):
        """
        DESCRIPTION: Restore internet connection (it may take some time)
        DESCRIPTION: Verify console
        EXPECTED: 'reload components' command is shown in console
        """
        pass

    def test_012_repeat_steps_5_6(self):
        """
        DESCRIPTION: Repeat steps 5-6
        EXPECTED: 
        """
        pass

    def test_013_navigate_to_event_details_page_of_event_with_mapped_streaming_from_img(self):
        """
        DESCRIPTION: Navigate to Event Details page of event with mapped streaming from IMG
        EXPECTED: * Event Details page is opened
        EXPECTED: * Stream button is present
        """
        pass

    def test_014_repeat_steps_2_13(self):
        """
        DESCRIPTION: Repeat steps #2-13
        EXPECTED: Results are the same
        """
        pass

    def test_015_navigate_to_event_details_page_of_event_with_mapped_streaming_from_igamemedia(self):
        """
        DESCRIPTION: Navigate to Event Details page of event with mapped streaming from iGameMedia
        EXPECTED: * Event Details page is opened
        EXPECTED: * Stream button is present
        """
        pass

    def test_016_repeat_steps_2_13(self):
        """
        DESCRIPTION: Repeat steps #2-13
        EXPECTED: Results are the same
        """
        pass
