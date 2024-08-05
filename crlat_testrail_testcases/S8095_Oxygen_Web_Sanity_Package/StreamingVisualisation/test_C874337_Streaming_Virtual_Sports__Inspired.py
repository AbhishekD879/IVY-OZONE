import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.streaming
@vtest
class Test_C874337_Streaming_Virtual_Sports__Inspired(Common):
    """
    TR_ID: C874337
    NAME: Streaming Virtual Sports - Inspired
    DESCRIPTION: Video Streaming - Verify that the customer can see a video stream on a Virtual Sport
    PRECONDITIONS: Login to Oxygen app
    """
    keep_browser_open = True

    def test_001_navigate_to_virtuals_page_from_the_menu(self):
        """
        DESCRIPTION: Navigate to Virtuals Page from the Menu
        EXPECTED: The Virtual Sports page is loaded
        """
        pass

    def test_002_open_virtual_horses(self):
        """
        DESCRIPTION: Open Virtual Horses
        EXPECTED: The Virtual Horses event page is opened
        EXPECTED: The video stream is displayed and played automatically
        """
        pass

    def test_003_click_on_the_pauseplay_button_from_the_video_player_wait_for_the_video_stream_to_be_available(self):
        """
        DESCRIPTION: Click on the Pause/Play button from the video player (wait for the video stream to be available)
        EXPECTED: The video stream is paused/played
        """
        pass
